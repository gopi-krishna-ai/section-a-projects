js_content = '''document.addEventListener('DOMContentLoaded', () => {
    
    let chartInstance = null;

    // Load Stats
    function loadStats() {
        fetch('/api/stats')
            .then(res => res.json())
            .then(data => {
                document.getElementById('stat-total').innerText = data.total_analyzed;
                document.getElementById('stat-disaster').innerText = data.total_disasters;
                document.getElementById('stat-incidents').innerText = data.active_incidents;
                document.getElementById('stat-false').innerText = data.false_alarms;

                updateChart(data.total_disasters, data.total_analyzed - data.total_disasters);
            })
            .catch(err => console.error("Error loading stats:", err));
    }

    // Chart.js
    function updateChart(disasters, safe) {
        const ctx = document.getElementById('disasterChart');
        if (!ctx) return;
        
        if (chartInstance) {
            chartInstance.data.datasets[0].data = [disasters, safe];
            chartInstance.update();
        } else {
            chartInstance = new Chart(ctx.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['Disaster', 'Non-Disaster'],
                    datasets: [{
                        data: [disasters, safe],
                        backgroundColor: ['#dc3545', '#198754'],
                        borderWidth: 0
                    }]
                },
                options: {
                    plugins: { legend: { labels: { color: 'white' } } }
                }
            });
        }
    }

    // Analyze Custom Tweet
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            const tweet = document.getElementById('tweetInput').value;
            if(!tweet) return;

            fetch('/api/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({tweet: tweet})
            })
            .then(res => res.json())
            .then(data => {
                if(data.error) {
                    alert(data.error);
                    return;
                }
                const box = document.getElementById('resultBox');
                const txt = document.getElementById('resultText');
                box.style.display = 'block';
                
                if(data.prediction === 'Disaster') {
                    box.className = 'mt-3 p-3 rounded bg-danger text-white';
                    txt.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> DISASTER ALERT (Confidence: ' + data.confidence + '%)';
                    addLiveFeedRow(tweet, 'Disaster');
                } else {
                    box.className = 'mt-3 p-3 rounded bg-success text-white';
                    txt.innerHTML = '<i class="fa-solid fa-check"></i> NORMAL / NOT DISASTER';
                    addLiveFeedRow(tweet, 'Not Disaster');
                }
                loadStats();
            })
            .catch(err => console.error("Error predicting:", err));
        });
    }

    // Mock Live Feed Simulation
    function addLiveFeedRow(text, classification) {
        const tbody = document.getElementById('liveFeedTable');
        if (!tbody) return;
        
        const tr = document.createElement('tr');
        
        let badge = classification === 'Disaster' 
            ? '<span class="badge bg-danger">Disaster</span>'
            : '<span class="badge bg-success">Normal</span>';

        tr.innerHTML = '<td>' + text + '</td><td>' + badge + '</td>';
        
        tbody.prepend(tr);
        if(tbody.children.length > 5) {
            tbody.removeChild(tbody.lastChild);
        }
    }

    // Initial Load
    loadStats();
    addLiveFeedRow("Just had a great coffee at the new cafe down the street!", "Not Disaster");
    addLiveFeedRow("Massive flooding reported in the downtown area. Send rescue teams!", "Disaster");
});
'''

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
