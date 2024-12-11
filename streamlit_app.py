import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

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
tokenizer, model = load_model()

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

# Instructions for using the app
st.markdown("""
### How to Use
1. Enter a natural language description of your coding task or question (e.g., "Write a Python function to reverse a string").
2. Click "Generate Code" to see the AI-generated code.
""")
