# AKRecorder
## Overview
Azure Kinect DK を使用した人体録画＆分析ツール

人体を検知している間、録画を行います。検知されていなければ録画は行われません。<br>また、関節の位置をcsv形式で保存し、任意で録画セッションごとに分けてPNG画像を保存しできます。

csvファイルについては、一行に1フレーム分のデータが以下のような形で格納されています。
```csv
{ラベル番号}, {時刻(時分秒ミリ秒)}, {0点目のx座標}, {0点目のy座標}, {0点目のz座標}, {1点目のx座標}, {1点目y座標}, {1点目z座標}, ...( * 32 点分)...
6, 134210093202.8218, 7.189494, 954.5975,217.9923, -109.9409, 964.8756,235.1705,...
```
なお、`0`～`31`までの関節のインデックス番号については[こちらの公式ページ](https://learn.microsoft.com/ja-jp/previous-versions/azure/kinect-dk/body-joints)から対応関係が確認できます。

記録されたCSVファイルは、[`analyze.py`](analyze.py)でその分析をすることができます。

Recorder for Azure Kinect

Start recording a human when he or she appears, otherwise not.<br>
Also, saving joint positions in a csv format and color PNG images every human (optional).

[Example Movie at a living lab](https://youtu.be/yrhxCEUvvkY)

## Requirements
```
- Visual Studio 2022
- Azure Kinect DK
- Azure Kinect Sensor SDK >= v1.4.0
- Azure Kinect Body Tracking SDK >= v1.0.0

- numpy （数値計算）
- pandas （CSVデータ処理）
- matplotlib （描画処理）
```

## Usage
1. [`Csharp_3d_viewer.sln`](Csharp_3d_viewer.sln)を Visual Studio 2022 で開きます。プロジェクトの構成が読み込まれます。

2. Visual Studio 2022 上で`ビルド > ソリューションのビルド`を行います。

3. `デバッグ > デバッグなしで開始` を選択して実行します。

4. 開始直後は、コンソール画面から記録するデータへのラベルを設定してください。整数値を入力後、`Enter`キーで確定させます。 
> [!WARNING]
> - 開始直前と直後は **人がいないところを映してください**
> - 人を映すのは、 **記録するデータへのラベルを設定した後にしてください**
>（人体検知外の時に現在時刻を取得し、ラベルとともにデータを保存する時に使用するため）

5. `ESC`キー、または`Ctrl + C`で終了します。

6. [`analyze.py`](analyze.py)で記録したデータの分析ができます。`analyze.py`を実行後、ターミナルからCSVファイルが保存されているフォルダを順に入力してください。通常は`temp/{日付}/{時間}/{人の識別番号}/pos.csv`に保存されています。

Visual Studio 2022では基本的にC++、C#の開発に注力しているので、Pythonの実行はセットアップの手間が無いVSCodeを使用することを推奨します。

Visual Studio 2022でPythonを動かしたい場合は[こちらの記事](https://zenn.dev/mom/articles/4fd7c02bcc9087)を参照して下さい。

===================================

1. Build `Csharp_3d_viewer.sln`.

2. Click `Debug > Start without debugging` to begin.

3. Right after starting, set labels for the recorded data from the console screen.
> [!WARNING]
> - Just before and right after starting, **make sure to capture an empty scene without people**.
> - Only start capturing people **after setting labels for the recorded data**.
> (This is because the current timestamp will be obtained when no human is detected and used later when saving data along with the labels.)

4. Press `ESC` key or `Ctrl + C` to exit.

5. You can analyze the recorded data using [`analyze.py`](analyze.py). After running `analyze.py`, enter the folder where the CSV file is saved in the terminal step by step. By default, it is saved in `temp/{date}\{time}\{person ID}\pos.csv`.


## Analysis Methods on `analyze.py`
`analyze.py`では記録したデータのばらつきを示す指標として、**平均標準偏差** というものを用いています。

**定義：**
1. 各軸の時間変化による値の標準偏差を求める

    $$\sigma_x = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (x_t - \bar{x})^2},\ \sigma_y = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (y_t - \bar{y})^2},\ \sigma_z = \sqrt{\frac{1}{N} \sum_{t=1}^{N} (z_t - \bar{z})^2}$$

2. 各軸の標準偏差の平均を求める

    $$\sigma_{i} = \frac{\sigma_x + \sigma_y + \sigma_z}{3}$$

3. 全 $32$ 点分について 1. 2. を行い、その平均を指標 **平均標準偏差 $S$** とする

    $$S = \frac{1}{32} \sum_{i=1}^{32} \sigma_{i}$$

また、各ラベルごとに、全ての点の時系列データを3次元空間上にプロットして散布図を描画します。`Next`ボタンで閲覧するラベル番号を変えることができます。

===================================

In `analyze.py`, the **Mean Standard Deviation (S)** is used as an indicator of data variation.

**Definition:**
1. Compute the standard deviation of values over time for each axis.

2. Calculate the mean of the standard deviations across all three axes.

3. Perform steps 1 and 2 for all $32$ points and take the average to obtain the final indicator, **Mean Standard Deviation $S$**.


Additionally, for each label, all time-series data points are plotted in a 3D scatter plot.  
You can change the label number using the `Next` button to browse different datasets.

## License
AKRecorder is under the [MIT](LICENSE) license.
