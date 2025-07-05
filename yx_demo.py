# 测试相机
# from yx_predict_disparity import DisparityPredictor
# import torch
# import numpy as np
from yx_hik_depth_utils import HikStereoCamera
# import os

def main():
    # 初始化相机
    camera = HikStereoCamera()
    camera.open()

    # 初始化深度预测器
    # predictor = DisparityPredictor(ckpt_path="checkpoints/kitti.pth", out_dir="stereo_data/depth")

    # 采集并预测深度
    for i in range(10):  # 采集10帧
        left_tensor, right_tensor = camera.capture(save=True, save_dir="stereo_data", idx=i)
        # depth = predictor.predict(left_tensor, right_tensor)
        print(f"Frame {i}: Depth shape: {left_tensor.shape}")

    # 关闭相机
    camera.close()

if __name__ == "__main__":
    main()