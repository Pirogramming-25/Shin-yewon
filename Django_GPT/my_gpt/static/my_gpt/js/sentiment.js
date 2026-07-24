const recentHistory = [];
let isRequesting = false;

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sentiment-form");
    const textarea = document.getElementById("sentiment-text");
    const button = document.getElementById("sentiment-submit");
    const loading = document.getElementById("sentiment-loading");
    const resultBox = document.getElementById("sentiment-result");
    const errorBox = document.getElementById("sentiment-error");
    const historyBox = document.getElementById("sentiment-history");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (isRequesting) return;
        isRequesting = true;

        errorBox.textContent = "";
        resultBox.textContent = "";
        button.disabled = true;
        textarea.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/sentiment/run/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ text: textarea.value }),
            });

            const data = await response.json();

            if (!response.ok) {
                errorBox.textContent = data.error || "오류가 발생했습니다.";
                resultBox.textContent = "";
                return;
            }

            resultBox.innerHTML = `
                <p>감정: ${data.label}</p>
                <p>신뢰도: ${(data.score * 100).toFixed(2)}%</p>
            `;

            if (recentHistory) {
                recentHistory.unshift({
                    text: textarea.value,
                    label: data.label,
                    score: data.score,
                });
                if (recentHistory.length > 5) recentHistory.pop();
                renderHistory();
            }
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
            resultBox.textContent = "";
        } finally {
            button.disabled = false;
            textarea.disabled = false;
            loading.style.display = "none";
            isRequesting = false;
        }
    });

    function renderHistory() {
        if (!historyBox) return;
        historyBox.innerHTML = recentHistory
            .map((h, i) => `<li>${i + 1}. ${h.text.slice(0, 30)} → ${h.label} (${(h.score * 100).toFixed(2)}%)</li>`)
            .join("");
    }
});