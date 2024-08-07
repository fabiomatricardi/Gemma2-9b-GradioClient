# Gemma2-9b-GradioClient
Run with API call to Hugging Face Spaces Gemma2-9B model


### Instructions
You can git clone the repo or do it yourself.

#### Dependencies and virtual environment
```
mkdir Gemma2-9b
cd Gemma2-9b
python -m venv venv     #on MAC/Linux - I am using python 3.11
python -m venv venv     #on windows
```

Activate the venv
```
source venv/bin/activate  #for mac
venv\Scripts\activate     #for windows users
```

Install packages
```
pip install huggingface_hub  gradio-client streamlit==1.36.0 tiktoken
```

### Download the files
you will need
```
stapp.py
assistant2.png
banner.png
Gemma-2-Banner.original.jpg
user.png
```

### Run the Streamlit app
with the venv activated from the terminal run
```
streamlit run stapp.py
```
