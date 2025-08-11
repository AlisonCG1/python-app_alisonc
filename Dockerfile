FROM python:3.12-slim

WORKDIR python-app_alisonc/myapi

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "myapi.app:app", "--host", "0.0.0.0", "--port", "8080"]