let weatherData = [];
let tempChart, rainChart;

// Load CSV data on page load
Papa.parse("master_indian_weather_dataset.csv", {
  download: true,
  header: true,
  complete: function(results) {
    weatherData = results.data.filter(row => row.location && row.date); // Filter out empty rows
    console.log(`✓ Loaded ${weatherData.length} weather records`);
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

  // Find matching row
  const row = weatherData.find(d => d.location === location && d.date === date);
  
  if (!row) {
    alert(`No data available for ${location} on ${date}`);
    return;
  }

  // Update weather cards
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
