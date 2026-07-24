document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("summarize-form");
    const textarea = document.getElementById("summarize-text");
    const button = document.getElementById("summarize-submit");
    const loading = document.getElementById("summarize-loading");
    const resultBox = document.getElementById("summarize-result");
    const errorBox = document.getElementById("summarize-error");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        errorBox.textContent = "";
        resultBox.innerHTML = "";
        button.disabled = true;
        textarea.disabled = true;
        loading.style.display = "block";

        try {
            const response = await fetch("/summarize/run/", {
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
                return;
            }

            resultBox.innerHTML = `
                <p>원문 길이: ${data.original_length}자</p>
                <p>요약문 길이: ${data.summary_length}자</p>
                <p>요약 비율: ${data.ratio.toFixed(2)}%</p>
                <p>요약 결과: ${data.summary}</p>
            `;
        } catch (err) {
            errorBox.textContent = "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } finally {
            button.disabled = false;
            textarea.disabled = false;
            loading.style.display = "none";
        }
    });
});