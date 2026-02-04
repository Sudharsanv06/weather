# Extreme Weather Early Warning System - Frontend

## 🎯 Dashboard Features
- Real-time weather data visualization
- AI-powered risk assessment (99.56% accuracy)
- Interactive location and date selection
- Dynamic charts for temperature and rainfall trends
- Color-coded risk alerts

## 🚀 How to Run

### Option 1: VS Code Live Server (Recommended)
1. Install **Live Server** extension in VS Code
2. Right-click `index.html`
3. Select **"Open with Live Server"**
4. Dashboard opens at `http://127.0.0.1:5500/frontend/`

### Option 2: Python HTTP Server
```bash
cd frontend
python -m http.server 8000
```
Then open: `http://localhost:8000`

### Option 3: Node.js HTTP Server
```bash
cd frontend
npx http-server -p 8000
```
Then open: `http://localhost:8000`

## 📊 Dataset
- **7,882 records** from 547 Indian cities
- Date range: Aug 2023 - Dec 2025
- 11 features including AI risk classification

## 🎨 Tech Stack
- Pure HTML, CSS, JavaScript
- Chart.js for visualizations
- Papa Parse for CSV parsing
- No backend required for demo

## 🌟 Risk Levels
- 🟢 **Low**: Normal weather conditions
- 🟡 **Moderate**: Monitor closely
- 🔴 **High**: Severe weather risk
