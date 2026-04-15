# HSV的轉換，更換color space之後，將附檔圖片內的紅蘋果(紅色色調區域)，轉變成藍蘋果(藍色色調)。
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class apple():
    def __init__(self,pixel=None,R=None,G=None,B=None,H=None,S=None,V=None):
        
        self.pixel = pixel
        self.R = R
        self.G = G
        self.B = B

        self.H = H
        self.S = S
        self.V = V
    
    # load_img()
    def load_img(self,path:str):
        '''
        func: load png
        '''
        rgb_img = plt.imread(path)
        print(rgb_img.shape)
        # to ensure img is 3 channels
        if rgb_img.shape[2] == 4:
            rgb_img = rgb_img[:,:,3]
        
        self.pixel = rgb_img

        self.R = rgb_img[:,:,0]
        self.G = rgb_img[:,:,1]
        self.B = rgb_img[:,:,2]


    # RGB2HSV()
    def RGB2HSV(self):
        '''
        func: change rgb space to hsv space
        Args:
            R, G, B:numpy array of pixel in rgb form
        Return:
            H, S, V:numpy array of pixel in hsv form
        '''
        C_high = np.maximum(np.maximum(self.R,self.G),self.B)
        C_low = np.minimum(np.minimum(self.R,self.G),self.B)
        C_rng = C_high - C_low

        self.V = C_high
        self.S = np.where(C_high==0,0,C_rng / (C_high+1e-10))

        # 防止除0
        eps = 1e-10
        # 1. normalization of R G B
        R_ = (self.R - C_low) / (C_rng + eps)
        G_ = (self.G - C_low) / (C_rng + eps)
        B_ = (self.B - C_low) / (C_rng + eps)

        # 2. set H'
        self.H = np.zeros_like(C_high)
        self.H = np.where(C_high == self.R, B_ - G_, 
           np.where(C_high == self.G, 2 + R_ - B_,
           np.where(C_high == self.B, 4 + G_ - R_, self.H)))
        # 3. scale to [0,1)
        self.H = np.where(self.H <0, self.H + 6, self.H)
        self.H = self.H / 6        
        
    # HSV2RGB()
    def HSV2RGB(self):
        '''
        func: change hsv space to rgb space
        Args:
            H, S, V:numpy array of pixel in rgb form
        Return:
            R, G, B:numpy array of pixel in hsv form
        '''
        # 1. check where the point is in the hexagon
        H = self.H
        H_ = np.mod(6*H,6)
        c1 = np.floor(H_) #c1 = 0,1,2,3,4,5
        c2 = H_ - c1
        
        # 2. set the RGB value tone
        v = self.V # RGB 中的最大值
        x = (1-self.S) * v # RGB 中的最小值
        z = (1-(1-c2)*self.S) * v # 比例上升
        y = (1 - c2*self.S) * v # 比例下降

        '''
        switch (c1) {
         case 0: r = V; g = z; b = x; break;
         case 1: r = y; g = V; b = x; break;
         case 2: r = x; g = V; b = z; break;
         case 3: r = x; g = y; b = V; break;
         case 4: r = z; g = x; b = V; break;
         case 5: r = V; g = x; b = y; break;
         }
        '''
        # 3. distribute the value to RGB
        # if c1 == 0:
        #     self.R, self.G, self.B = v, z, x
        # elif c1 ==1:
        #     self.R, self.G, self.B = y, v, x
        # elif c1 ==2:
        #     self.R, self.G, self.B = x, v, z
        # elif c1 ==3:
        #     self.R, self.G, self.B = x, y, v
        # elif c1 ==4:
        #     self.R, self.G, self.B = z, x, v
        # elif c1 ==5:
        #     self.R, self.G, self.B = v, x, y
        
        self.R = np.select([c1==0,c1==1,c1==2,c1==3,c1==4,c1==5],
                            [x,y,x,x,z,v])
        self.G = np.select([c1==0,c1==1,c1==2,c1==3,c1==4,c1==5],
                            [z,v,v,y,x,x])
        self.B = np.select([c1==0,c1==1,c1==2,c1==3,c1==4,c1==5],
                            [x,x,z,v,v,y])

        # 4. scale to 0~255
        self.R = np.clip(255*self.R,0,255)
        self.G = np.clip(255*self.G,0,255)
        self.B = np.clip(255*self.B,0,255)

    # HSV_shift()
    def HSV_shift(self,switch_degree:int):
        '''
        func: change the color by shifting the hue value in degree
        Args:
            'R2B': 240 degree
        '''
        self.H = np.mod(self.H + switch_degree/360,1)
    
    # RGB2pixel()
    def RGB2pixel(self):
        '''
        converrt RGB to pixel
        '''
        self.pixel = np.dstack((self.R,self.G,self.B))

# select_region()
def select_region(path:str):
    '''
    先將原圖的紅色框出來再轉換
    Args:
        path: img
    Returns:
        output_img: img only change color red into blue
    '''
    red_apple = apple()
    red_apple.load_img(path)
    pixel = red_apple.pixel
    
    # 紅色色相範圍（0°~30°）
    red_apple.RGB2HSV()
    H = red_apple.H
    S = red_apple.S
    V = red_apple.V
    if ((H != np.zeros_like(H)) & (S != np.zeros_like(S)) & (V != np.zeros_like(V))).any():
        red_mask = ((H < 0.111) | (H > 0.90)) & (S > 0.2) & (V > 0.1)
        # red_mask = (H < 0.083) & (S > 0.4) & (V > 0.3) #numpy mask
    else:
        print("mask get wrong")
    
    # transform 
    trans_apple = apple()
    trans_apple.pixel = pixel.copy()
    trans_apple.R = pixel[:,:,0].copy()
    trans_apple.G = pixel[:,:,1].copy()
    trans_apple.B = pixel[:,:,2].copy()
    trans_apple.RGB2HSV()
    trans_apple.HSV_shift(240)
    trans_apple.HSV2RGB()
    trans_apple.RGB2pixel()

    # replace pixel 只替換紅色區域
    output_img = pixel.copy()
    
    # 將 trans_apple.pixel 轉換回 0~1 範圍
    trans_pixel_normalized = trans_apple.pixel / 255.0
    output_img[red_mask] = trans_pixel_normalized[red_mask]
    
    return output_img

if __name__=="__main__":
    # init
    # color_transformer = apple()
    # color_transformer.load_img("red_apple.png")
    # color_transformer.RGB2HSV()
    # color_transformer.HSV_shift(240)
    # color_transformer.HSV2RGB()
    # color_transformer.RGB2pixel()
    # # show img
    # # plt.imshow(color_transformer.pixel)
    # plt.show()
    # # save as png
    # plt.imsave("blue_apple_gobal_change.png",color_transformer.pixel/255.0)

    path = 'red_apple.png'
    output_img = select_region(path)
    plt.imsave("blue_apple_select_region.png",output_img)

    # 檢視原圖RGB

    # img = plt.imread("red_apple.png")
    # rgb_img =  (img*255).astype(np.int16)
    # r_channel = rgb_img[:,:,0]
    # g_channel = rgb_img[:,:,1]
    # b_channel = rgb_img[:,:,2]

    # # select red color
    # mask = np.where((r_channel>200)&(g_channel<100)&(b_channel<100),1,0)
    # r_channel.to_csv("r_channel.csv")
    