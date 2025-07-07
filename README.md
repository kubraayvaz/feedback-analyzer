# 🧠 AI-Powered Customer Feedback Analyzer

This is an MVP (Minimum Viable Product) of an AI-powered tool that helps product and support teams extract meaningful insights from customer feedback using OpenAI’s GPT model. Built with **Streamlit** for rapid prototyping and an intuitive dashboard experience.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🔍 Features

- 📁 Upload customer feedback via CSV
- 🤖 Automatic **Sentiment Analysis** (Positive / Neutral / Negative)
- 🏷️ Feedback **Categorization** (Bug, Feature Request, UX, Other)
- 🧠 Summarized key issues using GPT
- 📊 Interactive visual dashboard for quick insights

---


## 🚀 Demo

![App Demo](resources/demo-screenshot.png)

> Coming soon — you can run it locally using the instructions below.

---

## 📦 Tech Stack

- **Frontend & Dashboard:** [Streamlit](https://streamlit.io/)
- **AI / NLP:** [OpenAI GPT-4 API](https://platform.openai.com/)
- **Data Handling:** Pandas, Matplotlib
- **Environment Config:** python-dotenv
- **Unit testing framework:** pytest

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone <repo-git-url>
cd feedback-analyzer
```

### 2.Create and Activate Virtual Environment (Optional)

```bash
python -m venv venv
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=your-api-key-here
```

⚠️ Do not commit this file. It’s already added to .gitignore.

### 5. Run the app

```bash
streamlit run app/main.py
```

### 📄 Input CSV Format

To use this app, upload a **CSV file** that contains a column with user feedback.

You can try it with the provided [example file](resources/sample_feedbacks.csv).

#### ✅ Required Column

- `feedback` (case-insensitive)
  - This column should contain **free-text user comments** (e.g., complaints, suggestions, praise).
  - The app will normalize the column name internally, so `Feedback`, `FEEDBACK`, or `feedBack` are all accepted.

#### ⚠️ Validation Rules

- The CSV must be readable (standard comma-separated file).
- The file **must contain** a column named `"feedback"` (in any case).
- The feedback column **must not be completely empty**.
- CSVs missing the feedback column will trigger an error.

### 6. Run tests

```bash
pytest tests/
```


## 🤖 AI Assistance Disclosure

This project was developed with the assistance of AI tools, including [ChatGPT](https://openai.com/chatgpt) and [GitHub Copilot](https://github.com/features/copilot), to help generate code, refactor, and document the project. All code has been reviewed, refactored, and organized by the author.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
