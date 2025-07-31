FROM python:3.12.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["sh", "./entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]