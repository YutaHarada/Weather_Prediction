import numpy as np
import pandas as pd
import re


# 月情報を三角関数で変換
def trig_encoding(df, col):

    # 三角関数の値を計算
    df[col + "_cos"] = np.cos(2 * np.pi * df[col] / 12)
    df[col + "_sin"] = np.sin(2 * np.pi * df[col] / 12)

    # 不要列を削除
    df.drop(columns=[col], inplace=True)

    return df


# 余分な記号や空白の除外
def modify_string(x):
    # 不要記号などの除去
    x = re.sub(r"[\)|\]|\s]", "", x)

    return x


# One-Hot-Vector化
def one_hot_encoding(df, col):
    # 最大風速の風向に応じて値を割り振る
    directions = ["北", "北北東", "北北西", "北東", "北西", "南", "南南東",
                  "南南西", "南東", "南西", "東", "東北東", "東南東", "西", "西北西", "西南西"]

    # 全ての方角を0とする
    for d in directions:
        df[d] = 0

    # 最大風速(風向)の値が取得できていればその方角の値を1とする
    direction = df[col].tolist()[0]
    if direction in directions:
        df[direction] = 1

    # 不要列を削除
    df.drop(columns=[col], inplace=True)

    return df


def preprocess(features: dict):
    # 受け取った辞書型データをDataSeriesに変換
    df = pd.DataFrame.from_dict(features, orient="index").T
    df = df.apply(pd.to_numeric, errors="ignore").copy()
    # 月の情報を三角関数で変換
    df = trig_encoding(df, "月")

    # 不要記号などの除去
    df["最大風速（風向）"] = df["最大風速（風向）"].apply(modify_string)
    # One-Hot-Vector化
    df = one_hot_encoding(df, "最大風速（風向）")

    return df
