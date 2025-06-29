import re

def preprocess_text(text):
    lines = text.splitlines()
    unique = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
    return unique

def get_summary(text):
    lines = preprocess_text(text)

    # Simple fallback summary: first 3 informative lines
    summary_lines = []
    for line in lines:
        if len(line.split()) > 4:  # ignore short lines
            summary_lines.append(line)
        if len(summary_lines) >= 3:
            break

    if summary_lines:
        return " ".join(summary_lines)
    return "No meaningful summary could be generated."

def get_bullet_points(text):
    lines = preprocess_text(text)

    # Basic bullet point logic based on simple filtering
    bullets = []
    for line in lines:
        if any(keyword in line.lower() for keyword in ["important", "note", "includes", "summary", "step", "feature", "•", "- "]):
            bullets.append(line.strip("•-* \t"))
        elif len(line.split()) >= 6:
            bullets.append(line.strip())

        if len(bullets) >= 5:
            break

    return bullets or ["No bullet points could be extracted."]
