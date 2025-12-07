let priceChart;
let volumeChart;

document.getElementById("fetchBtn").onclick = loadData;
document.getElementById("themeToggle").onclick = toggleTheme;

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}

function toggleTheme() {
    document.body.classList.toggle("dark");
    localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
}

async function loadData() {
    const s = document.getElementById("start").value;
    const e = document.getElementById("end").value;

    const r = await fetch(`http://localhost:8000/analyze?start=${s}&end=${e}`);
    const d = await r.json();

    document.getElementById("statsBox").textContent =
        "Pisin laskutrendi: " + d.bearish.length + " päivää\n" +
        "Suurin volyymi: " + d.max_volume.date + " (" + d.max_volume.volume + ")\n" +
        "Paras osto/myynti: " + d.best_trade.buy + " → " + d.best_trade.sell +
        " (tuotto " + d.best_trade.profit + ")";

    const labels = d.candles.map(c => c.date);
    const prices = d.candles.map(c => c.price);
    const volumes = d.candles.map(c => c.volume);

    if (priceChart) priceChart.destroy();
    if (volumeChart) volumeChart.destroy();

    priceChart = new Chart(document.getElementById("priceChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Hinta (EUR)",
                data: prices
            }]
        }
    });

    volumeChart = new Chart(document.getElementById("volumeChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Volyymi (EUR)",
                data: volumes
            }]
        }
    });
}
