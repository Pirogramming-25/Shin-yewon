from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-6-6",
        device=get_pipeline_device(),
    )


def summarize_text(text: str, do_sample: bool = False):
    summarizer = get_summarizer_pipeline()

    kwargs = {
        "max_length": 180,
        "min_length": 40,
        "do_sample": do_sample,
    }

    if do_sample:
        kwargs["top_p"] = 0.9
        kwargs["temperature"] = 0.8

    result = summarizer(text, **kwargs)

    summary = result[0]["summary_text"]
    ratio = (len(summary) / len(text)) * 100

    return {
        "summary": summary,
        "original_length": len(text),
        "summary_length": len(summary),
        "ratio": ratio,
    }