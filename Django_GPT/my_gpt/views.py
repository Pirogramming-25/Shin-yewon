import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .decorators import model_login_required
from .models import InferenceHistory
from .services.sentiment import analyze_sentiment
from .services.summarizer import summarize_text
from .services.moderator import analyze_toxicity
from .services.combo import run_combo_analysis

logger = logging.getLogger(__name__)

MIN_SENTIMENT_LEN = 1
MAX_SENTIMENT_LEN = 1000

MIN_SUMMARIZE_LEN = 100
MAX_SUMMARIZE_LEN = 5000

MIN_MODERATE_LEN = 1
MAX_MODERATE_LEN = 1000

MIN_COMBO_LEN = 200
MAX_COMBO_LEN = 5000

def sentiment_view(request):
    histories = None
    if request.user.is_authenticated:
        histories = InferenceHistory.objects.filter(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
        ).order_by("-created_at")[:5]

    return render(request, "my_gpt/sentiment.html", {"histories": histories})


@require_POST
def sentiment_run_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    text = data.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력 형식입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    if len(text) > MAX_SENTIMENT_LEN:
        return JsonResponse(
            {"error": f"{MAX_SENTIMENT_LEN}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = analyze_sentiment(text)
    except Exception:
        logger.exception("Sentiment inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    if request.user.is_authenticated:
        InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=text,
            output_text=result["label"],
            result_data=result,
        )

    return JsonResponse(result)

@model_login_required
def summarize_view(request):
    histories = InferenceHistory.objects.filter(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
    ).order_by("-created_at")[:5]

    return render(request, "my_gpt/summarize.html", {"histories": histories})


@model_login_required
@require_POST
def summarize_run_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    text = data.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력 형식입니다."}, status=400)

    if len(text.strip()) < MIN_SUMMARIZE_LEN:
        return JsonResponse(
            {"error": f"요약할 문서는 {MIN_SUMMARIZE_LEN}자 이상 입력해주세요."},
            status=400,
        )

    if len(text) > MAX_SUMMARIZE_LEN:
        return JsonResponse(
            {"error": f"문서는 {MAX_SUMMARIZE_LEN}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = summarize_text(text)
    except Exception:
        logger.exception("Summarization failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def moderate_view(request):
    histories = InferenceHistory.objects.filter(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
    ).order_by("-created_at")[:5]

    return render(request, "my_gpt/moderate.html", {"histories": histories})


@model_login_required
@require_POST
def moderate_run_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    text = data.get("text", "")

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력 형식입니다."}, status=400)

    if not text.strip():
        return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)

    if len(text) > MAX_MODERATE_LEN:
        return JsonResponse(
            {"error": f"{MAX_MODERATE_LEN}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = analyze_toxicity(text)
    except Exception:
        logger.exception("Moderation inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=result["highest_label"],
        result_data=result,
    )

    return JsonResponse(result)


@model_login_required
def combo_view(request):
    histories = InferenceHistory.objects.filter(
        user=request.user,
        task=InferenceHistory.Task.COMBO,
    ).order_by("-created_at")[:5]

    return render(request, "my_gpt/combo.html", {"histories": histories})


@model_login_required
@require_POST
def combo_run_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

    text = data.get("text", "")
    regenerate = bool(data.get("regenerate", False))

    if not isinstance(text, str):
        return JsonResponse({"error": "잘못된 입력 형식입니다."}, status=400)

    if len(text.strip()) < MIN_COMBO_LEN:
        return JsonResponse(
            {"error": f"복합 분석은 {MIN_COMBO_LEN}자 이상 입력해주세요."},
            status=400,
        )

    if len(text) > MAX_COMBO_LEN:
        return JsonResponse(
            {"error": f"문서는 {MAX_COMBO_LEN}자 이하로 입력해주세요."},
            status=400,
        )

    try:
        result = run_combo_analysis(text, do_sample=regenerate)
    except Exception:
        logger.exception("Combo inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.COMBO,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(result)