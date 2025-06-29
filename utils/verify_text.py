# utils/verify_text.py

from transformers import pipeline

grammar_checker = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction")

def check(text):
    if not text.strip():
        return ["No content to check."]
    
    if len(text) > 512:
        text = text[:512]  # limit input for performance

    result = grammar_checker(text, max_length=512)
    corrected = result[0]['generated_text']

    if corrected.strip() == text.strip():
        return ["No grammatical suggestions."]

    return [f"Suggestion: {corrected.strip()}"]
