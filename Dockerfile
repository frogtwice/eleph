FROM python:3.12-slim
COPY . .
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "app:app"]
