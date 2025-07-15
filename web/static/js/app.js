document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predict-form");
    const resultDiv = document.getElementById("result");
    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = "<span>Loading...</span>";
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { 
            // Convert string numbers to actual numbers
            data[key] = ["duration", "src_bytes", "dst_bytes", "packet_count", "service_count", "hour"].includes(key) 
                ? Number(value) 
                : value; 
        });
        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            if (result.error) {
                resultDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
            } else {
                const congestionText = result.congestion ? "Yes" : "No";
                const probability = (result.probability * 100).toFixed(2);
                resultDiv.innerHTML = `
                    <div class="alert ${result.congestion ? 'alert-warning' : 'alert-success'}">
                        <h4>Prediction Results:</h4>
                        <p><b>Congestion Predicted:</b> ${congestionText}</p>
                        <p><b>Probability:</b> ${probability}%</p>
                    </div>`;
            }
        } catch (err) {
            resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
        }
    });
});