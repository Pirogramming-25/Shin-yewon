document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("combo-form");
    const textarea = document.getElementById("combo-text");
    const button = document.getElementById("combo-submit");
    const regenBtn = document.getElementById("combo-regenerate");
    const loading = document.getElementById("combo-loading");
    const resultBox = document.getElementById("combo-result");
    const errorBox = document.getElementById("combo-error");

    let lastText = "";

    async function runCombo(text, regenerate) {
        errorBox.textContent = "";
        button.disabled = true;
        textarea.disabled = true;
        if (regenBtn) regenBtn.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/combo/run/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ text, regenerate }),
            });

            const data = await response.json();

            if (!response.ok) {
                errorBox.textContent = data.error || "오류가 발생했습니다.";
                return;
            }

            lastText = data.original_text;

            const allScoresHtml = data.toxicity.all_scores
                .map((s) => `<li>${s.label}: ${(s.score * 100).toFixed(2)}%</li>`)
                .join("");

            resultBox.innerHTML = `
                <h3>입력 원문</h3>
                <p>${data.original_text}</p>

                <h3>요약문</h3>
                <p>${data.summary}</p>

                <h3>감정 분석</h3>
                <p>${data.sentiment.label} (${(data.sentiment.score * 100).toFixed(2)}%)</p>

                <h3>유해 표현 분석</h3>
                <p>최고 위험: ${data.toxicity.highest_label} (${(data.toxicity.highest_score * 100).toFixed(2)}%)</p>
                <ul>${allScoresHtml}</ul>

                <h3>종합 판정</h3>
                <p>${data.verdict}</p>

                <button id="combo-regenerate">재생성</button>
            `;

            document.getElementById("combo-regenerate").addEventListener("click", () => {
                runCombo(lastText, true);
            });
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } finally {
            button.disabled = false;
            textarea.disabled = false;
            loading.style.display = "none";
        }
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        runCombo(textarea.value, false);
    });
});