import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 各点の名前（Azure Kinectの定義）
joint_names = [
    "PELVIS", "SPINE_NAVAL", "SPINE_CHEST", "NECK",
    "CLAVICLE_LEFT", "SHOULDER_LEFT", "ELBOW_LEFT", "WRIST_LEFT", "HAND_LEFT", "HANDTIP_LEFT", "THUMB_LEFT",
    "CLAVICLE_RIGHT", "SHOULDER_RIGHT", "ELBOW_RIGHT", "WRIST_RIGHT", "HAND_RIGHT", "HANDTIP_RIGHT", "THUMB_RIGHT",
    "HIP_LEFT", "KNEE_LEFT", "ANKLE_LEFT", "FOOT_LEFT",
    "HIP_RIGHT", "KNEE_RIGHT", "ANKLE_RIGHT", "FOOT_RIGHT",
    "HEAD", "NOSE", "EYE_LEFT", "EAR_LEFT", "EYE_RIGHT", "EAR_RIGHT"
]

# わかりやすい色分け（RGB）
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

def plot_scatter_from_csv(base_folder, sub_folder):
    # ファイルパスを構築
    file_path = os.path.join("temp", base_folder, sub_folder, "0", "pos.csv")

    # CSVデータの読み込み
    df = pd.read_csv(file_path, header=None)

    # ラベル番号を取得
    labels = df.iloc[:, 0].unique()

    # 図全体のレイアウトを作成（1行2列）
    fig = plt.figure(figsize=(14, 6))

    # 3Dプロットを作成（左側）
    ax1 = fig.add_subplot(121, projection='3d')
    all_x, all_y, all_z = [], [], []

    for label in labels:
        df_label = df[df.iloc[:, 0] == label]

        # 各点のXYZ座標を取得
        for i, joint_name in enumerate(joint_names):
            x = df_label.iloc[:, 2 + i * 3]
            y = df_label.iloc[:, 3 + i * 3]
            z = df_label.iloc[:, 4 + i * 3]
            ax1.scatter(x, y, z, color=joint_colors[joint_name], label=f"{joint_name}" if label == labels[0] else "")

            # NaN(欠損値)を除外してリストに追加
            all_x.extend(x.dropna())
            all_y.extend(y.dropna())
            all_z.extend(z.dropna())

    # 統計情報の計算
    all_x, all_y, all_z = np.array(all_x), np.array(all_y), np.array(all_z)

    if all_x.size > 0 and all_y.size > 0 and all_z.size > 0:
        std_x, std_y, std_z = np.nanstd(all_x), np.nanstd(all_y), np.nanstd(all_z)
        range_x, range_y, range_z = np.nanmax(all_x) - np.nanmin(all_x), np.nanmax(all_y) - np.nanmin(all_y), np.nanmax(all_z) - np.nanmin(all_z)
    else:
        std_x, std_y, std_z = 0, 0, 0
        range_x, range_y, range_z = 0, 0, 0

    # 3Dグラフの設定
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Z")
    ax1.set_title("3D Scatter Plot of Joint Positions")
    ax1.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.15, 1.1))

    # 統計情報の棒グラフを作成（右側）
    ax2 = fig.add_subplot(122)
    categories = ['X', 'Y', 'Z']

    std_values = [std_x, std_y, std_z]
    range_values = [range_x, range_y, range_z]

    x_positions = np.arange(len(categories))

    # 2軸を作成
    ax2.bar(x_positions - 0.2, std_values, 0.4, label="Standard Deviation", color="royalblue")
    ax3 = ax2.twinx()
    ax3.bar(x_positions + 0.2, range_values, 0.4, label="Range", color="tomato")

    # 軸とラベル設定
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(categories)
    ax2.set_ylabel("Standard Deviation", color="royalblue")
    ax3.set_ylabel("Range", color="tomato")

    # 凡例をそれぞれの軸で追加
    ax2.legend(loc="upper left", fontsize=10)
    ax3.legend(loc="upper right", fontsize=10)

    ax2.set_title("Statistics of Joint Positions")

    plt.tight_layout()
    plt.show()

# 使用例
base_folder = input("ベースフォルダ名を入力してください: ")
sub_folder = input("サブフォルダ名を入力してください: ")
plot_scatter_from_csv(base_folder, sub_folder)
