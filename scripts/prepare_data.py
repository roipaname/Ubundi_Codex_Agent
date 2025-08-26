import os, json, random
from pathlib import Path
from utils.loader import collect_files, load_any

random.seed(42)

DATA_DIR = "data/info"
OUT_PATH = "data/resume_instructions.jsonl"

TEMPLATE = (
    "You are a helpful AI assistant that knows everything about the user's CV, "
    "career history, projects, education, and skills. Based on the following extracted passage "
    "from the CV or related documents, answer the user's question clearly, accurately, "
    "and concisely. If the information is not present in the passage, politely say so.\n\n"
    "### PASSAGE\n{passage}\n\n"
    "### QUESTION\n{question}\n\n"
    "### ANSWER\n{answer}"
)


GENERIC_QS = [
    # Personal background
    "What is the user's educational background?",
    "Summarize the user's career journey so far.",
    "What industries has the user worked in?",

    # Skills
    "List the user's top technical skills.",
    "What programming languages does the user know?",
    "Which AI/ML frameworks has the user used?",
    "What database or data engineering tools has the user worked with?",
    "What cloud platforms does the user have experience in?",

    # Projects / Experience
    "Describe a project where the user applied machine learning.",
    "Give an example of a fullstack project the user built.",
    "What data engineering projects has the user worked on?",
    "How has the user applied AI to solve real-world problems?",
    "List some tools or libraries the user integrated in past projects.",

    # Achievements
    "What certifications or awards has the user received?",
    "What are some of the user's notable achievements?",
    "Summarize the user's research or academic contributions.",

    # Work style / Soft skills
    "How does the user approach teamwork and collaboration?",
    "What problem-solving strategies does the user use?",
    "How does the user handle learning new technologies quickly?",

    # Job-fit / Career goals
    "What kind of roles is the user best suited for?",
    "How does the user's background align with data engineering or AI roles?",
    "What are the user's career aspirations?"
]



def chunk(text, size=800, overlap=150):
    tokens = text.split()
    out, i = [], 0
    while i < len(tokens):
        out.append(" ".join(tokens[i:i+size]))
        i += size - overlap
    return out

def main():
    files = collect_files(DATA_DIR)
    os.makedirs(Path(OUT_PATH).parent, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as out:
        for fp in files:
            text = load_any(fp)
            for ch in chunk(text):
                q = random.choice(GENERIC_QS)
                # trivial "answer" bootstrap: use the first 3-4 sentences of the chunk
                ans = " ".join(ch.split(".")[:3]).strip()
                prompt = TEMPLATE.format(passage=ch, question=q, answer=ans)
                rec = {"prompt": prompt, "response": ans}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
