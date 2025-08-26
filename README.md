
# Ubundi Codex Agent

Ubundi Codex Agent is an AI-powered assistant for processing, analyzing, and interacting with resume and cover letter data. It leverages advanced language models, FAISS vector databases, and fine-tuning techniques for customized performance.

---

## 🚀 Features

- 📄 **Resume & Cover Letter Processing** – Ingests and analyzes documents in multiple formats.  
- 🔍 **Vector Database Integration** – Uses FAISS for efficient similarity search.  
- 🧠 **Fine-tuning & Custom Models** – Supports LoRA fine-tuning for GPT-2 and model adapters.  
- 🌐 **API & UI** – REST API endpoints and a simple user interface.  
- 🛠 **Extensible Utilities** – Modular data loaders and web tools.  

---

## 📂 Project Structure


.
├── .env
├── persona.yaml
├── requirements.txt
├── data/
│   ├── resume\_instructions.jsonl
│   └── info/
│       ├── Clarence\_Ebebe\_Cover\_Letter.pdf
│       ├── ClarenceEbebeResume\_AIEngineer\_Resume.pdf
│       ├── cover.txt
│       ├── extra.md
│       ├── extra.txt
│       └── resume.txt
├── models/
│   └── lora-resume-gpt2/
├── scripts/
│   ├── agent.py
│   ├── api.py
│   ├── build\_vector\_db.py
│   ├── finetune.py
│   ├── ingest\_new\.py
│   ├── prepare\_data.py
│   └── ui.py
├── storage/
│   └── faiss/
└── utils/
├── loader.py
└── webtools.py



---

## ⚙️ Setup

### 1. Clone the Repository
```sh
git clone <repo-url>
cd Ubundi_Codex_Agent


### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```sh
cp .env.example .env
# Update the .env file with your configs
```

### 4. Prepare Data

Place your resume and cover letter files inside:

```
data/info/
```

---

## 🛠 Usage

### Build the Vector Database

```sh
python scripts/build_vector_db.py
```

### Fine-tune the Model (Optional)

```sh
python scripts/finetune.py \
    --data_path data/resume_instructions.jsonl \
    --output_dir models/lora-resume-gpt2 \
    --model_name gpt2 \
    --epochs 3 \
    --batch_size 4
```

> Tweak `epochs` and `batch_size` for your needs.

### Run the API

```sh
python scripts/api.py
```

### Run the UI

```sh
python scripts/ui.py
```

---

## 📜 Scripts Overview

* `agent.py` – Core agent logic
* `api.py` – REST API server
* `build_vector_db.py` – Builds FAISS vector database
* `finetune.py` – Fine-tunes the language model
* `ingest_new.py` – Adds new data to the system
* `prepare_data.py` – Cleans/prepares data for processing
* `ui.py` – Launches the user interface

---

## 🔧 Utilities

* `loader.py` – Data loading utilities
* `webtools.py` – Web tools and helpers

---

## 💾 Storage

* `storage/faiss/` – FAISS index files

---

## 🤖 Models

* `lora-resume-gpt2/` – Fine-tuned GPT-2 model with LoRA adapters

---


