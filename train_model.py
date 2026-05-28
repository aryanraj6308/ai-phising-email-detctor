import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


DEFAULT_DATA_PATH = Path("data/sample_emails.csv")
DEFAULT_MODEL_PATH = Path("models/phishing_detector.joblib")


def normalize_label(value):
    normalized = str(value).strip().lower()
    phishing_values = {"1", "phishing", "phish", "malicious", "spam", "fraud"}
    safe_values = {"0", "safe", "legitimate", "ham", "normal", "benign"}

    if normalized in phishing_values:
        return 1
    if normalized in safe_values:
        return 0
    raise ValueError(f"Unknown label value: {value}")


def load_dataset(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    required_columns = {"text", "label"}
    missing = required_columns.difference(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

    data = data.dropna(subset=["text", "label"]).copy()
    data["label"] = data["label"].map(normalize_label)
    return data


def train(data_path: Path, model_path: Path) -> None:
    data = load_dataset(data_path)

    x_train, x_test, y_train, y_test = train_test_split(
        data["text"],
        data["label"],
        test_size=0.25,
        random_state=42,
        stratify=data["label"],
    )

    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            (
                "classifier",
                LogisticRegression(max_iter=1000, class_weight="balanced"),
            ),
        ]
    )

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(f"Model saved to {model_path}")
    print()
    print(classification_report(y_test, predictions, target_names=["safe", "phishing"]))


def parse_args():
    parser = argparse.ArgumentParser(description="Train the phishing email detector.")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args.data, args.model)

