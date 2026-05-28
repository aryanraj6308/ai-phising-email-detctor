# AI Phishing Email Detector

A machine learning web app that predicts whether an email or message is likely to be phishing. The project uses Python, scikit-learn, and Streamlit, and is structured so it can be uploaded directly to GitHub.

## Features

- Paste or upload email text for analysis
- Predicts phishing probability with a trained NLP model
- Highlights suspicious words and phrases
- Shows confidence score, risk level, and safety tips
- Includes a small sample dataset for quick local testing
- Supports replacing the sample data with larger Kaggle phishing datasets

## Tech Stack

- Python
- Streamlit
- scikit-learn
- pandas
- joblib

## Project Structure

```text
ai-phishing-email-detector/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── sample_emails.csv
├── models/
│   └── .gitkeep
└── src/
    ├── __init__.py
    ├── detector.py
    └── suspicious_terms.py
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Train the model:

```bash
python train_model.py
```

4. Run the dashboard:

```bash
streamlit run app.py
```

## Using a Kaggle Dataset

The bundled dataset is intentionally small so the project works immediately. For better accuracy, download a phishing email or SMS dataset from Kaggle and format it as a CSV with these columns:

```text
text,label
"Your email message here",phishing
"A normal safe message here",safe
```

Then train with:

```bash
python train_model.py --data path/to/your_dataset.csv
```

Labels can be `phishing` / `safe`, `1` / `0`, or similar common values.

## How It Works

The model uses a TF-IDF vectorizer to convert message text into numeric features, then trains a logistic regression classifier. The Streamlit dashboard loads the trained model, predicts phishing probability, and highlights terms commonly found in phishing attempts.

## Important Note

This tool is for learning and portfolio purposes. It should not be used as the only security control for real email systems.

