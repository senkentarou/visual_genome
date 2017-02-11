# Visual Genome の画像を扱うためのスクリプト
---

## 概要

 * 開発・実行環境:
   * ubuntu 14.04LTS(64 bit)
   * python 3.4.5


 * Visual Genome:
     * 公式サイト: [Visual Genome](http://visualgenome.org/)
     * ダウンロードページ: [Visual Genome Dataset](http://visualgenome.org/api/v0/api_home.html)

     * 今回使用するデータセット:
       * [Download images part1(9.2GB)](https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip)
       * [Download images part2(5.47GB)](https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip)
       * [Download objects(413.87)](http://visualgenome.org/static/data/dataset/objects.json.zip)


 * スクリプト:
   * extract_contents.py
     * 画像内の物体を表す語(synsets)を, 出現頻度順にソートするスクリプト.
     * 画像に含まれる物体の種類の確認に使用.  

   * extract_image.py
     * 画像内の物体を表す語(synsets)から, その物体を含む画像のリストを出力するスクリプト
     * 画像の抽出に使用

   * extract_bbox_by_image_list.py
     * 画像内の物体を表す語(synsets)から, その物体が位置する範囲(Bounding Box; bbox)を抽出するスクリプト
     * 物体の位置抽出に使用(x, y, width, height)

   * extract_bbox_to_normalize.py
     * 画像内の物体を表す語(synsets)から, その物体が位置する範囲(Bounding Box; bbox)を画像の縦横のサイズで正規化(0~1で表現)して抽出するスクリプト
     * 物体の位置抽出に使用(x, y, width, height)


## 実行手順

 1. データセットとスクリプトをダウンロード
   * 上記のデータセットのリンクからダウンロードする.
   * **以下では, 次のディレクトリ構造を前提とする.**
   ```
     visual_genome (フォルダ)
       |- images (フォルダ; ダウンロードしたpart1とpart2を統合したもの. 自分で作成する)
       |- scripts (フォルダ; 本スクリプト群を格納する)
       |- objects.json (ファイル)
   ```

 2. scriptsフォルダへ移動
   ```
     cd scripts
   ```

 3. スクリプト実行
   * synsetsの種類の確認のため, extract_contents.pyを実行
     ```
       python extract_contents.py
     ```

     * 実行結果として, ./results/contents.csvが生成されていることを確認する.
       ```
         less ./results/contents.csv
       ```
     * synsetsは, ファイルの第1列(name列)に記載されている文字列である.

   * お気に入りのsynsetsを見つけたら, それを含む画像を抽出するために,  
     extract_image.pyを実行

     * synsetsとして, "clock.n.01"を指定して"100"枚抽出する場合,
       ```
         python extract_image.py -t clock.n.01 -n 100
       ```

       * 実行結果として, ./results/image_list.txtが生成されていることを確認する.
       ```
         less ./results/image_list.txt
       ```

   * synsetsと, それを含む画像から位置情報(Bounding Box)を抽出したい場合は,  
     extract_bbox_by_image_list.pyを実行

     * synsetsとして, "clock.n.01", 画像リストとして, "./results/image_list.txt"を指定する場合,
       ```
         python extract_bbox_by_image_list.py -s clock.n.01 -i ./results/image_list.txt
       ```

       * 実行結果として./out/以下にファイルが生成されていることを確認する.
       ```
         ls ./out/
       ```

   * Bounding Boxについて正規化したバージョンが良い場合は,  
     extract_bbox_to_normalize.pyを実行

     * synsetsとして, "clock.n.01", 画像リストとして, "./results/image_list.txt"を指定する場合,
       ```
         python extract_bbox_to_normalize.py -s clock.n.01 -i ./results/image_list.txt
       ```

　* 上記の方法以外にオプションを指定できる場合があるため, 詳細は各スクリプトの上部のコメントを参照すること


## おすすめの活用方法
 * **以下では, scriptsの親ディレクトリ(visual_genome)からのコマンドを前提とする.**

 * extract_image.pyの実行結果の画像リスト(./scripts/results/image_list.txt)から特定の画像をディレクトリに集める.
   * image_partフォルダを作って, その中に集める場合,
   ```
     mkdir image_part
     cat ./scripts/results/image_list.txt | xargs -I{} cp ./images/{} ./image_part/
   ```

---
