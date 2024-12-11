import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Set a custom cache directory
os.environ["TRANSFORMERS_CACHE"] = "./model_cache"

# Hugging Face API token
HF_TOKEN = "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"

# Load the BigCode StarCoder model and tokenizer
@st.cache_resource
def load_model():
    model_name = "bigcode/starcoder"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HF_TOKEN)
    return tokenizer, model

# Load the model and tokenizer
try:
    tokenizer, model = load_model()
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Streamlit app title
st.title("BigCode StarCoder - AI Coding Assistant 🤖")

# Input box for user prompt
prompt = st.text_area("Enter your coding task or question:", "")

# Generate code when the user clicks the button
if st.button("Generate Code"):
    if prompt.strip():
        with st.spinner("Generating code..."):
            try:
                # Tokenize input and generate output
                inputs = tokenizer(prompt, return_tensors="pt")
                outputs = model.generate(inputs["input_ids"], max_length=256, num_return_sequences=1)
                generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Display the generated code
                st.subheader("Generated Code")
                st.code(generated_code, language="python")
            except Exception as e:
                st.error(f"Error generating code: {e}")
    else:
        st.warning("Please enter a prompt to generate code.")
