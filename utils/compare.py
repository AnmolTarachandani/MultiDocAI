# utils/compare.py

from difflib import SequenceMatcher
import html

def highlight_word_diff(text1, text2):
    lines1 = text1.strip().split("\n")
    lines2 = text2.strip().split("\n")
    html_rows = []
    summary_diff = []

    for line1, line2 in zip(lines1, lines2):
        if line1.strip() == line2.strip():
            continue  # Skip identical lines

        words1 = line1.split()
        words2 = line2.split()
        matcher = SequenceMatcher(None, words1, words2)

        highlighted1 = []
        highlighted2 = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                highlighted1.extend(html.escape(w) for w in words1[i1:i2])
                highlighted2.extend(html.escape(w) for w in words2[j1:j2])
            else:
                highlighted1.extend(
                    f"<span style='background:yellow'>{html.escape(w)}</span>"
                    for w in words1[i1:i2]
                )
                highlighted2.extend(
                    f"<span style='background:yellow'>{html.escape(w)}</span>"
                    for w in words2[j1:j2]
                )

        row1 = " ".join(highlighted1)
        row2 = " ".join(highlighted2)

        html_rows.append(f"""
            <tr>
                <td style="background:#fff; padding:10px;">{row1}</td>
                <td style="background:#fff; padding:10px;">{row2}</td>
            </tr>
        """)

        summary_diff.append(f"- `{line1.strip()}` → `{line2.strip()}`")

    if not html_rows:
        html_table = "<p>No differences found.</p>"
    else:
        html_table = f"""
        <table style='border-collapse:collapse; width:100%; margin-bottom:10px;'>
            <thead>
                <tr>
                    <th style="padding:8px; background:#f8f8f8; border:1px solid #ccc;">Document 1</th>
                    <th style="padding:8px; background:#f8f8f8; border:1px solid #ccc;">Document 2</th>
                </tr>
            </thead>
            <tbody>
                {''.join(html_rows)}
            </tbody>
        </table>
        """

    return html_table, "\n".join(summary_diff)
