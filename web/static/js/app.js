document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predict-form");
    const resultDiv = document.getElementById("result");
    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = "<span>Loading...</span>";
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });
        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result.error) {
                resultDiv.innerHTML = `<span style='color:red;'>${result.error}</span>`;
            } else {
                resultDiv.innerHTML = `<b>Prediction:</b> ${result.prediction} <br/><b>Probability:</b> ${result.probability}`;
            }
        } catch (err) {
            resultDiv.innerHTML = `<span style='color:red;'>${err}</span>`;
        }
    });
    // Feature importance chart
    fetch("/api/feature_importance")
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById("featureImportanceChart").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.map(d => d.feature),
                    datasets: [{
                        label: "Importance",
                        data: data.map(d => d.importance),
                        backgroundColor: "rgba(54, 162, 235, 0.5)",
                    }]
                },
                options: { responsive: true }
            });
        });
});