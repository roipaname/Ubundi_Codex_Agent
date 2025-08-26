# agent.py
import os
from typing import List, Tuple
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.webtools import ddg_search, fetch_readable
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

load_dotenv()
BASE_MODEL = os.getenv("BASE_MODEL", "gpt2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DB_DIR = "storage/faiss"
LORA_DIR = "models/lora-resume-gpt2/checkpoint-16"

# Load generator (base + LoRA )
tokenizer = AutoTokenizer.from_pretrained(LORA_DIR if os.path.exists(LORA_DIR) else BASE_MODEL)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    LORA_DIR if os.path.exists(LORA_DIR) else BASE_MODEL,
    device_map="auto"
)
model.eval()

# Load embeddings + FAISS
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
db = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)

def retrieve(query: str, k: int = 4) -> List[Tuple[str, dict]]:
    docs = db.similarity_search(query, k=k)
    return [(d.page_content, d.metadata) for d in docs]

PROMPT = """You are a helpful AI assistant specialized in Clarence's CV, career history, projects, education, and skills.
Use the provided CONTEXT (from Clarence's resume or related documents) and, if available, WEB_SNIPPETS (recent information about Clarence or his work online).
Cite sources inline: use [R] for resume/context chunks and [W] for web snippets.
Answer clearly, concisely, and accurately. If the information is not present, politely state that it is unavailable.

Question:
{question}

CONTEXT (Resume):
{context}


"""


@torch.inference_mode()
def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=900)  # 900 leaves room for output
    input_ids = inputs["input_ids"]

    out = model.generate(
        input_ids,
        max_length=1024,        # absolute model cap
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)


def answer(query: str, use_web: bool = True, k: int = 4):
    # 1) RAG from lectures
    chunks = retrieve(query, k=k)
    context = "\n\n".join(f"[L{i+1}] {c[:1200]}" for i, (c, _) in enumerate(chunks))

    # 2) Web (lightweight) if requested
    web_txt = ""
    if use_web:
        hits = ddg_search(query, max_results=3)
        snippets = []
        for i, h in enumerate(hits):
            try:
                text = fetch_readable(h["url"])[:1500]
                snippets.append(f"[W{i+1}] {h['title']}\n{text}\n(Source: {h['url']})")
            except Exception:
                continue
        web_txt = "\n\n".join(snippets)

    prompt = PROMPT.format(question=query, context=context)
    return generate_answer(prompt)

if __name__ == "__main__":
    print(answer("where did clarence work", use_web=False))
