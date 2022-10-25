FROM tensorflow/tensorflow:latest

WORKDIR /app

COPY NLP_Model.py .
COPY requirements.txt .

RUN pip install -r requirements.txt 

ENV PYTHONPATH /app

ENV MODEL_NAME NLP_Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

RUN chown -R 8888 /app
RUN mkdir /.cache
RUN chmod 777 /.cache
RUN mkdir /.config
RUN chmod 777 /.config

CMD exec seldon-core-microservice $MODEL_NAME $API_TYPE --service-type $SERVICE_TYPE --persistence $PERSISTENCE

EXPOSE 9000
