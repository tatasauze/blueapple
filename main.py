# HSV的轉換，更換color space之後，將附檔圖片內的紅蘋果(紅色色調區域)，轉變成藍蘋果(藍色色調)。

import numpy as np
import matplotlib.pyplot as plt
import cv2


class apple():
    def __init__(self,path:str):
        self.path = path
        self.piexl = None

        self.R = None
        self.G = None
        self.B = None

        self.H = None
        self.S = None
        self.V = None
    
    # load_img()
    def load_img(self):
        '''
        func: load png
        '''
        bgr_img = cv2.imread(self.path)
        rgb_img = cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGB)
        self.piexl = rgb_img
        
        # 3 channels to R G B
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
        C_high = np.max(self.R,self.G,self.B)
        C_low = np.min(self.R,self.G,self.B)
        C_rng = C_high - C_low

        self.V = C_high
        self.S = C_rng / C_high

        # 1. normalization of R G B
        R_ = (self.R - C_low) / C_rng
        G_ = (self.G - C_low) / C_rng
        B_ = (self.B - C_low) / C_rng

        # 2. set H'
        if C_high == self.R:
            self.H = B_ - G_
        elif C_high == self.G:
            self.H = 2 + R_ - B_
        elif C_high == self.B:
            self.H = 4 + G_ - R_
        else:
            print("something went wrong")
        
        # 3. scale to [0,1)
        if self.H <0:
            self.H += 6
            self.H /= 6
        else:
            self.H /= 6
        

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
        if c1 == 0:
            self.R, self.G, self.B = v, z, x
        elif c1 ==1:
            self.R, self.G, self.B = y, v, x
        elif c1 ==2:
            self.R, self.G, self.B = x, v, z
        elif c1 ==3:
            self.R, self.G, self.B = x, y, v
        elif c1 ==4:
            self.R, self.G, self.B = z, x, v
        elif c1 ==5:
            self.R, self.G, self.B = v, x, y
        
        # 4. scale to 0~255
        self.B = min(255*self.B,255)
        self.G = min(255*self.G,255)
        self.R = min(255*self.R,255)

    # HSV_shift()
    def HSV_shift(self,switch_degree:int):
        '''
        func: change the color by shifting the hue value in degree
        Args:
            'R2B': 240 degree
        '''
        self.H = np.mod(self.H + switch_degree/360)
    
    # RGB2pixel()
    def RGB2pixel(self):
        '''
        converrt RGB to pixel
        '''
        self.piexl = np.dstack((self.R,self.G,self.B))

if __name__=="main":
    # init
    color_transformer = apple("apple.png")
    color_transformer.load_img()
    color_transformer.RGB2HSV()
    color_transformer.HSV_shift(240)
    color_transformer.HSV2RGB()
    color_transformer.RGB2pixel()
    # show img
    plt.imshow(color_transformer.piexl)
    plt.show()
    # save as png
    plt.imsave("apple_blue.png",color_transformer.piexl)
