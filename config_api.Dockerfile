FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /freqtrade/user_data

RUN pip install flask gunicorn --quiet

COPY user_data/config_api.py /freqtrade/user_data/config_api.py
COPY user_data/config_manager.html /freqtrade/user_data/config_manager.html
COPY user_data/config.json /freqtrade/user_data/config.json
COPY user_data/strategies /freqtrade/user_data/strategies

EXPOSE 8081

CMD ["gunicorn", "--bind", "0.0.0.0:8081", "--workers", "2", "--timeout", "120", "config_api:app"]
