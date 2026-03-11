FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade/user_data

COPY user_data/config_api.py /freqtrade/user_data/config_api.py
COPY user_data/config_manager.html /freqtrade/user_data/config_manager.html
COPY user_data/config.json /freqtrade/user_data/config.json

RUN pip install flask --quiet

EXPOSE 8080 8081

CMD sh -c "python config_api.py & \
    sleep 2 && \
    freqtrade trade \
    --logfile /freqtrade/user_data/logs/freqtrade.log \
    --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite \
    --config /freqtrade/user_data/config.json \
    --strategy SampleStrategy"
