import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def load_data():
    data = {
        'age': [22, 34, 45, 23, 55, 33, 25, 46, 28, 35],
        'account_length': [10, 35, 40, 20, 50, 30, 25, 45, 40, 32],
        'monthly_spend': [50, 60, 55, 40, 70, 60, 45, 80, 65, 50],
        'num_contacts': [3, 2, 1, 5, 4, 3, 4, 1, 2, 3],
        'churn': [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
    }
    return pd.DataFrame(data)

def preprocess_data(df):
    X = df.drop('churn', axis=1)
    y = df['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, X.columns

def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, feature_names):
    y_pred = model.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Churn', 'Churn'], yticklabels=['No Churn', 'Churn'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()
    importances = model.feature_importances_
    feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance, palette='viridis')
    plt.title('Feature Importance')
    plt.show()

if _name_ == "_main_":
    print("Loading data...")
    df = load_data()
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\nPreprocessing data...")
    X_train, X_test, y_train, y_test, feature_names = preprocess_data(df)
    print("\nTraining model...")
    model = train_model(X_train, y_train)
    print("\nEvaluating model...")
    evaluate_model(model, X_test, y_test, feature_names)