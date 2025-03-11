using Microsoft.Azure.Kinect.BodyTracking;
using OpenGL;
using OpenGL.CoreUI;
using System;
using System.IO;
using System.Collections.Generic;
using System.Numerics;
using System.Threading.Tasks;

namespace Csharp_3d_viewer
{
    public class PosSaver
    {
        // GUI描画用のレンダラー群
        private SphereRenderer SphereRenderer;
        private CylinderRenderer CylinderRenderer;
        private PointCloudRenderer PointCloudRenderer;
        private List<Vertex> pointCloud = null;

        private readonly VisualizerData visualizerData;
        public PosSaver(VisualizerData visualizerData)
        {
            this.visualizerData = visualizerData;

            // 実行開始時に一意のCSVファイル名を生成（tempフォルダ直下）
            csvFileName = $@"{path}\pos_{DateTime.Now.ToString("yyyyMMdd_HHmmssfff")}.csv";
            
            // tempフォルダが存在しなければ作成
            Directory.CreateDirectory(path);
        }

        public bool IsActive { get; private set; }
        public bool IsHuman { get; private set; } = false;

        // ラベル用の難易度指定
        public int Label { get; private set; } = 0;
        private bool isLabelSet = false;

        // 出力先フォルダ（temp直下にCSVを作成する）
        public static string path = @"..\..\..\..\..\temp";

        // 実行ごとに一意なCSVファイル名
        private readonly string csvFileName;

        public DateTime now = DateTime.Now;

        public void SetLabel(int label)
        {
            Label = label;
        }

        public void StartVisualizationThread()
        {
            Task.Run(() =>
            {
                using (NativeWindow nativeWindow = NativeWindow.Create())
                {
                    IsActive = true;
                    nativeWindow.ContextCreated += NativeWindow_ContextCreated;
                    nativeWindow.Render += NativeWindow_Render;
                    nativeWindow.KeyDown += (object obj, NativeWindowKeyEventArgs e) =>
                    {
                        switch (e.Key)
                        {
                            case KeyCode.Escape:
                                nativeWindow.Stop();
                                IsActive = false;
                                break;

                            case KeyCode.F:
                                nativeWindow.Fullscreen = !nativeWindow.Fullscreen;
                                break;
                        }
                    };
                    nativeWindow.Animation = true;

                    nativeWindow.Create(0, 0, 640, 480, NativeWindowStyle.Overlapped);

                    nativeWindow.Show();

                    // 別スレッドでユーザーからのラベル入力を受け付ける
                    GetUserModeInput();

                    nativeWindow.Run();
                }
            });
        }

        private void GetUserModeInput()
        {
            while (!isLabelSet)
            {
                Console.Write("ラベルの番号を入力してください（整数値）: ");
                string input = Console.ReadLine();

                if (int.TryParse(input, out int label))
                {
                    SetLabel(label);
                    Console.WriteLine($"ラベル番号 {label} の計測を行います");
                    isLabelSet = true;
                }
                else Console.WriteLine("無効な入力\n整数値を入力してください");
            }
        }

        private void NativeWindow_ContextCreated(object sender, NativeWindowEventArgs e)
        {
            Gl.ReadBuffer(ReadBufferMode.Back);

            Gl.ClearColor(0.0f, 0.0f, 0.0f, 1.0f);

            Gl.Enable(EnableCap.Blend);
            Gl.BlendFunc(BlendingFactor.SrcAlpha, BlendingFactor.OneMinusSrcAlpha);

            Gl.LineWidth(2.5f);

            CreateResources();
        }

        private static float ToRadians(float degrees)
        {
            return degrees / 180.0f * (float)Math.PI;
        }

        public void NativeWindow_Render(object sender, NativeWindowEventArgs e)
        {
            using (var lastFrame = visualizerData.TakeFrameWithOwnership())
            {
                if (lastFrame == null) return;

                NativeWindow nativeWindow = (NativeWindow)sender;

                // GUI描画処理
                Gl.Viewport(0, 0, (int)nativeWindow.Width, (int)nativeWindow.Height);
                Gl.Clear(ClearBufferMask.ColorBufferBit);

                var proj = Matrix4x4.CreatePerspectiveFieldOfView(ToRadians(65.0f), (float)nativeWindow.Width / nativeWindow.Height, 0.1f, 150.0f);
                var view = Matrix4x4.CreateLookAt(Vector3.Zero, Vector3.UnitZ, -Vector3.UnitY);

                if (lastFrame.NumberOfBodies > 0)
                {
                    // レンダラーにカメラ情報を設定
                    SphereRenderer.View = view;
                    SphereRenderer.Projection = proj;

                    CylinderRenderer.View = view;
                    CylinderRenderer.Projection = proj;

                    PointCloudRenderer.View = view;
                    PointCloudRenderer.Projection = proj;

                    PointCloud.ComputePointCloud(lastFrame.Capture.Depth, ref pointCloud);
                    PointCloudRenderer.Render(pointCloud, new Vector4(1, 1, 1, 1));

                    IsHuman = true;

                    // １フレームごとに全ボディの情報を１つのCSVファイルに追記
                    using (var sw = new StreamWriter(csvFileName, append: true))
                    {
                        now = DateTime.Now;
                        string timeStamp = now.ToString("HHmmssfff");
                        // 先頭にモードとタイムスタンプを書き込む
                        sw.Write($"{Label}, {timeStamp}");

                        // 原則1人のみの座標を記録
                        // for (uint i = 0; i < lastFrame.NumberOfBodies; ++i)
                        
                        var skeleton = lastFrame.GetBodySkeleton(0);
                        var bodyId = lastFrame.GetBodyId(0);

                        for (int jointId = 0; jointId < (int)JointId.Count; ++jointId)
                        {
                            var joint = skeleton.GetJoint(jointId);
                            sw.Write($", {joint.Position.X}, {joint.Position.Y}, {joint.Position.Z}");

                            // GUI描画用
                            const float radius = 0.024f;
                            SphereRenderer.Render(joint.Position / 1000, radius, BodyColors.GetColorAsVector(bodyId));

                            if (JointConnections.JointParent.TryGetValue((JointId)jointId, out JointId parentId))
                            {
                                CylinderRenderer.Render(joint.Position / 1000, skeleton.GetJoint((int)parentId).Position / 1000, BodyColors.GetColorAsVector(bodyId));
                            }
                        }
                        sw.WriteLine();
                    }
                }
                else
                {
                    IsHuman = false;
                }
            }
        }

        private void CreateResources()
        {
            // GUI描画用リソースの初期化
            SphereRenderer = new SphereRenderer();
            CylinderRenderer = new CylinderRenderer();
            PointCloudRenderer = new PointCloudRenderer();
        }
    }
}
