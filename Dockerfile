FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY ./scripts ./scripts

ENTRYPOINT ["streamlit", "run"]

CMD ["./scripts/app.py"]
