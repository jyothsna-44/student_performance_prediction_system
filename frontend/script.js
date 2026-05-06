let radarChart, barChart;

// Initial Load: Populate At-Risk List
window.onload = async () => {
    try {
        const res = await fetch("http://127.0.0.1:5000/at-risk");
        const data = await res.json();
        const container = document.getElementById("risk-list");
        container.innerHTML = data.map(s => `
            <div class="risk-item">
                <span class="risk-id">#ID-${s.id}</span>
                <span class="risk-val">Attend: ${s.attendance}%</span>
            </div>
        `).join("");
    } catch (e) { console.log("Init failed"); }
};

async function runAnalysis() {
    const inputs = {
        study: document.getElementById("study").value,
        attendance: document.getElementById("attendance").value,
        past: document.getElementById("past").value,
        assign: document.getElementById("assign").value,
        marks: document.getElementById("marks").value
    };

    // UI Feedback
    const btn = document.querySelector(".primary-btn");
    btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ANALYZING...`;

    try {
        const res = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(inputs)
        });

        const data = await res.json();
        
        // Update Banner
        const banner = document.getElementById("result-banner");
        banner.classList.remove("hidden");
        document.getElementById("result-label").innerText = data.result;
        document.getElementById("insight-text").innerText = data.insight;
        
        const badge = document.getElementById("badge-icon");
        badge.innerHTML = data.is_pass ? '<i class="fas fa-check-circle" style="color: #10b981"></i>' : '<i class="fas fa-times-circle" style="color: #ef4444"></i>';
        banner.style.borderColor = data.is_pass ? "#10b981" : "#ef4444";

        // Update Tags
        document.getElementById("similar-id-list").innerHTML = data.similar_ids.map(id => `
            <span class="id-tag">#ID-${id}</span>
        `).join("");

        // Success Celebration
        if(data.is_pass) confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });

        renderCharts(data.your_data, data.avg_data);

    } catch (e) {
        alert("Server connection failed.");
    } finally {
        btn.innerHTML = `<span>GENERATE ANALYSIS</span> <i class="fas fa-bolt"></i>`;
    }
}

function renderCharts(you, avg) {
    const ctxRadar = document.getElementById("radarChart");
    const ctxBar = document.getElementById("barChart");
    const labels = ["Study", "Attend", "Past", "Tasks", "Skills"];

    if (radarChart) radarChart.destroy();
    if (barChart) barChart.destroy();

    const chartStyle = {
        color: '#94a3b8',
        gridColor: 'rgba(255, 255, 255, 0.05)'
    };

    radarChart = new Chart(ctxRadar, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Candidate',
                data: you,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                pointBackgroundColor: '#6366f1'
            }]
        },
        options: {
            scales: {
                r: {
                    grid: { color: chartStyle.gridColor },
                    angleLines: { color: chartStyle.gridColor },
                    pointLabels: { color: chartStyle.color, font: { size: 10 } },
                    ticks: { display: false }
                }
            },
            plugins: { legend: { display: false } }
        }
    });

    barChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                { label: 'Candidate', data: you, backgroundColor: '#6366f1', borderRadius: 8 },
                { label: 'Industry Avg', data: avg, backgroundColor: 'rgba(255, 255, 255, 0.05)', borderRadius: 8 }
            ]
        },
        options: {
            scales: {
                y: { display: false },
                x: {
                    grid: { display: false },
                    ticks: { color: chartStyle.color }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}