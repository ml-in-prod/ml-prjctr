FROM tensorflow/tensorflow:latest

WORKDIR /app

COPY streamlit.py .
COPY requirements.txt .

RUN pip install -r requirements.txt 

EXPOSE 8000

CMD [ "streamlit", "run", "streamlit.py"]