FROM tensorflow/tensorflow:latest

WORKDIR /app

COPY fast_api_server.py .
COPY requirements.txt .

RUN pip install -r requirements.txt 

EXPOSE 8000

CMD [ "uvicorn", "fast_api_server:app", "--host" , "0.0.0.0"]