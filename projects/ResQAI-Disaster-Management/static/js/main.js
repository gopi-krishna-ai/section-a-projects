document.addEventListener('DOMContentLoaded', () => {
    
    let chartInstance = null;

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
                    plugins: { legend: { labels: { color: '#1e293b' } } }
                }
            });
        }
    }

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
                
                // Show XAI Explanation
                if (data.key_words) {
                    document.getElementById('xaiBox').style.display = 'block';
                    document.getElementById('xaiText').innerText = data.explanation;
                    
                    let tags = '';
                    if (data.key_words.length > 0) {
                        data.key_words.forEach(w => {
                            tags += '<span class="badge bg-secondary me-1">' + w + '</span>';
                        });
                    } else {
                        tags = '<span class="text-muted">None</span>';
                    }
                    document.getElementById('xaiTags').innerHTML = tags;
                }

                loadStats();
            })
            .catch(err => console.error("Error predicting:", err));
        });
    }

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

    loadStats();
});

