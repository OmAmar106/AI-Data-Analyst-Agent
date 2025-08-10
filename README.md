# 📊 Data Analyst Agent

A **prompt-driven Data Analysis Agent** built as part of the **TDS Course (IIT Madras)**.
The agent processes user prompts, performs **intelligent data analysis**, and provides insights using a combination of **LangChain**, **Groq API**, **AI Pipe API**, and **Perplexity API**.

---

## ✨ Features

* 🧠 **Prompt-Based Analysis** – Just describe your requirement in plain language.
* 🔗 **LangChain Integration** – Orchestrates data retrieval, processing, and LLM responses.
* ⚡ **Groq API** – High-speed inference for large language model queries.
* 🔍 **AI Pipe API** – Custom AI pipeline integration for advanced analytics.
* 📚 **Perplexity API** – Augments analysis with up-to-date web information.
* 📈 **Data Insights** – Summaries, trends, and visualizations.

---

## Screenshots

To Be Updated

---

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **Pandas, NumPy, Matplotlib** (for analysis & visualization)

---

## 📦 Installation

```bash
>> git clone https://github.com/OmAmar106/Data-Analyst-Agent-TDS-Project.git
>> cd Data-Analyst-Agent-TDS-Project
```
```bash
python -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirements.txt
# Set up API keys in .env file

python main/app.py
```

---

## 🚀 Usage

* Enter your **prompt** (e.g., *"Scrape the list of highest grossing films from Wikipedia and tell the highest grossing film."*)
* The agent:
  1. Parses the prompt
  2. Retrieves & processes data
  3. Generates insights & visualizations
  4. Returns a natural language summary

## 🔌 API

- **Endpoint**: `/analyze`
- **Method**: `POST`
- **Expected Input**:
  - `question`: string