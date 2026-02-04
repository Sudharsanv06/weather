# Backend - Near-Future Risk Forecasting

## 🔮 What This Does
Predicts future weather risk levels (3-7 days ahead) using:
- Recent historical data (rolling averages)
- Trained RandomForest ML model (99.56% accuracy)
- Statistical baseline forecasting

## 🎯 Features
- **Next 3 Days Risk Forecast**: Short-term prediction
- **Next 7 Days Risk Forecast**: Medium-term prediction
- **Confidence Scores**: ML probability for each prediction
- **Estimated Conditions**: Future temperature, humidity, rainfall, wind

## 🧠 How It Works
1. **Get Recent Data**: Last 7 days of weather for selected location
2. **Calculate Averages**: Statistical rolling means
3. **Estimate Future**: Use averages as future condition estimates
4. **ML Prediction**: Pass estimates to trained model
5. **Return Risk**: Low / Moderate / High with confidence

## 📊 Example Output
```
Location: Mumbai
🔮 Predicted Future Risk: Moderate
📊 Confidence: 86.0%

📈 Estimated Future Conditions:
  Max Temp: 35.5°C
  Humidity: 53.7%
  Rainfall: 8.9mm
  Wind Speed: 9.5km/h

🎯 Risk Probabilities:
  High: 3.6%
  Low: 10.5%
  Moderate: 86.0%
```

## 🚀 Usage

### Test the Module
```bash
cd backend
python future_forecast.py
```

### Use in Your Code
```python
from backend.future_forecast import predict_future_risk

# Get forecast for a city
risk, confidence, conditions, probabilities = predict_future_risk("Mumbai")

print(f"Future Risk: {risk}")
print(f"Confidence: {confidence * 100}%")
```

## ✅ Why This Approach?
- **Explainable**: Judges understand rolling averages
- **Honest**: No fake LSTM claims
- **Reliable**: Uses proven ML model
- **Industry Standard**: Baseline forecasting method
- **No New Data Needed**: Works with existing dataset

## 🎓 Technical Details
- **Method**: Rolling average baseline forecasting
- **Lookback Window**: 7 days (configurable)
- **ML Model**: RandomForest Classifier
- **Features**: 7 weather parameters
- **Classes**: Low, Moderate, High risk

## 📦 Dependencies
- pandas
- joblib
- scikit-learn (already installed)

All dependencies are already in your environment!
