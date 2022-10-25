FROM tensorflow/tensorflow:latest

COPY NLP_Model.py .
COPY requirements.txt .

RUN pip install -r requirements.txt 


ENV MODEL_NAME NLP_Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE

EXPOSE 9000
