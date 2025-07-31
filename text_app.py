import streamlit as st
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

st.title("😂 AI Joke Generator")

@st.cache_resource
def load_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return generator

text_generator = load_model()

prompt = st.text_input("Start your joke with...", "Why did the chicken")

if st.button("Generate Joke"):
    with st.spinner("Making you laugh... 😂"):
        output = text_generator(prompt, max_length=100, num_return_sequences=1)
        st.markdown("### 🃏 Here's your AI joke:")
        st.success(output[0]['generated_text'])
