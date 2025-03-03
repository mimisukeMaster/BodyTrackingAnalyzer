# AKRecorder
## Overview
Azure Kinect DK を使用した人体録画ツール

人体を検知している間、録画を行います。検知されていなければ録画は行われません。<br>また、関節の位置をcsv形式で保存し、録画セッションごとに分けてPNG画像を保存します。

csvファイルについては、一行に１フレーム分のデータが以下のような形で格納されています。
```csv
{ラベル番号}, {時刻(時分秒ミリ秒)}, {0点目のx座標}, {0点目のy座標}, {0点目のz座標}, {1点目のx座標}, {1点目y座標}, {1点目z座標}, ...( * 32 点分)...
6, 134210093202.8218, 7.189494, 954.5975,217.9923, -109.9409, 964.8756,235.1705,...
```
なお、`0`～`31`までの関節のインデックス番号については[こちらの公式ページ](https://learn.microsoft.com/ja-jp/previous-versions/azure/kinect-dk/body-joints)から対応関係が確認できます。


Recorder for Azure Kinect

Start recording a human when he or she appears, otherwise not.<br>
Also, saving joint positions in a csv format and color PNG images every human.

[Example Movie at a living lab](https://youtu.be/yrhxCEUvvkY)

## Requirements
```
- Visual Studio 2022
- Azure Kinect DK
- Azure Kinect Sensor SDK >= v1.4.0
- Azure Kinect Body Tracking SDK >= v1.0.0
```

## Usage
1. [`Csharp_3d_viewer.sln`](Csharp_3d_viewer.sln)を Visual Studio 2022 で開きます。プロジェクトの構成が読み込まれます。

2. Visual Studio 2022 上で`ビルド > ソリューションのビルド`を行います。

3. `デバッグ > デバッグなしで開始` を選択して実行します。

4. 開始直後は、コンソール画面から記録するデータへのラベルを設定してください。整数値を入力後、`Enter`キーで確定させます。 
> [!WARNING]
> - 開始直前と直後は **人がいないところを映してください**
> - 人を映すのは、 **記録するデータへのラベルを設定した後にしてください**
>（人体検知外の時に現在時刻を取得し、ラベルとともに検知した画像を保存する時に使用するため）

5. `ESC`キー、または`Ctrl + C`で終了します。

===================================

1. Build `Csharp_3d_viewer.sln`.

2. Click `Debug > Start without debugging` to begin.

3. Right after starting, set labels for the recorded data from the console screen.
> [!WARNING]
> - Just before and right after starting, **make sure to capture an empty scene without people**.
> - Only start capturing people **after setting labels for the recorded data**.
> (This is because the current timestamp will be obtained when no human is detected and used later when saving the detected images along with the labels.)

4. Press `ESC` key or `Ctrl + C` to exit.

## License
AKrecorder is under the [MIT](LICENSE) license.
