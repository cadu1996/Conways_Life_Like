from scipy.signal import correlate2d
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Conway():
    def __init__(self, B=[3], S=[2,3]):
        ### Rules Survival and Born ###
        self.B = B  
        self.S = S

        ### Generation Matrix ###
        self.grid = np.random.randint(2, size=(270,480), dtype=np.int0)
        
    def next_generation(self):
        ### Create a kernel ###
        kernel = np.ones((3,3))
        kernel[1,1] = 0

        ### Apply Kernel in Grid ###
        neighbours = correlate2d(self.grid, kernel, 'same')

        ### Apply Rules in grid ###
        old_grid = self.grid.copy()
        self.grid[(old_grid == 1) & (~np.isin(neighbours,self.S))] = 0
        self.grid[(old_grid == 0) & (np.isin(neighbours,self.B))] = 1

    def write_video(self, title="teste.mp4",videodims=(1920,1080), fps=10, generation=1000):
        ### Inicialization Record Video ###
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')                        ## Define Codec to MP4
        video = cv2.VideoWriter(title, fourcc, fps, videodims)

        ### Loop to record frame in video ###
        for i in range(generation):
            self.next_generation()                                      
            plt.imsave("frame.png", self.grid)                          ## Save frame with image
            img = cv2.imread("frame.png")                               ## Read image 
            img = cv2.resize(img, videodims)                            ## Resize image to 1920x1080

            ### Write generation in video ###
            font = cv2.FONT_HERSHEY_SIMPLEX             
            cv2.putText(img, "generation: {0}".format(i+1),(0,100), font, 2, (255,255,255), 2, cv2.LINE_AA)
    
            ### Write image in video ###
            video.write(img)
        
        ### Save video ###
        video.release()
    
    def main(self):
        self.write_video()

if __name__ == '__main__':
    run = Conway(B=[3], S=[2,3])
    run.main()