# AKRecorder
## Overview
Azure Kinect DK を使用した人体録画ツール

人体を検知すると録画を開始し、それ以外では録画しません。
また、関節の位置をcsv形式で保存し、人間ごとにPNG画像を保存します。

Recorder for Azure Kinect

Start recording a human when he or she appears, otherwise not.
Also, saving joint positions in a csv format and color PNG images every human.

[Example Movie at a living lab](https://youtu.be/yrhxCEUvvkY)

## Requirements
```cmd
Visual Studio 2022
Azure Kinect DK
Azure Kinect Sensor SDK >= v1.4.0
Azure Kinect Body Tracking SDK >= v1.0.0
```

## Usage
1. `[Csharp_3d_viewer.sln](Csharp_3d_viewer.sln)`を Visual Studio 2022 で開きます。プロジェクトの構成が読み込まれます。
2. Visual Studio 2022 上で`ビルド > ソリューションのビルド`を行います。
3. `デバッグ > デバッグなしで開始` を選択して実行します。
> [!WARNING]
> 実行直後は、必ず**人がいないところを一定時間映した後、人体を映してください。**
>（人体検知外の時に現在時刻を取得し、検知した画像を保存する時に使用するため）

4. `ESC`キー、または`Ctrl+C`で終了します。

1.Build `Csharp_3d_viewer.sln`.
2. Click `Debug > Start without debugging` to begin.
> [!WARNING]
> Immediately after execution, be sure to project a human body after projecting an area where no one is present for a certain period of time.
> (To get the current time when the human body is not detected and to use it when saving the detected image)

4. Press `ESC` key or `Ctrl+C` to exit.

## License
AKrecorder is under the [MIT](LICENSE) license.
