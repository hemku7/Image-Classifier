import os
import random
import numpy as np
import cv2

class ImageHandler():

    def __init__(self, directory_path=None):

        self.directory_path = directory_path
        self.images = []
        image_extensions = {".jpg", ".jpeg", ".png",
                            ".gif", ".bmp", ".tiff", ".webp"}

        for i in os.listdir(self.directory_path):
            img = os.path.join(self.directory_path, i)
            if os.path.isfile(img) and os.path.splitext(img)[1] in image_extensions:
                self.images.append(img)

    def get_random_image(self):
        return random.choice(self.images)
    
    def get_image_as_numpy(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (226, 226))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
        return img