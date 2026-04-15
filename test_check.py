import matplotlib.pyplot as plt
import numpy as np

# 檢查 check0.png（原始像素）
img0 = plt.imread('check0.png')
print(f"check0.png 範圍: {img0.min()} ~ {img0.max()}")
print(f"check0.png dtype: {img0.dtype}")

# 檢查 check.png（替換後像素）
img1 = plt.imread('check.png')
print(f"check.png 範圍: {img1.min()} ~ {img1.max()}")
print(f"check.png dtype: {img1.dtype}")

# 檢查原圖
original = plt.imread('red_apple.png')
print(f"原圖範圍: {original.min()} ~ {original.max()}")
print(f"原圖 dtype: {original.dtype}")
