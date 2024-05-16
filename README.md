# DataGPT 
Chat with your data using chat gpt.

## Install Pre-requisites

```bash
pip install -r requirements.txt
```

## Setup environment variables

Create a `.env` file in the root directory and add the following variables
    
```bash
    OPENAI_API_KEY = <YOUR OPENAI KEY>
```

## Run the code

```bash
python -m streamlit run frontend.py
```

## Demo

![Demo](example.png)

1. Upload a csv file using the file uploader
2. Enter your question in the text box
3. Tick the `Has Chart` checkbox if you want to see a chart and your prompt produces a chart
4. Click on `Chat` button to get the answer