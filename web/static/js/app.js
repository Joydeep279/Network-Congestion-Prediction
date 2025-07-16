document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predict-form");
    const resultDiv = document.getElementById("result");
    let predictionChart = null;

    // Custom plugin to draw text in the middle of the doughnut chart
    const centerTextPlugin = {
        id: 'centerText',
        afterDraw: (chart) => {
            if (chart.config.type !== 'doughnut' || chart.data.datasets.length === 0) {
                return;
            }
            const ctx = chart.ctx;
            const { width, height } = chart;
            const mainPrediction = chart.config.options.plugins.centerText.mainPrediction;

            ctx.save();
            ctx.font = 'bold 30px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = mainPrediction.isCongestion ? '#856404' : '#155724';
            const text = `${(mainPrediction.probability * 100).toFixed(1)}%`;
            ctx.fillText(text, width / 2, height / 2 - 15);
            
            ctx.font = '16px sans-serif';
            ctx.fillStyle = '#6c757d';
            const subText = mainPrediction.isCongestion ? 'Congestion' : 'Clear';
            ctx.fillText(subText, width / 2, height / 2 + 15);

            ctx.restore();
        }
    };
    Chart.register(centerTextPlugin);

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = "<span>Loading...</span>";

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = !isNaN(parseFloat(value)) && isFinite(value) ? Number(value) : value;
        });

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            resultDiv.innerHTML = '<div class="chart-container"><canvas id="predictionChart"></canvas></div>';
            
            if (result.error) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
            } else {
                renderPredictionResult(result);
            }

        } catch (err) {
            resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
        }
    });

    function renderPredictionResult(result) {
        const congestionText = result.congestion ? "Yes" : "No";
        const probability = result.probability;
        const probabilityFormatted = (probability * 100).toFixed(2);

        const textResultDiv = document.createElement('div');
        textResultDiv.className = `alert ${result.congestion ? 'alert-warning' : 'alert-success'} mt-3`;
        textResultDiv.innerHTML = `
            <h4 class="alert-heading">Prediction Results</h4>
            <p><b>Congestion Status:</b> ${congestionText}</p>
            <p><b>Confidence:</b> ${probabilityFormatted}%</p>
        `;
        resultDiv.prepend(textResultDiv);
        
        const ctx = document.getElementById("predictionChart").getContext("2d");
        
        if (predictionChart) {
            predictionChart.destroy();
        }
        
        predictionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Congestion Probability', 'No Congestion Probability'],
                datasets: [{
                    data: [probability, 1 - probability],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.7)',  // Warning (yellow)
                        'rgba(40, 167, 69, 0.7)'    // Success (green)
                    ],
                    borderColor: [
                        'rgba(255, 193, 7, 1)',
                        'rgba(40, 167, 69, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += (context.parsed * 100).toFixed(2) + '%';
                                }
                                return label;
                            }
                        }
                    },
                    centerText: {
                        mainPrediction: {
                            isCongestion: result.congestion,
                            probability: result.congestion ? probability : 1 - probability
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
});