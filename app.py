import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import sentencepiece
# Load translation models and tokenizers
@st.cache_resource
def load_model(src_lang, tgt_lang):
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Translation function
def translate(text, src_lang, tgt_lang):
    tokenizer, model = load_model(src_lang, tgt_lang)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Streamlit UI
st.title("AI-Powered Translation App")
st.write("Translate text between English, Spanish, and French!")

# Input text
input_text = st.text_area("Enter text to translate", height=150)

# Language selection
languages = {"English": "en", "Spanish": "es", "French": "fr"}
src_lang = st.selectbox("Source Language", list(languages.keys()))
tgt_lang = st.selectbox("Target Language", list(languages.keys()), index=1)

# Translate button
if st.button("Translate"):
    if input_text.strip():
        if src_lang != tgt_lang:
            src_code = languages[src_lang]
            tgt_code = languages[tgt_lang]
            try:
                with st.spinner("Translating..."):
                    translation = translate(input_text, src_code, tgt_code)
                st.success("Translation complete!")
                st.write("**Translated Text:**")
                st.write(translation)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please select different source and target languages.")
    else:
        st.warning("Please enter some text to translate.")

