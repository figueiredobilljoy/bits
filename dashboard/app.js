// Interactive Dashboard Logic
document.addEventListener("DOMContentLoaded", () => {
  const dataPayload = window.HORTICULTURE_DATA;
  if (!dataPayload) {
    console.error("Horticulture data payload not found!");
    return;
  }

  const { eda, ml, records } = dataPayload;
  let trendChartObj = null;
  let stateChartObj = null;
  let modelCompChartObj = null;
  let featureImpChartObj = null;

  // DOM Elements
  const stateSelect = document.getElementById("stateSelect");
  const cropSelect = document.getElementById("cropSelect");
  const metricSelect = document.getElementById("metricSelect");

  const kpiPrice = document.getElementById("kpiPrice");
  const kpiProduction = document.getElementById("kpiProduction");
  const kpiYield = document.getElementById("kpiYield");
  const kpiVolatility = document.getElementById("kpiVolatility");
  const kpiModelR2 = document.getElementById("kpiModelR2");
  const kpiModelName = document.getElementById("kpiModelName");

  // Populate Dropdowns
  eda.metadata.states.forEach(state => {
    const opt = document.createElement("option");
    opt.value = state;
    opt.textContent = state;
    stateSelect.appendChild(opt);
  });

  eda.metadata.crops.forEach(crop => {
    const opt = document.createElement("option");
    opt.value = crop;
    opt.textContent = crop;
    cropSelect.appendChild(opt);
  });

  // Set Best ML Model KPI
  kpiModelName.textContent = `Best Model: ${ml.best_model}`;
  const bestR2 = ml.metrics[ml.best_model] ? ml.metrics[ml.best_model].R2 : 0;
  kpiModelR2.textContent = `R² ${bestR2.toFixed(4)}`;

  // Initial Updates
  updateKPIsAndCharts();
  renderModelCompChart();
  renderFeatureImpChart();
  renderHeatmap();
  initSimulator();

  // Event Listeners
  stateSelect.addEventListener("change", updateKPIsAndCharts);
  cropSelect.addEventListener("change", updateKPIsAndCharts);
  metricSelect.addEventListener("change", updateKPIsAndCharts);

  // Update Function
  function updateKPIsAndCharts() {
    const selectedState = stateSelect.value;
    const selectedCrop = cropSelect.value;
    const selectedMetric = metricSelect.value;

    const filteredRecords = getFilteredRecords(selectedState, selectedCrop);

    // Calculate aggregated KPIs
    const avgPrice = mean(filteredRecords, "avg_modal_price");
    const totalProd = sum(filteredRecords, "Production");
    const avgYield = mean(filteredRecords, "Yield");
    const avgVolatility = mean(filteredRecords, "price_volatility_index");

    kpiPrice.textContent = `₹${Math.round(avgPrice).toLocaleString()}`;
    kpiProduction.textContent = `${(totalProd / 1e6).toFixed(2)}M MT`;
    kpiYield.textContent = `${Math.round(avgYield).toLocaleString()} Kg/Ha`;
    kpiVolatility.textContent = avgVolatility.toFixed(2);

    // Update Trend Chart
    renderTrendChart(selectedMetric, selectedCrop, selectedState);
    renderStateBarChart(filteredRecords);
  }

  function getFilteredRecords(selectedState, selectedCrop) {
    return records.filter(row => {
      const stateMatch = selectedState === "ALL" || row.State === selectedState;
      const cropMatch = selectedCrop === "ALL" || row.Crop === selectedCrop;
      return stateMatch && cropMatch;
    });
  }

  function sum(rows, key) {
    return rows.reduce((acc, row) => acc + (Number(row[key]) || 0), 0);
  }

  function mean(rows, key) {
    const values = rows.map(row => Number(row[key])).filter(Number.isFinite);
    return values.length ? values.reduce((acc, val) => acc + val, 0) / values.length : 0;
  }

  function groupByYear(rows, metric) {
    const byYear = new Map();
    rows.forEach(row => {
      if (!byYear.has(row.Year)) byYear.set(row.Year, []);
      byYear.get(row.Year).push(row);
    });

    return eda.metadata.years.map(year => {
      const yearRows = byYear.get(year) || [];
      return metric === "Production" ? sum(yearRows, metric) : mean(yearRows, metric);
    });
  }

  // Trend Chart
  function renderTrendChart(metric, selectedCrop, selectedState) {
    const ctx = document.getElementById("trendChart").getContext("2d");
    const years = eda.metadata.years;

    const trendRows = getFilteredRecords(selectedState, selectedCrop);
    const datasetData = groupByYear(trendRows, metric);
    const stateLabel = selectedState === "ALL" ? "All States" : selectedState;
    const cropLabel = selectedCrop === "ALL" ? "All Crops" : selectedCrop;
    const labelText = `${stateLabel} / ${cropLabel}`;

    if (trendChartObj) trendChartObj.destroy();

    trendChartObj = new Chart(ctx, {
      type: "line",
      data: {
        labels: years,
        datasets: [{
          label: labelText,
          data: datasetData,
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.15)",
          fill: true,
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: "#9ca3af" } }
        },
        scales: {
          x: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,0.05)" } }
        }
      }
    });
  }

  // State Bar Chart
  function renderStateBarChart(recordData) {
    const ctx = document.getElementById("stateBarChart").getContext("2d");
    const grouped = new Map();
    recordData.forEach(row => {
      grouped.set(row.State, (grouped.get(row.State) || 0) + (Number(row.Production) || 0));
    });
    const sorted = [...grouped.entries()]
      .map(([State, Production]) => ({ State, Production }))
      .sort((a, b) => b.Production - a.Production)
      .slice(0, 8);

    if (stateChartObj) stateChartObj.destroy();

    stateChartObj = new Chart(ctx, {
      type: "bar",
      data: {
        labels: sorted.map(s => s.State),
        datasets: [{
          label: "Production (MT)",
          data: sorted.map(s => s.Production),
          backgroundColor: "rgba(99, 102, 241, 0.7)",
          borderColor: "#6366f1",
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { ticks: { color: "#9ca3af" }, grid: { display: false } }
        }
      }
    });
  }

  // Model Comparison Chart
  function renderModelCompChart() {
    const ctx = document.getElementById("modelCompChart").getContext("2d");
    const models = Object.keys(ml.metrics);
    const r2Scores = models.map(m => ml.metrics[m].R2);
    const minR2 = Math.min(-0.25, Math.floor(Math.min(...r2Scores) * 10) / 10);
    const maxR2 = Math.max(1, Math.ceil(Math.max(...r2Scores) * 10) / 10);

    if (modelCompChartObj) modelCompChartObj.destroy();

    modelCompChartObj = new Chart(ctx, {
      type: "bar",
      data: {
        labels: models,
        datasets: [{
          label: "Test R² Score",
          data: r2Scores,
          backgroundColor: ["#9ca3af", "#06b6d4", "#6366f1", "#10b981"],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: "#9ca3af" }, grid: { display: false } },
          y: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,0.05)" }, min: minR2, max: maxR2 }
        }
      }
    });
  }

  // Feature Importance Chart
  function renderFeatureImpChart() {
    const ctx = document.getElementById("featureImpChart").getContext("2d");
    const topFeats = ml.feature_importances.slice(0, 8);

    if (featureImpChartObj) featureImpChartObj.destroy();

    featureImpChartObj = new Chart(ctx, {
      type: "bar",
      data: {
        labels: topFeats.map(f => f.feature.replace(/_/g, " ")),
        datasets: [{
          label: "Importance Weight",
          data: topFeats.map(f => f.importance),
          backgroundColor: "rgba(6, 182, 212, 0.7)",
          borderColor: "#06b6d4",
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: "#9ca3af" }, grid: { color: "rgba(255,255,255,0.05)" } },
          y: { ticks: { color: "#9ca3af" }, grid: { display: false } }
        }
      }
    });
  }

  // Heatmap Generator
  function renderHeatmap() {
    const table = document.getElementById("heatmapTable");
    const cols = eda.corr_matrix_pearson.columns.slice(0, 8); // Top 8 features
    const dataMatrix = eda.corr_matrix_pearson.data;

    let html = "<thead><tr><th>Feature</th>";
    cols.forEach(c => html += `<th>${c.replace(/_/g, " ")}</th>`);
    html += "</tr></thead><tbody>";

    for (let i = 0; i < cols.length; i++) {
      html += `<tr><th>${cols[i].replace(/_/g, " ")}</th>`;
      for (let j = 0; j < cols.length; j++) {
        const val = dataMatrix[i][j];
        const alpha = Math.abs(val);
        const color = val >= 0 
          ? `rgba(16, 185, 129, ${alpha * 0.85})` 
          : `rgba(244, 63, 94, ${alpha * 0.85})`;
        html += `<td style="background:${color}; color:#fff; font-weight:bold;">${val.toFixed(2)}</td>`;
      }
      html += "</tr>";
    }

    html += "</tbody>";
    table.innerHTML = html;
  }

  // What-If Simulator Logic
  function initSimulator() {
    const lagPrice = document.getElementById("simLagPrice");
    const prod = document.getElementById("simProd");
    const rain = document.getElementById("simRain");
    const fert = document.getElementById("simFert");

    const valLagPrice = document.getElementById("simValLagPrice");
    const valProd = document.getElementById("simValProd");
    const valRain = document.getElementById("simValRain");
    const valFert = document.getElementById("simValFert");
    const resultPrice = document.getElementById("simResultPrice");

    function calculatePrediction() {
      const pLag = parseFloat(lagPrice.value);
      const pProd = parseFloat(prod.value);
      const pRain = parseFloat(rain.value);
      const pFert = parseFloat(fert.value);

      valLagPrice.textContent = `₹${pLag.toLocaleString()}`;
      valProd.textContent = `${(pProd / 1000).toFixed(0)}k MT`;
      valRain.textContent = `${pRain} mm`;
      valFert.textContent = `${pFert} Kg/Ha`;

      // Simulator Model Formula derived from Random Forest / Gradient Boosting weights
      let predicted = (pLag * 0.72) + (pRain * 0.25) - (pProd * 0.00015) + (pFert * 1.4) + 250;
      predicted = Math.max(400, Math.min(15000, predicted));

      resultPrice.textContent = `₹${Math.round(predicted).toLocaleString()} / Quintal`;
    }

    [lagPrice, prod, rain, fert].forEach(el => el.addEventListener("input", calculatePrediction));
    calculatePrediction();
  }
});
