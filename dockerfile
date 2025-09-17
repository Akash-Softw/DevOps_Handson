# Dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Upgrade pip to the latest version to avoid vulnerabilities
RUN pip install --upgrade pip

# Reduce image vulnerabilities by minimizing installed packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y ca-certificates && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 6000
CMD ["gunicorn","--workers","2","--bind","0.0.0.0:6000","app:app"]
