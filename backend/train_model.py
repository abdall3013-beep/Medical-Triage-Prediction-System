"""
====================================================
Medical Triage Prediction System
Model Training Script
====================================================

Author : Your Name
Model  : Logistic Regression
Library: Scikit-Learn

Description:
This script trains the machine learning model
and saves the trained model for the Flask API.
"""

# ==========================================
# Import Libraries
# ==========================================

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# Configuration
# ==========================================

DATASET_PATH = "synthetic_medical_triage.csv"

MODEL_PATH = "model.pkl"

SCALER_PATH = "scaler.pkl"

ENCODER_PATH = "label_encoders.pkl"

FEATURE_IMPORTANCE_PATH = "feature_importance.csv"


# ==========================================
# Load Dataset
# ==========================================

def load_dataset():

    print("=" * 60)
    print("Loading Dataset...")
    print("=" * 60)

    df = pd.read_csv(DATASET_PATH)

    print(df.head())

    print("\nShape :", df.shape)

    print("\nInformation")

    print(df.info())

    print("\nStatistics")

    print(df.describe())

    return df


# ==========================================
# Clean Dataset
# ==========================================

def clean_dataset(df):

    print("\nChecking Missing Values...\n")

    print(df.isnull().sum())

    print("\nChecking Duplicate Rows...")

    print(df.duplicated().sum())

    # Remove duplicated rows

    df = df.drop_duplicates()

    # Fill missing numeric values

    numeric_columns = df.select_dtypes(include=np.number).columns

    for col in numeric_columns:

        df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical values

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:

        df[col] = df[col].fillna(df[col].mode()[0])

    print("\nCleaning Finished Successfully")

    return df


# ==========================================
# Encode Categorical Columns
# ==========================================

def encode_features(df):

    print("\nEncoding Categorical Features...")

    encoders = {}

    categorical_columns = df.select_dtypes(include="object").columns

    for col in categorical_columns:

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

        encoders[col] = encoder

    return df, encoders


# ==========================================
# Split Features & Target
# ==========================================

def prepare_features(df):

    X = df.drop("triage_level", axis=1)

    y = df["triage_level"]

    feature_names = X.columns.tolist()

    return X, y, feature_names
# ==========================================
# Scale Features
# ==========================================

def scale_features(X):

    print("\nScaling Features...")

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


# ==========================================
# Split Dataset
# ==========================================

def split_dataset(X, y):

    print("\nSplitting Dataset...")

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42,

        stratify=y

    )

    print("Training Samples :", len(X_train))

    print("Testing Samples  :", len(X_test))

    return X_train, X_test, y_train, y_test


# ==========================================
# Train Model
# ==========================================

def train_model(X_train, y_train):

    print("\nTraining Logistic Regression Model...")

    model = LogisticRegression(

        max_iter=1000,

        random_state=42

    )

    model.fit(

        X_train,

        y_train

    )

    print("Training Finished Successfully")

    return model


# ==========================================
# Evaluate Model
# ==========================================

def evaluate_model(model, X_test, y_test):

    print("\nEvaluating Model...")

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(

        y_test,

        y_pred

    )

    precision = precision_score(

        y_test,

        y_pred,

        average="weighted"

    )

    recall = recall_score(

        y_test,

        y_pred,

        average="weighted"

    )

    f1 = f1_score(

        y_test,

        y_pred,

        average="weighted"

    )

    print("\n==============================")

    print("Model Evaluation")

    print("==============================")

    print(f"Accuracy  : {accuracy:.4f}")

    print(f"Precision : {precision:.4f}")

    print(f"Recall    : {recall:.4f}")

    print(f"F1 Score  : {f1:.4f}")

    print("\nClassification Report\n")

    print(classification_report(

        y_test,

        y_pred

    ))

    cm = confusion_matrix(

        y_test,

        y_pred

    )

    print("\nConfusion Matrix\n")

    print(cm)

    return y_pred
# ==========================================
# Feature Importance
# ==========================================

def save_feature_importance(

    model,

    feature_names

):

    print("\nSaving Feature Importance...")

    importance = pd.DataFrame({

        "Feature": feature_names,

        "Coefficient": model.coef_[0]

    })

    importance = importance.sort_values(

        by="Coefficient",

        ascending=False

    )

    importance.to_csv(

        FEATURE_IMPORTANCE_PATH,

        index=False

    )

    print(importance)


# ==========================================
# Save Files
# ==========================================

def save_files(

    model,

    scaler,

    encoders

):

    print("\nSaving Model Files...")

    joblib.dump(

        model,

        MODEL_PATH

    )

    joblib.dump(

        scaler,

        SCALER_PATH

    )

    joblib.dump(

        encoders,

        ENCODER_PATH

    )

    print("✔ model.pkl")

    print("✔ scaler.pkl")

    print("✔ label_encoders.pkl")
    # ==========================================
# Main Function
# ==========================================

def main():

    df = load_dataset()

    df = clean_dataset(df)

    df, encoders = encode_features(df)

    X, y, feature_names = prepare_features(df)

    X_scaled, scaler = scale_features(X)

    X_train, X_test, y_train, y_test = split_dataset(

        X_scaled,

        y

    )

    model = train_model(

        X_train,

        y_train

    )

    evaluate_model(

        model,

        X_test,

        y_test

    )

    save_feature_importance(

        model,

        feature_names

    )

    save_files(

        model,

        scaler,

        encoders

    )

    print("\n========================================")

    print("Project Finished Successfully")

    print("========================================")


if __name__ == "__main__":

    main()