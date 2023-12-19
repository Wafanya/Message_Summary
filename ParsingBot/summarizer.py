from typing import Dict, Literal

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def summarize_text(text: str) -> Dict[Literal["summary_text"], str]:
    # Load tokenizer and model 
    tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")
    model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")

    # Define summarizer 
    summarizer = pipeline('summarization', model=model, tokenizer=tokenizer)

    return summarizer(text, max_length=250, min_length=30, do_sample=False)