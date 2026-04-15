import numpy as np
import matplotlib.pyplot as plt

# 測試問題
path = 'red_apple.png'
pixel = plt.imread(path)
print("原始像素範圍:", pixel.min(), "~", pixel.max())
print("原始像素 dtype:", pixel.dtype)
print("原始像素 shape:", pixel.shape)
