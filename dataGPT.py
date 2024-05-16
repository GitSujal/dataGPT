import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Set the page title and favicon
st.set_page_config(page_title="DataGPT", page_icon=":bar_chart:")
st.title("Chat with Your Data")

# Step 1: Data Input
uploaded_files = None
with st.sidebar.title("Data Input"):
    choice = st.sidebar.radio("Choose data input method", ["Upload Data", "Choose from existing files"])

df = pd.DataFrame()
# Step 1: Data Input
if choice == "Upload Data":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", accept_multiple_files=False)
    if uploaded_file is not None and uploaded_file:
        df = pd.read_csv(uploaded_file)
        file_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]  # Get the base name without extension
        st.markdown(f"## Chatting with {file_name}")  # Write the file name
else:
    folder_path = os.path.join(os.getcwd(), "data")
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    selected_file = st.selectbox("Choose files", files, index=0)
    if selected_file:  # Check that selected_files is not None or empty
        df = pd.read_csv(os.path.join(folder_path, selected_file))
        file_name = os.path.splitext(selected_file)[0]  # Get the base name without extension
        st.markdown(f"## Chatting with {file_name}")
if df.empty:
    st.warning("Please upload a CSV file or choose from existing files.")
else:
    st.dataframe(df.head(5))
# Create an agent for each dataframe
agent = create_pandas_dataframe_agent(ChatOpenAI(model="gpt-4-turbo", temperature=0), df, verbose=True)

# Create a text input for the user to enter their analysis prompt
prompt = st.text_area("Enter your analysis prompt")
output_image = False
if "plot" in prompt.lower():
    output_image = True
    prompt = prompt + "save the chart as chart.png"
has_chart = st.checkbox("Has chart")
if has_chart:
    output_image = True
# Step 3: Data Analysis
# This is where you'd perform your data analysis based on the user's prompt
if st.button('Chat'):
    if prompt:
        st.spinner("Generating Response...")
        # Invoke each agent with the same prompt and collect the responses
        try:
            responses = agent(prompt)
        except ValueError:
            responses = {"output": "An error occurred. LLM could not generate a response. Please try again."}
        # Write each response
        if output_image:
            # plot the chart if the prompt contains the word "plot"
            st.image("chart.png", use_column_width=True, caption=responses["output"])
        else:
            st.write(responses["output"])