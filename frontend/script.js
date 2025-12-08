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

function formatNumber(value) {
    if (value === null || value === undefined) return "-";

    const abs = Math.abs(value);

    if (abs >= 1_000_000_000)
        return (value / 1_000_000_000).toFixed(2) + "mrd";

    if (abs >= 1_000_000)
        return (value / 1_000_000).toFixed(2) + "m";

    if (abs >= 1_000)
        return (value / 1_000).toFixed(2) + "t";

    return value.toFixed(2);
}

async function loadData() {
    const s = document.getElementById("start").value;
    const e = document.getElementById("end").value;

    const r = await fetch(`http://localhost:8000/analyze?start=${s}&end=${e}`);
    const d = await r.json();

    document.getElementById("statsBox").textContent =
        "Pisin laskutrendi: " + d.bearish.length + " päivää\n" +
        "Suurin volyymi: " + d.max_volume.date + " (" + formatNumber(d.max_volume.volume) + " EUR)\n" +
        "Paras osto/myynti: " + d.best_trade.buy + " → " + d.best_trade.sell +
        " (tuotto " + formatNumber(d.best_trade.profit) + " EUR)";

    const labels = d.candles.map(c => c.date);
    const prices = d.candles.map(c => Number(c.price.toFixed(2)));
    const volumes = d.candles.map(c => Number(c.volume.toFixed(2)));

    if (priceChart) priceChart.destroy();
    if (volumeChart) volumeChart.destroy();

    priceChart = new Chart(document.getElementById("priceChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Hinta (EUR)",
                data: prices
            }]
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            return formatNumber(ctx.raw) + " EUR";
                        }
                    }
                }
            }
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
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            return formatNumber(ctx.raw) + " EUR";
                        }
                    }
                }
            }
        }
    });
}
