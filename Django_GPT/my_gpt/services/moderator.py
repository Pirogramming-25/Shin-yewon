from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,
        device=get_pipeline_device(),
    )


def analyze_toxicity(text: str):
    moderator = get_moderator_pipeline()
    results = moderator(text)[0]

    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
    top = results_sorted[0]

    return {
        "highest_label": top["label"],
        "highest_score": top["score"],
        "all_scores": results_sorted,
    }