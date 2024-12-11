import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the Salesforce CodeT5 model and tokenizer
@st.cache_resource
def load_model():
    model_name = "Salesforce/codeT5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# Load the model and tokenizer
try:
    tokenizer, model = load_model()
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Streamlit app title
st.title("Salesforce CodeT5 - AI Coding Assistant 🤖")

# Input box for user prompt
prompt = st.text_area("Enter your coding task or question:", "")

# Generate code when the user clicks the button
if st.button("Generate Code"):
    if prompt.strip():
        with st.spinner("Generating code..."):
            try:
                # Tokenize input and generate output
                inputs = tokenizer(prompt, return_tensors="pt")
                outputs = model.generate(inputs["input_ids"], max_length=256)
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
