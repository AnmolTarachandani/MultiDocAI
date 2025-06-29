import streamlit as st
from utils import ocr, translate, verify_text, summarize, compare
import streamlit.components.v1 as components

st.set_page_config(page_title="MultiDoc AI", layout="wide")
st.title("📄 AI Document Analyser")

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Arabic": "ar"
}

mode = st.radio("Choose Mode", ["Single Document", "Two Documents"])

uploaded_file1 = st.file_uploader("Upload Document 1", type=["pdf", "docx", "png", "jpg", "jpeg", "txt", "rtf", "csv", "odt"])
uploaded_file2 = None

if mode == "Two Documents":
    uploaded_file2 = st.file_uploader("Upload Document 2", type=["pdf", "docx", "png", "jpg", "jpeg", "txt", "rtf", "csv", "odt"])

if uploaded_file1 and (mode == "Single Document" or (mode == "Two Documents" and uploaded_file2)):
    st.markdown("### 🌐 Select translation language")
    selected_lang_name = st.selectbox(
        "Choose target language", list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index("English")
    )
    translation_lang = LANGUAGES[selected_lang_name]

    if st.button("🚀 Process Document" if mode == "Single Document" else "🚀 Process Documents"):

        # --- SINGLE DOCUMENT MODE ---
        if mode == "Single Document":
            with st.spinner("🔍 Processing..."):
                ocr_text, lang = ocr.extract_text(uploaded_file1)
                translated_text = translate.translate_text(ocr_text, target_lang=translation_lang)
                suggestions = verify_text.check(ocr_text)
                summary = summarize.get_summary(ocr_text)
                bullets = summarize.get_bullet_points(ocr_text)

            detected_lang_name = next((k for k, v in LANGUAGES.items() if v == lang), lang)
            st.subheader("📘 Document Analysis")
            st.markdown(f"**Detected Language:** `{detected_lang_name}`")

            st.markdown("### 📝 OCR Text")
            st.code(ocr_text)

            st.markdown("### 🌐 Translated Text")
            st.code(translated_text)

            st.markdown("### ✅ AI Suggestions")
            st.write(suggestions if suggestions else "No suggestions.")

            st.markdown("### 🧠 Summary")
            st.success(summary)

            st.markdown("### 📌 Bullet Points")
            if bullets:
                for point in bullets:
                    st.markdown(f"- {point}")
            else:
                st.info("No bullet points extracted.")

        # --- COMPARE TWO DOCUMENTS MODE ---
        if mode == "Two Documents":
            with st.spinner("🔍 Processing Document 1..."):
                ocr_text1, lang1 = ocr.extract_text(uploaded_file1)
                translated_text1 = translate.translate_text(ocr_text1, target_lang=translation_lang)
                suggestions1 = verify_text.check(ocr_text1)
                summary1 = summarize.get_summary(ocr_text1)
                bullets1 = summarize.get_bullet_points(ocr_text1)

            with st.spinner("🔍 Processing Document 2..."):
                ocr_text2, lang2 = ocr.extract_text(uploaded_file2)
                translated_text2 = translate.translate_text(ocr_text2, target_lang=translation_lang)
                suggestions2 = verify_text.check(ocr_text2)
                summary2 = summarize.get_summary(ocr_text2)
                bullets2 = summarize.get_bullet_points(ocr_text2)

            col1, col2 = st.columns(2)

            with col1:
                detected_lang1 = next((k for k, v in LANGUAGES.items() if v == lang1), lang1)
                st.subheader("📘 Document 1")
                st.markdown(f"**Detected Language:** `{detected_lang1}`")
                st.markdown("### 📝 OCR Text")
                st.code(ocr_text1)
                st.markdown("### 🌐 Translated Text")
                st.code(translated_text1)
                st.markdown("### ✅ AI Suggestions")
                st.write(suggestions1 if suggestions1 else "No suggestions.")
                st.markdown("### 🧠 Summary")
                st.success(summary1)
                st.markdown("### 📌 Bullet Points")
                if bullets1:
                    for point in bullets1:
                        st.markdown(f"- {point}")
                else:
                    st.info("No bullet points extracted.")

            with col2:
                detected_lang2 = next((k for k, v in LANGUAGES.items() if v == lang2), lang2)
                st.subheader("📗 Document 2")
                st.markdown(f"**Detected Language:** `{detected_lang2}`")
                st.markdown("### 📝 OCR Text")
                st.code(ocr_text2)
                st.markdown("### 🌐 Translated Text")
                st.code(translated_text2)
                st.markdown("### ✅ AI Suggestions")
                st.write(suggestions2 if suggestions2 else "No suggestions.")
                st.markdown("### 🧠 Summary")
                st.success(summary2)
                st.markdown("### 📌 Bullet Points")
                if bullets2:
                    for point in bullets2:
                        st.markdown(f"- {point}")
                else:
                    st.info("No bullet points extracted.")

            # Show Differences
            st.subheader("📊 Differences")
            diff_html, diff_summary = compare.highlight_word_diff(ocr_text1, ocr_text2)

            components.html(
                f"""
                <div style="max-height:600px; overflow:auto; border:1px solid #ccc; padding:10px;">
                    {diff_html}
                </div>
                """,
                height=300,
                scrolling=False
            )

            if diff_summary:
                st.markdown("### 🧾 Summary of Differences")
                st.markdown(diff_summary)
