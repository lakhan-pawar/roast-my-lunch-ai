import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secret API key from the .env file
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

# 2. Configure the Page
st.set_page_config(page_title="Roast My Lunch", page_icon="🥪")

# 3. Add the Title and Instructions
st.title("🥪 Roast My Lunch")
st.write("I am an AI trained by the finest (and meanest) chefs. Describe your lunch, and I will judge your life choices.")

# 4. Initialize the Groq Client (The Brain)
# We check if the key exists to prevent crashing if you forgot the .env file
if not api_key:
    st.error("🚨 API Key missing! Please create a .env file with your GROQ_API_KEY.")
    st.stop()

client = Groq(api_key=api_key)

# 5. The User Input
# We use a text area so you can type a detailed description
lunch_description = st.text_area("Describe your meal:", placeholder="Example: A soggy turkey sandwich with generic mayo and a bag of stale chips...")

# 6. The Logic (The Button)
if st.button("Roast It! 🔥"):
    if lunch_description:
        # Show a spinner while the AI thinks (Good UX)
        with st.spinner("Analyzing nutritional value... and emotional damage..."):
            
            try:
                # This is the actual call to the AI Model
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a harsh, snarky, and funny food critic like Gordon Ramsay. Keep it short (2-3 sentences). Roast the user's meal description brutally but humorously."
                        },
                        {
                            "role": "user",
                            "content": lunch_description,
                        }
                    ],
                    # We use Llama 3 because it is fast and smart
                    model="llama-3.1-8b-instant",
                )

                # Extract the answer
                roast = chat_completion.choices[0].message.content
                
                # Display the result
                st.success("Here is the verdict:")
                st.markdown(f"### *\"{roast}\"*")
                
            except Exception as e:
                st.error(f"Error calling AI: {e}")
    else:
        st.warning("Please describe your lunch first!")

# 7. Sidebar (Optional - for professional polish)
with st.sidebar:
    st.header("About")
    st.write("Built with **Llama 3** and **Streamlit**.")
    #st.write("Week 1 of my AI Journey.")