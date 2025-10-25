FROM python:3.12-slim


# we probably need build tools?
RUN apt-get update \
     && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY . .

CMD ["streamlit", "run", "Home.py"]
#FROM python:3.9-slim-buster
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#EXPOSE 8501
#CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
