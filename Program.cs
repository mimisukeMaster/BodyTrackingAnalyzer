using Microsoft.Azure.Kinect.BodyTracking;
using Microsoft.Azure.Kinect.Sensor;
using System;
using System.Threading.Tasks;

namespace Csharp_3d_viewer
{
    class Program
    {
        static async Task Main()
        {
            using (var visualizerData = new VisualizerData())
            {
                var renderer = new PosSaver(visualizerData);

                renderer.StartVisualizationThread();

                // Open device.
                using (Device device = Device.Open())
                {
                    device.StartCameras(new DeviceConfiguration()
                    {
                        ColorFormat = ImageFormat.ColorBGRA32,
                        ColorResolution = ColorResolution.R720p,
                        DepthMode = DepthMode.NFOV_Unbinned,
                        SynchronizedImagesOnly = true,
                        WiredSyncMode = WiredSyncMode.Standalone,
                        CameraFPS = FPS.FPS15
                    });

                    var deviceCalibration = device.GetCalibration();
                    var transformation = deviceCalibration.CreateTransformation();
                    PointCloud.ComputePointCloudCache(deviceCalibration);

                    using (Tracker tracker = Tracker.Create(deviceCalibration, new TrackerConfiguration() { ProcessingMode = TrackerProcessingMode.Gpu, SensorOrientation = SensorOrientation.Default }))
                    {
                        while (renderer.IsActive)
                        {
                            using (Capture sensorCapture = await Task.Run(() => device.GetCapture()).ConfigureAwait(true))
                            {
                                // Queue latest frame from the sensor.
                                tracker.EnqueueCapture(sensorCapture);
                            }

                            // Try getting latest tracker frame.
                            using (Frame frame = tracker.PopResult(TimeSpan.Zero, throwOnTimeout: false))
                            {
                                if (frame != null)
                                {
                                    // Save this frame for visualization in Renderer.

                                    // One can access frame data here and extract e.g. tracked bodies from it for the needed purpose.
                                    // Instead, for simplicity, we transfer the frame object to the rendering background thread.
                                    // This example shows that frame popped from tracker should be disposed. Since here it is used
                                    // in a different thread, we use Reference method to prolong the lifetime of the frame object.
                                    // For reference on how to read frame data, please take a look at Renderer.NativeWindow_Render().
                                    visualizerData.Frame = frame.Reference();
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
