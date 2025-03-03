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

    # 3Dプロットを作成
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')

    all_x, all_y, all_z = [], [], []

    for label in labels:
        df_label = df[df.iloc[:, 0] == label]

        # 各点のXYZ座標を取得
        for i, joint_name in enumerate(joint_names):
            x = df_label.iloc[:, 2 + i * 3]
            y = df_label.iloc[:, 3 + i * 3]
            z = df_label.iloc[:, 4 + i * 3]
            ax.scatter(x, y, z, color=joint_colors[joint_name], label=f"{joint_name}" if label == labels[0] else "")

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

    # グラフ内に統計情報を描画
    stats_text = f"standard deviation: X={std_x:.2f}, Y={std_y:.2f}, Z={std_z:.2f}\n" \
                f"range: X={range_x:.2f}, Y={range_y:.2f}, Z={range_z:.2f}"
    
    ax.text2D(0.25, 0.0, stats_text, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Scatter Plot of Joint Positions")
    ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.13, 1.15)) 
    plt.show()

# 使用例
base_folder = input("ベースフォルダ名を入力してください: ")
sub_folder = input("サブフォルダ名を入力してください: ")
plot_scatter_from_csv(base_folder, sub_folder)
