"""
NEAR-FUTURE RISK FORECASTING
Uses recent historical data + trained ML model to predict future risk levels
"""

import pandas as pd
import joblib
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load dataset
print("Loading dataset...")
df = pd.read_csv("../master_indian_weather_dataset.csv")
df["date"] = pd.to_datetime(df["date"])
print(f"✓ Loaded {len(df):,} records")

# Load trained ML model
print("\nLoading ML model...")
model = joblib.load("../weather_risk_model.pkl")
feature_info = joblib.load("../model_features.pkl")
features = feature_info['features']
print(f"✓ Model loaded with {len(features)} features")

def get_recent_data(location, days=7):
    """
    Get most recent N days of data for a location
    """
    city_data = df[df["location"] == location].sort_values("date")
    if len(city_data) == 0:
        return None
    return city_data.tail(days)

def estimate_future_conditions(recent_df):
    """
    Estimate future weather conditions based on recent historical averages
    This is a statistical baseline forecasting method
    """
    estimated = {}
    
    # Calculate rolling averages from recent data
    estimated["max_temperature"] = recent_df["max_temperature"].mean()
    estimated["min_temperature"] = recent_df["min_temperature"].mean()
    estimated["avg_temperature"] = recent_df["avg_temperature"].mean()
    estimated["temp_range"] = estimated["max_temperature"] - estimated["min_temperature"]
    estimated["humidity"] = recent_df["humidity"].mean()
    estimated["rainfall"] = recent_df["rainfall"].mean()
    estimated["wind_speed"] = recent_df["wind_speed"].mean()
    
    return pd.DataFrame([estimated])

def predict_future_risk(location, days_lookback=7):
    """
    Predict future risk level for a location based on recent trends
    
    Returns:
        predicted_risk (str): 'Low', 'Moderate', or 'High'
        confidence (float): Model confidence (0-1)
        estimated_conditions (dict): Estimated future weather conditions
    """
    # Get recent data
    recent_data = get_recent_data(location, days=days_lookback)
    
    if recent_data is None or len(recent_data) == 0:
        return None, None, None
    
    # Estimate future conditions
    future_features_df = estimate_future_conditions(recent_data)
    
    # Ensure features are in correct order
    future_features_df = future_features_df[features]
    
    # Predict risk level
    predicted_risk = model.predict(future_features_df)[0]
    
    # Get confidence (probability of predicted class)
    probabilities = model.predict_proba(future_features_df)[0]
    confidence = max(probabilities)
    
    # Get all probabilities for each class
    class_names = model.classes_
    risk_probabilities = dict(zip(class_names, probabilities))
    
    # Get estimated conditions as dict
    estimated_conditions = future_features_df.iloc[0].to_dict()
    
    return predicted_risk, round(confidence, 2), estimated_conditions, risk_probabilities

def predict_multi_day_forecast(location, forecast_days=[3, 7]):
    """
    Generate forecast for multiple time horizons
    """
    forecasts = {}
    
    for days in forecast_days:
        risk, conf, conditions, probs = predict_future_risk(location, days_lookback=days)
        forecasts[f"next_{days}_days"] = {
            "risk_level": risk,
            "confidence": conf,
            "estimated_conditions": conditions,
            "probabilities": probs
        }
    
    return forecasts

# Test the forecasting
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING NEAR-FUTURE RISK FORECASTING")
    print("="*60)
    
    # Test with multiple cities
    test_cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai"]
    
    for city in test_cities:
        print(f"\n{'─'*60}")
        print(f"Location: {city}")
        print(f"{'─'*60}")
        
        # Single forecast
        risk, confidence, conditions, probs = predict_future_risk(city)
        
        if risk:
            print(f"\n🔮 Predicted Future Risk: {risk}")
            print(f"📊 Confidence: {confidence * 100:.1f}%")
            
            print(f"\n📈 Estimated Future Conditions:")
            print(f"  Max Temp: {conditions['max_temperature']:.1f}°C")
            print(f"  Min Temp: {conditions['min_temperature']:.1f}°C")
            print(f"  Avg Temp: {conditions['avg_temperature']:.1f}°C")
            print(f"  Humidity: {conditions['humidity']:.1f}%")
            print(f"  Rainfall: {conditions['rainfall']:.1f}mm")
            print(f"  Wind Speed: {conditions['wind_speed']:.1f}km/h")
            
            print(f"\n🎯 Risk Probabilities:")
            for risk_class, prob in probs.items():
                print(f"  {risk_class}: {prob*100:.1f}%")
        else:
            print(f"❌ No data available for {city}")
    
    # Multi-day forecast example
    print(f"\n\n{'='*60}")
    print("MULTI-DAY FORECAST EXAMPLE (Mumbai)")
    print(f"{'='*60}")
    
    forecasts = predict_multi_day_forecast("Mumbai", forecast_days=[3, 7])
    
    for period, forecast in forecasts.items():
        print(f"\n{period.replace('_', ' ').title()}:")
        print(f"  Risk: {forecast['risk_level']}")
        print(f"  Confidence: {forecast['confidence'] * 100:.1f}%")
    
    print("\n" + "="*60)
    print("✅ FORECASTING MODULE READY")
    print("="*60)
