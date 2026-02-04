"""
STEP 1: CREATE RISK LEVEL (Rule-Based + ML Model)
This is the CORE of the project - everything else depends on this.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("RISK LEVEL CREATION & ML MODEL TRAINING")
print("="*60)

# 1️⃣ Load master dataset
print("\n[1/6] Loading master dataset...")
df = pd.read_csv('master_indian_weather_dataset.csv')
print(f"✓ Loaded {len(df):,} records")

# 2️⃣ CREATE RISK LEVEL (Rule-Based - EXPLAINABLE)
print("\n[2/6] Creating rule-based risk_level...")
print("\nRisk Classification Rules:")
print("─" * 50)

def calculate_risk_level(row):
    """
    Rule-based risk classification (explainable for judges/users)
    
    HIGH RISK if ANY:
    - Temperature extremes (>40°C or <15°C)
    - Heavy rainfall (>50mm)
    - Very high humidity with high temp (>85% AND >35°C)
    - Strong winds (>25 km/h)
    
    MODERATE RISK if ANY:
    - Moderate temp extremes (38-40°C or 15-20°C)
    - Moderate rainfall (20-50mm)
    - High humidity (75-85%)
    - Moderate winds (15-25 km/h)
    
    LOW RISK:
    - Normal conditions
    """
    
    temp_max = row['max_temperature']
    temp_min = row['min_temperature']
    temp_avg = row['avg_temperature']
    humidity = row['humidity']
    rainfall = row['rainfall']
    wind = row['wind_speed']
    temp_range = row['temp_range']
    
    # HIGH RISK CONDITIONS
    if (temp_max > 40 or temp_min < 15 or 
        rainfall > 50 or 
        (humidity > 85 and temp_avg > 35) or
        wind > 25 or
        temp_range > 13):
        return 'High'
    
    # MODERATE RISK CONDITIONS
    elif (temp_max > 38 or temp_min < 20 or
          rainfall > 20 or
          humidity > 75 or
          wind > 15 or
          temp_range > 11):
        return 'Moderate'
    
    # LOW RISK (Normal conditions)
    else:
        return 'Low'

# Apply risk classification
df['risk_level'] = df.apply(calculate_risk_level, axis=1)

# Show distribution
print("\n✓ Risk Level Distribution:")
print(df['risk_level'].value_counts())
print(f"\nPercentages:")
print(df['risk_level'].value_counts(normalize=True).mul(100).round(2))

# 3️⃣ Prepare features for ML
print("\n[3/6] Preparing features for ML training...")

# Select numeric features (9 features)
feature_columns = [
    'max_temperature',
    'min_temperature', 
    'avg_temperature',
    'temp_range',
    'humidity',
    'rainfall',
    'wind_speed'
]

X = df[feature_columns]
y = df['risk_level']

print(f"✓ Features: {len(feature_columns)} numeric columns")
print(f"✓ Target: risk_level (3 classes)")

# 4️⃣ Train-Test Split
print("\n[4/6] Splitting data (80% train, 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Maintain class distribution
)

print(f"✓ Training set: {len(X_train):,} samples")
print(f"✓ Test set: {len(X_test):,} samples")

# 5️⃣ Train RandomForest Model
print("\n[5/6] Training RandomForest Classifier...")
print("Model configuration:")
print("  - Algorithm: Random Forest")
print("  - Trees: 100")
print("  - Max depth: 10")
print("  - Random state: 42")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)

model.fit(X_train, y_train)
print("✓ Model trained successfully!")

# 6️⃣ Model Evaluation
print("\n[6/6] Evaluating model performance...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*60}")
print(f"MODEL PERFORMANCE")
print(f"{'='*60}")
print(f"\nAccuracy: {accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature Importance
print("\nTop Feature Importance:")
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance)

# 7️⃣ Save everything for FastAPI
print(f"\n{'='*60}")
print("SAVING OUTPUTS")
print(f"{'='*60}")

# Save updated dataset with risk_level
output_dataset = 'master_indian_weather_dataset.csv'
df.to_csv(output_dataset, index=False)
print(f"\n✓ Dataset with risk_level saved: {output_dataset}")

# Save ML model
model_file = 'weather_risk_model.pkl'
joblib.dump(model, model_file)
print(f"✓ ML model saved: {model_file}")

# Save feature names (for API use)
feature_info = {
    'features': feature_columns,
    'classes': list(model.classes_)
}
joblib.dump(feature_info, 'model_features.pkl')
print(f"✓ Feature info saved: model_features.pkl")

# Test prediction with sample data
print(f"\n{'='*60}")
print("TESTING PREDICTION (Sample)")
print(f"{'='*60}")

sample = X_test.iloc[0:1]
prediction = model.predict(sample)
probability = model.predict_proba(sample)

print(f"\nSample Input:")
print(sample.to_dict('records')[0])
print(f"\nPredicted Risk: {prediction[0]}")
print(f"Probabilities: Low={probability[0][0]:.2%}, Moderate={probability[0][1]:.2%}, High={probability[0][2]:.2%}")

print(f"\n{'='*60}")
print("✅ SUCCESS! Core components ready:")
print(f"{'='*60}")
print("1. ✓ Risk level created (rule-based, explainable)")
print("2. ✓ ML model trained (RandomForest)")
print("3. ✓ Model saved for FastAPI")
print("\nNext: Build FastAPI backend + UI")
print(f"{'='*60}")
