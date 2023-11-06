FROM python:3.8-buster AS builder
# 各種パッケージをインストール
COPY requirements.txt .

RUN pip install awslambdaric && \
    pip install -r requirements.txt 

# マルチステージビルドを使う。
FROM python:3.8-slim-buster
ARG APP_DIR="/home/app/"
# スクリプトのコピー
COPY app.py ${APP_DIR}/app.py
COPY preprocessing.py ${APP_DIR}/preprocessing.py
WORKDIR ${APP_DIR}
COPY --from=builder  /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages/
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
