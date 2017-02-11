# coding: utf-8

#
# extract_contents.py; objects.jsonに含まれる画像の物体名(synsets)を
#                      ファイルに抽出するスクリプト
#
# 使い方: python extract_contents.py
# オプション: なし
#

import os
import json

SCRIPT_NAME = "extract_contents.py"  # スクリプト名
JSON_FILEPATH = "../objects.json"  # jsonファイルの位置
OUTPUT_FILEPATH = "./results/contents.csv"  # 結果出力位置


# json形式ファイル読み込み
def load_json_data(json_filepath):

    print("Loading json data...")

    # エラー処理: jsonファイルの存在
    if not os.path.exists(json_filepath):
        print("ERROR: %s does not exist." % json_filepath)
        exit(1)

    # エラー処理: 入力パスがjsonファイルであるかの確認
    if not json_filepath.endswith(".json"):
        print("ERROR: This is not JSON file. (.json)")
        exit(1)

    # ファイルを開いてjson形式を読み込む
    with open(json_filepath, "r") as f:
        json_data = json.load(f)

    return json_data


# コンテンツの種類と数をリストにして返す.
def extract_contents_by_synsets(json_data):

    print("Extracting contents...")

    # 辞書型配列で, 該当した名前を数える
    contents_dict = dict()
    for jd in json_data:
        for ob in jd["objects"]:
            if len(ob["synsets"]) > 0:
                name = ob["synsets"][0]
                if name in contents_dict:
                    contents_dict[name] += 1
                else:
                    contents_dict[name] = 1

    # 出現頻度順にソートしたリスト取得
    contents_list = sorted(contents_dict.items(),
                           key=lambda x: x[1],
                           reverse=True)

    return contents_list


# ファイル出力
def output_textfile(result_list, output_filepath):

    print("Outputing result...")

    # エラー処理: ファイルパスの仕様統一
    if not output_filepath.startswith("./"):
        output_filepath = "./" + output_filepath

    # ディレクトリパスを抽出
    dir_path = ""
    for word in output_filepath.split("/")[:-1]:
        dir_path += "%s/" % word

    # エラー処理: 存在しないディレクトリを作成
    if not os.path.exists(dir_path):
        print("WARNING: %s does not exist. mkdir" % dir_path)
        os.mkdir(dir_path)

    # 結果を出力
    with open(output_filepath, "w") as f:
        f.write("name,count\n")
        for rl in result_list:
            f.write("%s,%s\n" % (rl[0], rl[1]))

    print("Output to %s" % output_filepath)


if __name__ == "__main__":

    print("\n%s: START" % SCRIPT_NAME)

    # jsonファイル読み込み
    json_data = load_json_data(JSON_FILEPATH)

    # コンテンツと数を抜き出す
    contents_list = extract_contents_by_synsets(json_data)

    # textファイルに出力
    output_textfile(contents_list, OUTPUT_FILEPATH)

    print("%s: DONE\n" % SCRIPT_NAME)
