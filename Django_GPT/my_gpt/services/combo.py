from .summarizer import summarize_text
from .sentiment import analyze_sentiment
from .moderator import analyze_toxicity


def run_combo_analysis(text: str, do_sample: bool = False):
    summary_result = summarize_text(text, do_sample=do_sample)
    summary = summary_result["summary"]

    sentiment_result = analyze_sentiment(summary)
    toxicity_result = analyze_toxicity(summary)

    sentiment_label = sentiment_result["label"].lower()
    toxicity_score = toxicity_result["highest_score"]

    if sentiment_label == "negative":
        sentiment_description = "부정적인 평가를 포함합니다."
    else:
        sentiment_description = "강한 부정적 평가는 확인되지 않았습니다."

    if toxicity_score >= 0.5:
        toxicity_description = "유해 표현 가능성이 높습니다."
    else:
        toxicity_description = "심각한 유해 표현 가능성은 낮습니다."

    verdict = f"이 피드백은 {sentiment_description} {toxicity_description}"

    return {
        "original_text": text,
        "summary": summary,
        "sentiment": {
            "label": sentiment_result["label"],
            "score": sentiment_result["score"],
        },
        "toxicity": {
            "highest_label": toxicity_result["highest_label"],
            "highest_score": toxicity_result["highest_score"],
            "all_scores": toxicity_result["all_scores"],
        },
        "verdict": verdict,
    }