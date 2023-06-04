FROM python:3.10-slim

RUN apt-get -q update && apt-get -q install -y wget

COPY ./model_server.py ./
COPY ./requirements.txt ./

RUN wget -q https://raw.githubusercontent.com/arj7192/fight_fraud_with_machine_learning/main/Chapter07/model.joblib

RUN pip install -r requirements.txt

USER root
ENTRYPOINT ["python", "model_server.py"]