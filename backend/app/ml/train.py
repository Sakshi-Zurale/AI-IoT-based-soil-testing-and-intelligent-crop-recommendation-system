from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data" / "crop_training_demo.csv"
MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL = MODEL_DIR / "crop_model.joblib"

FEATURES = ["N", "P", "K", "temperature", "humidity", "moisture"]


def train():
    df = pd.read_csv(DATA)

    X = df[FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.50,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        random_state=42
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Demo dataset accuracy:", round(accuracy_score(y_test, pred), 4))
    print(classification_report(y_test, pred, zero_division=0))

    joblib.dump(
        {
            "model": model,
            "features": FEATURES
        },
        MODEL
    )

    print("Saved:", MODEL)


if __name__ == "__main__":
    train()