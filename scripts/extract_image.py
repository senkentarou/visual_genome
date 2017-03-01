# coding: utf-8

#
# extract_image.py; 指定した物体を含む画像のリストを出力するスクリプト
#
# 使い方: python extract_image.py
# オプション: [-s 対象物体名(synsets)]
#             [-n 画像リストの長さ(数)]
#             [-o 出力先のファイルパス]
# * オプションを指定しない場合は,
#     -s=clock.n.01, -n=100, -o=./results/image_list.txt
#   となる.
#

import os
import json
import argparse

SCRIPT_NAME = "extract_image.py"
JSON_FILEPATH = "../objects.json"


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


# nameを指定して該当の画像IDを抜き出す.
def extract_image_list(json_data, extract_name):

    print("Extracting image list by name...")

    image_list = []
    for jd in json_data:
        for ob in jd["objects"]:
            if ob["names"][0] == extract_name:
                image_list.append("%s.jpg" % jd["image_id"])

    # 重複をなくす.
    image_list = list(set(image_list))

    return image_list


# synsetsを指定して該当の画像IDを抜き出す.
def extract_image_list_by_synsets(json_data, synsets_name):

    print("Extracting image list by synsets...")

    image_list = []
    for jd in json_data:
        for ob in jd["objects"]:
            synsets = ob["synsets"]
            if len(synsets) > 0:
                if synsets[0] == synsets_name:
                    image_list.append("%s.jpg" % jd["image_id"])

    # 重複をなくす.
    image_list = list(set(image_list))

    return image_list


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
        for rl in result_list:
            f.write("%s\n" % rl)

    print("Output to %s" % output_filepath)


# メイン部
if __name__ == "__main__":

    print("\n%s: START" % SCRIPT_NAME)

    # 引数取得
    p = argparse.ArgumentParser()
    p.add_argument("-s", type=str, default="clock.n.01")
    p.add_argument("-o", type=str, default="./results/image_list.txt")
    p.add_argument("-n", type=int, default=100)
    args = p.parse_args()

    synsets_name = args.s
    output_filepath = args.o
    num = args.n

    print("Args:")
    print("  -s; synsets_name: %s" % synsets_name)
    print("  -o; output_filepath: %s" % output_filepath)
    print("  -n; num: %s" % num)

    # jsonファイル読み込み
    json_data = load_json_data(JSON_FILEPATH)

    # 該当するidを抜き出す
    #image_list = extract_image_list(json_data, synsets_name)

    # 該当するidを抜き出す
    image_list = extract_image_list_by_synsets(json_data, synsets_name)

    # textファイルに出力
    output_textfile(image_list[:num], output_filepath)

    print("%s: DONE\n" % SCRIPT_NAME)
