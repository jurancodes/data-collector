FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY nba-player-loader.py /app/

CMD ["python", "nba-player-loader.py"]
