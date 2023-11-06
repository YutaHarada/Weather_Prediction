import pickle
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from typing import Dict, Any

from preprocessing import preprocess

# アプリケーションを初期化
app = FastAPI()


# リクエストのパラメータの検証用クラス
class Feature(BaseModel):
    feature: Dict[str, Any]


# indexエンドポイント
@app.get("/")
async def index():
    responce = {"column": "value"}
    return responce


# 推論処理用エンドポイント
@app.post("/predict")
async def predict(feature: Feature):
    # レスポンス内容の初期化
    response = {}

    # S3からモデルの読み込み
    bucket = os.getenv('BUCKET_NAME')
    s3 = boto3.client('s3')

    try:
        # S3 からオブジェクトを取得
        model_obj = s3.get_object(Bucket=bucket, Key="rain_pred.model")
        # オブジェクトのコンテンツを取得
        model = pickle.loads(model_obj["Body"].read())
        # 前処理の実施
        data = preprocess(feature.feature)
        # 推論の実施
        prediction = model.predict(data)[0]
        # レスポンス内容の設定
        if prediction == 1:
            response["prediction"] = "今日は傘を持っていたほうがいいでしょう！"
        elif prediction == 0:
            response["prediction"] = "今日は傘は不要でしょう！"
        else:
            response["prediction"] = "Prediction Failed"

        return response

    except NoCredentialsError:
        return "エラー: 資格情報が見つからない、または不正です。"

    except ClientError as e:
        # ClientErrorが発生した場合、エラーメッセージを取得する
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return "エラー: 指定したオブジェクトが見つかりません。"
        else:
            return f"予期せぬエラーが発生しました: {e}"

    except Exception as e:
        # その他の例外を捕捉
        return f"エラーが発生しました: {e}"


handler = Mangum(app)
