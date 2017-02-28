# coding: utf-8

#
# extract_bbox_to_normalize.py;
# bbox(bounding box)を正規化した状態で抽出するスクリプト
#
# 使い方: python extract_bbox_to_normalize.py
# オプション: [-i 画像リストファイル]
#             [-o 出力先ディレクトリ]
#             [-s オブジェクト名(synsets)]
#             [-l オブジェクトID]
# 出力: (ID) x y width height <- 正規化された状態
#
# 注意: これはextract_bbox_by_image_list.pyとほぼ同じ機能で,
#       値だけを画像サイズで正規化するものである.
#       従って, extract_bbox_by_image_list.pyで十分な場合は,
#       このスクリプトを実行する必要はない.
#
# 注意2: 外部ライブラリを用いるため, 必要であれば,
#        付属のrequirements.txtからインストールする.
#          pip install -r requirements.txt
#
# * オプションを指定しない場合は以下の通り.
#     -i=./results/image_list.txt
#     -o=./out/
#     -s=clock.n.01
#     -l=None
#
# * IDを指定しない場合は4列として出力.
# * iオプションのファイルは, 先にextract_image.pyで
#   作成する必要がある.
# * iオプションをNoneと指定した場合は
#   このスクリプトでsynsetsを自動的に抽出・指定する.
#

import os
import json
import argparse
from PIL import Image as im

SCRIPT_NAME = "extract_bbox_by_image_list.py"
JSON_FILEPATH = "../objects.json"
IMAGE_DIR = "../images/"


# json形式ファイル読み込み
def load_json_data(json_filepath):

    print("Loading json data...")

    # エラー処理: jsonファイルの存在
    if not os.path.exists(json_filepath):
        print("  ERROR: %s does not exist." % json_filepath)
        exit(1)

    # エラー処理: 入力パスがjsonファイルであるかの確認
    if not json_filepath.endswith(".json"):
        print("  ERROR: This is not JSON file. (.json)")
        exit(1)

    # ファイルを開いてjson形式を読み込む
    with open(json_filepath, "r") as f:
        json_data = json.load(f)

    return json_data


# synsetsを指定して該当の画像IDを抜き出す.
def extract_synsets(json_data, synsets_name):

    print("Extract Synsets...")

    synsets = []
    for jd in json_data:
        for ob in jd["objects"]:
            if len(ob["synsets"]) > 0:
                if ob["synsets"][0] == synsets_name:
                    synsets.append("%s.jpg" % jd["image_id"])

    synsets = list(set(synsets))  # 重複をなくす.
    return synsets


# synsetsを指定して該当の画像IDとjsonデータを抜き出す.
# output: list([画像ID(int), jsonデータ(dictionary)])
def extract_json_data(json_data, synsets_name):

    print("Extract Json Data...")

    jd_list = []  # json_data_list
    for jd in json_data:
        for ob in jd["objects"]:
            synsets = ob["synsets"]
            if len(synsets) > 0:
                if synsets[0] == synsets_name:
                    cols = [int(jd["image_id"]), ob]
                    jd_list.append(cols)

    return jd_list


# jpg_listに該当するjson_data_listから
# bboxデータ(x, y, weight, height)を抜き出す
def extract_bbox_data(json_data_list,
                      jpg_list,
                      synsets_name,
                      ids=None):

    print("Extract Bounding Box Data...")

    bbox = {}

    for jl in jpg_list:

        samples_row = []

        # 画像を開いて大きさ情報を取得
        with im.open("%s/%s" % (IMAGE_DIR, jl), "r") as img:
            width, height = img.size

        # jsonデータについて走査
        for jd in json_data_list:
            jpg_name = int(jl.split(".")[0])
            jd_list_id = int(jd[0])

            # oo.jpgのoo部とjsonのimage_idが一致すれば
            if jpg_name == jd_list_id:
                samples_col = []

                if ids is not None:
                    samples_col.append(ids)

                samples_col.append("%.17lf"
                                   % (float(jd[1]["x"]) / int(width)))
                samples_col.append("%.17lf"
                                   % (float(jd[1]["y"]) / int(height)))
                samples_col.append("%.17lf"
                                   % (float(jd[1]["w"]) / int(width)))
                samples_col.append("%.17lf"
                                   % (float(jd[1]["h"]) / int(height)))
                samples_row.append(samples_col)

        bbox[jl] = samples_row

    return bbox


# textファイル(jpgリスト)を入力する関数
def input_textfile(input_filepath):

    print("Input data: %s" % input_filepath)

    text_list = []
    with open(input_filepath, "r") as f:
        for line in f:
            text_list.append(line.strip())

    return text_list


# 結果を出力する関数
def output_textfile(result_dict, output_dir):

    print("Output result...")

    # エラー処理: ファイルパスの仕様統一
    if not output_dir.startswith("./"):
        output_dir = "./" + output_dir

    if not output_dir.endswith("/"):
        output_dir += "/"

    # エラー処理: 存在しないディレクトリの作成
    if not os.path.exists(output_dir):
        print("  ATTENTION: %s does not exist. mkdir" % output_dir)
        os.mkdir(output_dir)

    # 結果を出力
    for key, value in result_dict.items():
        txt_id = "{0:08d}.txt".format(int(key.split(".")[0]))
        with open(output_dir + txt_id, "w") as f:
            for value_row in value:
                string = " ".join([str(vr) for vr in value_row])
                f.write("%s\n" % string)

    print("Output to %s" % output_dir)


# メイン部
if __name__ == "__main__":

    print("\n%s: START" % SCRIPT_NAME)

    # 引数取得
    p = argparse.ArgumentParser()
    p.add_argument("-i", type=str, default="results/image_list.txt")
    p.add_argument("-o", type=str, default="./out/")
    p.add_argument("-s", type=str, default="clock.n.01")
    p.add_argument("-l", type=int, default=None)
    args = p.parse_args()

    input_file = args.i
    output_dir = args.o
    synsets_name = args.s
    label_num = args.l

    print("Args:")
    print("  -i; input_file: %s" % input_file)
    print("  -o; output_dir: %s" % output_dir)
    print("  -s; synsets_name: %s" % synsets_name)
    print("  -l; label_num: %s" % label_num)

    # jsonファイル全体を読み込み
    json_data = load_json_data(JSON_FILEPATH)

    # jpgリストファイル読み込み
    if input_file == "None":
        jpg_list = extract_synsets(json_data, synsets_name)
    else:
        jpg_list = input_textfile(input_file)

    # synsetsに該当するjsonファイルとその画像番号を取得
    json_data_list = extract_json_data(json_data, synsets_name)

    # boundingboxの形式でデータ抽出
    bbox_dict = extract_bbox_data(json_data_list,
                                  jpg_list,
                                  synsets_name,
                                  ids=label_num)

    # 結果を出力
    output_textfile(bbox_dict, output_dir)

    print("%s: DONE\n" % SCRIPT_NAME)
