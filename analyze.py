import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button

# Azure Kinectの関節名
joint_names = [
    "PELVIS", "SPINE_NAVAL", "SPINE_CHEST", "NECK", 
    "CLAVICLE_LEFT", "SHOULDER_LEFT", "ELBOW_LEFT", "WRIST_LEFT", "HAND_LEFT", "HANDTIP_LEFT", "THUMB_LEFT", 
    "CLAVICLE_RIGHT", "SHOULDER_RIGHT", "ELBOW_RIGHT", "WRIST_RIGHT", "HAND_RIGHT", "HANDTIP_RIGHT", "THUMB_RIGHT", 
    "HIP_LEFT", "KNEE_LEFT", "ANKLE_LEFT", "FOOT_LEFT", 
    "HIP_RIGHT", "KNEE_RIGHT", "ANKLE_RIGHT", "FOOT_RIGHT", 
    "HEAD", "NOSE", "EYE_LEFT", "EAR_LEFT", "EYE_RIGHT", "EAR_RIGHT"
]

# 各関節に対応する色
joint_colors = {
    "PELVIS": "navy", "SPINE_NAVAL": "blue", "SPINE_CHEST": "dodgerblue", "NECK": "deepskyblue", 
    "CLAVICLE_LEFT": "limegreen", "SHOULDER_LEFT": "forestgreen", "ELBOW_LEFT": "mediumseagreen", 
    "WRIST_LEFT": "seagreen", "HAND_LEFT": "green", "HANDTIP_LEFT": "darkgreen", "THUMB_LEFT": "lightgreen", 
    "CLAVICLE_RIGHT": "hotpink", "SHOULDER_RIGHT": "red", "ELBOW_RIGHT": "orangered", 
    "WRIST_RIGHT": "firebrick", "HAND_RIGHT": "darkred", "HANDTIP_RIGHT": "crimson", "THUMB_RIGHT": "salmon", 
    "HIP_LEFT": "orange", "KNEE_LEFT": "darkorange", "ANKLE_LEFT": "chocolate", "FOOT_LEFT": "saddlebrown", 
    "HIP_RIGHT": "purple", "KNEE_RIGHT": "mediumpurple", "ANKLE_RIGHT": "darkviolet", "FOOT_RIGHT": "indigo", 
    "HEAD": "gold", "NOSE": "yellow", "EYE_LEFT": "khaki", "EAR_LEFT": "goldenrod", 
    "EYE_RIGHT": "khaki", "EAR_RIGHT": "goldenrod"
}

# 各点の数（Azure Kinect の定義）
joint_count = 32

def load_data(date_folder):
    """ 指定した日付フォルダ内のすべてのCSVファイルを取得し、ラベルごとにデータを整理 """
    base_path = os.path.join("temp", date_folder)
    data = {}

    if not os.path.exists(base_path):
        print(f"指定されたフォルダ '{base_path}' が見つかりません。")
        return data

    for time_folder in os.listdir(base_path):
        file_path = os.path.join(base_path, time_folder, "0", "pos.csv")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path, header=None)

            if df.empty:
                print(f"警告: {file_path} が空です。スキップします。")
                continue  # 空のファイルはスキップ

            label = df.iloc[0, 0]  # 各CSVのラベル番号

            if label not in data:
                data[label] = []
            data[label].append(df)

    return data

def compute_statistics(data):
    """ 各ラベルごとに統計情報を算出 """
    stats = {}

    for label, df_list in data.items():
        all_x, all_y, all_z = [], [], []

        for df in df_list:
            for i in range(joint_count):
                x = df.iloc[:, 2 + i * 3].dropna()
                y = df.iloc[:, 3 + i * 3].dropna()
                z = df.iloc[:, 4 + i * 3].dropna()

                all_x.extend(x)
                all_y.extend(y)
                all_z.extend(z)

        all_x, all_y, all_z = np.array(all_x), np.array(all_y), np.array(all_z)

        if all_x.size == 0 or all_y.size == 0 or all_z.size == 0:
            print(f"警告: ラベル {label} のデータが不足しているため、統計情報を計算できません。")
            stats[label] = {"mean_std": np.nan, "mean_range": np.nan}
            continue

        std_values = []
        range_values = []

        for i in range(joint_count):
            x = np.array([df.iloc[:, 2 + i * 3].dropna() for df in df_list]).flatten()
            y = np.array([df.iloc[:, 3 + i * 3].dropna() for df in df_list]).flatten()
            z = np.array([df.iloc[:, 4 + i * 3].dropna() for df in df_list]).flatten()

            if x.size == 0 or y.size == 0 or z.size == 0:
                continue  # データがない場合はスキップ

            std_x, std_y, std_z = np.nanstd(x), np.nanstd(y), np.nanstd(z)
            range_x = np.nanmax(x) - np.nanmin(x) if x.size > 0 else np.nan
            range_y = np.nanmax(y) - np.nanmin(y) if y.size > 0 else np.nan
            range_z = np.nanmax(z) - np.nanmin(z) if z.size > 0 else np.nan

            std_values.append(np.mean([std_x, std_y, std_z]))
            range_values.append(np.mean([range_x, range_y, range_z]))

        stats[label] = {
            "mean_std": np.nanmean(std_values) if std_values else np.nan,
            "mean_range": np.nanmean(range_values) if range_values else np.nan
        }

    return stats

def plot_statistics(ax, stats):
    """ ラベルごとの統計情報を棒グラフで表示 """
    labels = list(stats.keys())
    mean_std = [stats[label]["mean_std"] for label in labels]
    mean_range = [stats[label]["mean_range"] for label in labels]

    x_positions = np.arange(len(labels))

    ax.bar(x_positions - 0.2, mean_std, 0.4, label="Mean Standard Deviation", color="royalblue")
    ax2 = ax.twinx()
    ax2.bar(x_positions + 0.2, mean_range, 0.4, label="Mean Range", color="tomato")

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Mean Standard Deviation", color="royalblue")
    ax2.set_ylabel("Mean Range", color="tomato")

    ax.legend(loc="upper left", fontsize=10)
    ax2.legend(loc="upper right", fontsize=10)

    ax.set_title("Statistics of Joint Positions")

def plot_3d_scatter(ax, data, current_label):
    """ 3D散布図を表示 """
    ax.clear()  # プロットをクリア

    df_list = data[current_label]
    for df in df_list:
        for i in range(joint_count):
            joint_name = joint_names[i]
            x = df.iloc[:, 2 + i * 3]
            y = df.iloc[:, 3 + i * 3]
            z = df.iloc[:, 4 + i * 3]

            # 各点に名前と色を設定
            ax.scatter(x, y, z, label=joint_name, color=joint_colors[joint_name], alpha=0.7)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"3D Scatter Plot (Label: {current_label})")
    ax.legend(loc="upper left", fontsize=8)

def update_plot(event, data, ax2, current_label_text):
    """ ボタンが押されたときにプロットを更新 """
    current_label = int(current_label_text[0])  # ラベル番号を取得
    label_list = list(data.keys())
    
    # ラベル番号の更新
    next_label = label_list[(label_list.index(current_label) + 1) % len(label_list)]
    current_label_text[0] = str(next_label)  # 次のラベル番号を保存
    
    plot_3d_scatter(ax2, data, next_label)  # 散布図を更新
    plt.draw()

# メイン処理
date_folder = input("日付フォルダ名を入力してください（例: 20250303）: ")
data = load_data(date_folder)
if not data:
    print("データが見つかりませんでした。")
else:
    stats = compute_statistics(data)

    # サブプロットの作成（1行2列）
    fig = plt.figure(figsize=(14, 7))

    # 左側に統計グラフ
    ax1 = fig.add_subplot(121)
    plot_statistics(ax1, stats)

    # 右側に3D散布図
    ax2 = fig.add_subplot(122, projection='3d')
    current_label = list(data.keys())[0]  # 最初のラベルを初期選択
    plot_3d_scatter(ax2, data, current_label)

    # ボタンの作成
    ax_button = fig.add_axes([0.85, 0.05, 0.1, 0.075])  # ボタンの位置
    button = Button(ax_button, "Next Label")
    current_label_text = [str(current_label)]  # 現在のラベルを格納
    button.on_clicked(lambda event: update_plot(event, data, ax2, current_label_text))

    plt.tight_layout()
    plt.show()
