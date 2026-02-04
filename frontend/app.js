let weatherData = [];
let tempChart, rainChart;

// Define TODAY as reference point for forecasting
const TODAY = new Date("2026-02-04"); // For demo - use new Date() for production
const FORECAST_DAYS_LIMIT = 7;

// Load CSV data on page load
Papa.parse("master_indian_weather_dataset.csv", {
  download: true,
  header: true,
  complete: function(results) {
    weatherData = results.data.filter(row => row.location && row.date); // Filter out empty rows
    console.log(`✓ Loaded ${weatherData.length} weather records`);
    console.log(`✓ Today's date: ${TODAY.toISOString().split('T')[0]}`);
    console.log(`✓ Forecast window: ${TODAY.toISOString().split('T')[0]} to ${new Date(TODAY.getTime() + FORECAST_DAYS_LIMIT * 24*60*60*1000).toISOString().split('T')[0]}`);
    populateControls();
  },
  error: function(error) {
    console.error("Error loading CSV:", error);
    alert("Failed to load weather data. Make sure the CSV file is in the frontend folder.");
  }
});

function populateControls() {
  // Get unique locations
  const locations = [...new Set(weatherData.map(d => d.location))].sort();
  const locationSelect = document.getElementById("locationSelect");

  locations.forEach(loc => {
    const option = document.createElement("option");
    option.value = loc;
    option.textContent = loc;
    locationSelect.appendChild(option);
  });

  // Set default date to today or first available date
  const dateSelect = document.getElementById("dateSelect");
  if (weatherData.length > 0) {
    // Set to first date in dataset
    dateSelect.value = weatherData[0].date;
  }

  console.log(`✓ Populated ${locations.length} locations`);
}

function updateDashboard() {
  const location = document.getElementById("locationSelect").value;
  const date = document.getElementById("dateSelect").value;

  if (!location) {
    alert("Please select a location");
    return;
  }

  if (!date) {
    alert("Please select a date");
    return;
  }

  // Calculate days from TODAY (not from latest dataset date)
  const selectedDate = new Date(date);
  const diffTime = selectedDate - TODAY;
  const daysFromToday = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  console.log(`Selected: ${date}, Days from today: ${daysFromToday}`);

  // 1️⃣ PAST DATES → Historical data
  if (daysFromToday < 0) {
    const row = weatherData.find(d => d.location === location && d.date === date);
    
    if (!row) {
      alert(`No historical data available for ${location} on ${date}`);
      return;
    }
    
    showHistoricalData(row);
    return;
  }

  // 2️⃣ TODAY + NEXT 7 DAYS → Forecast
  if (daysFromToday >= 0 && daysFromToday <= FORECAST_DAYS_LIMIT) {
    showFutureForecast(location, daysFromToday);
    return;
  }

  // 3️⃣ BEYOND 7 DAYS → Not available
  if (daysFromToday > FORECAST_DAYS_LIMIT) {
    showForecastUnavailable(daysFromToday);
    return;
  }
}

function showHistoricalData(row) {
  // Update weather cards with historical data
  document.getElementById("maxTemp").textContent = parseFloat(row.max_temperature).toFixed(1);
  document.getElementById("rainfall").textContent = parseFloat(row.rainfall).toFixed(1);
  document.getElementById("humidity").textContent = parseFloat(row.humidity).toFixed(1);
  document.getElementById("wind").textContent = parseFloat(row.wind_speed).toFixed(1);

  // Update risk level
  const riskBox = document.getElementById("riskBox");
  const riskLevel = row.risk_level.toLowerCase();
  riskBox.className = `risk ${riskLevel}`;

  document.getElementById("riskLevel").textContent = row.risk_level;
  
  // Set alert text based on risk level
  const alertMessages = {
    high: "⚠️ SEVERE WEATHER RISK DETECTED! Take immediate precautions.",
    moderate: "⚠️ Monitor weather conditions closely. Stay prepared.",
    low: "✅ Weather conditions are normal. No action required."
  };
  
  document.getElementById("alertText").textContent = alertMessages[riskLevel] || "Data available";

  // Render charts for this location
  renderCharts(location);
}

function renderCharts(location) {
  // Get all data for this location
  const locationData = weatherData
    .filter(d => d.location === location)
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(0, 30); // Limit to 30 most recent records for clarity

  if (locationData.length === 0) {
    console.warn("No data for charts");
    return;
  }

  const dates = locationData.map(d => d.date);
  const temps = locationData.map(d => parseFloat(d.avg_temperature));
  const rains = locationData.map(d => parseFloat(d.rainfall));

  // Destroy existing charts
  if (tempChart) tempChart.destroy();
  if (rainChart) rainChart.destroy();

  // Temperature Chart
  tempChart = new Chart(document.getElementById("tempChart"), {
    type: "line",
    data: {
      labels: dates,
      datasets: [{
        label: "Avg Temperature (°C)",
        data: temps,
        borderColor: "#06b6d4",
        backgroundColor: "rgba(6, 182, 212, 0.1)",
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          labels: { color: "#e5e7eb" }
        }
      },
      scales: {
        x: { 
          ticks: { 
            color: "#94a3b8",
            maxRotation: 45,
            minRotation: 45
          },
          grid: { color: "#334155" }
        },
        y: { 
          ticks: { color: "#94a3b8" },
          grid: { color: "#334155" }
        }
      }
    }
  });

  // Rainfall Chart
  rainChart = new Chart(document.getElementById("rainChart"), {
    type: "bar",
    data: {
      labels: dates,
      datasets: [{
        label: "Rainfall (mm)",
        data: rains,
        backgroundColor: "#2563eb",
        borderColor: "#1e40af",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          labels: { color: "#e5e7eb" }
        }
      },
      scales: {
        x: { 
          ticks: { 
            color: "#94a3b8",
            maxRotation: 45,
            minRotation: 45
          },
          grid: { color: "#334155" }
        },
        y: { 
          ticks: { color: "#94a3b8" },
          grid: { color: "#334155" }
        }
      }
    }
  });
}

function showFutureForecast(location, daysFromToday) {
  /**
   * Forecast mode for future dates within the forecast window (Feb 4-11)
   * Uses near-future risk forecasting based on recent trends
   */
  
  // Get recent data for this location to estimate future conditions
  const locationData = weatherData
    .filter(d => d.location === location)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 7); // Last 7 days

  if (locationData.length === 0) {
    alert(`No historical data available for ${location} to generate forecast`);
    return;
  }

  // Calculate estimated future conditions (rolling averages)
  const avgMaxTemp = locationData.reduce((sum, d) => sum + parseFloat(d.max_temperature), 0) / locationData.length;
  const avgMinTemp = locationData.reduce((sum, d) => sum + parseFloat(d.min_temperature), 0) / locationData.length;
  const avgHumidity = locationData.reduce((sum, d) => sum + parseFloat(d.humidity), 0) / locationData.length;
  const avgRainfall = locationData.reduce((sum, d) => sum + parseFloat(d.rainfall), 0) / locationData.length;
  const avgWind = locationData.reduce((sum, d) => sum + parseFloat(d.wind_speed), 0) / locationData.length;
  const avgTemp = (avgMaxTemp + avgMinTemp) / 2;
  const tempRange = avgMaxTemp - avgMinTemp;

  // Simple rule-based risk estimation (matches backend logic)
  let forecastedRisk = "Low";
  if (avgMaxTemp > 40 || avgMinTemp < 15 || avgRainfall > 50 || avgHumidity > 85 || avgWind > 25 || tempRange > 13) {
    forecastedRisk = "High";
  } else if (avgMaxTemp > 38 || avgMinTemp < 20 || avgRainfall > 20 || avgHumidity > 75 || avgWind > 15 || tempRange > 11) {
    forecastedRisk = "Moderate";
  }

  // Update weather cards with forecasted values (using ≈ symbol to indicate approximation)
  document.getElementById("maxTemp").textContent = `≈ ${avgMaxTemp.toFixed(1)}`;
  document.getElementById("rainfall").textContent = `≈ ${avgRainfall.toFixed(1)}`;
  document.getElementById("humidity").textContent = `≈ ${avgHumidity.toFixed(1)}`;
  document.getElementById("wind").textContent = `≈ ${avgWind.toFixed(1)}`;

  // Update risk level
  const riskBox = document.getElementById("riskBox");
  const riskLevel = forecastedRisk.toLowerCase();
  riskBox.className = `risk ${riskLevel}`;

  document.getElementById("riskLevel").textContent = `${forecastedRisk} (Forecasted)`;
  
  // Set forecast alert text - special handling for "today"
  const timeframe = daysFromToday === 0 ? "today" : `next ${daysFromToday} day(s)`;
  const forecastEnd = new Date(TODAY.getTime() + FORECAST_DAYS_LIMIT * 24*60*60*1000);
  const windowText = `(${TODAY.toISOString().split('T')[0]} – ${forecastEnd.toISOString().split('T')[0]} window)`;
  
  const alertMessages = {
    high: `🔮 FORECASTED: Severe weather risk predicted for ${timeframe}. Based on recent climate trends ${windowText}`,
    moderate: `🔮 FORECASTED: Moderate risk conditions expected for ${timeframe}. Based on recent trends ${windowText}`,
    low: `🔮 FORECASTED: Normal weather conditions expected for ${timeframe}. Based on recent patterns ${windowText}`
  };
  
  document.getElementById("alertText").textContent = alertMessages[riskLevel];

  // Render charts with recent historical data
  renderCharts(location);
  
  console.log(`✓ Forecast mode activated for ${location} (${daysFromToday} days from today)`);
}

function showForecastUnavailable(daysFromToday) {
  /**
   * Display message when forecast is beyond the 7-day window
   */
  
  // Clear all weather cards
  document.getElementById("maxTemp").textContent = "--";
  document.getElementById("rainfall").textContent = "--";
  document.getElementById("humidity").textContent = "--";
  document.getElementById("wind").textContent = "--";

  // Update risk box
  const riskBox = document.getElementById("riskBox");
  riskBox.className = "risk";

  document.getElementById("riskLevel").textContent = "Unavailable";

  const forecastEnd = new Date(TODAY.getTime() + FORECAST_DAYS_LIMIT * 24*60*60*1000);
  const windowText = `${TODAY.toISOString().split('T')[0]} – ${forecastEnd.toISOString().split('T')[0]}`;
  
  document.getElementById("alertText").textContent =
    `⚠️ Climate forecast is available only up to 7 days ahead (${windowText}). Selected date is ${daysFromToday} days ahead.`;
  
  console.log(`⚠️ Forecast unavailable: ${daysFromToday} days exceeds ${FORECAST_DAYS_LIMIT}-day window`);
}
