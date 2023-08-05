import numpy as np
import cv2

class Bipolarizer(np.ndarray):
    def __new__(cls, *args, filename=None, apply_median=True, iters=1, w=15, inverse=False):
        def median(img):
            kernel = np.ones((w, w), np.float32) / (w * w)
            for _ in range(iters):
                img = cv2.filter2D(img, -1, kernel)
            return img
        K=2
        img = cv2.imread(args[0] if filename is None else filename)
        img = median(img) if apply_median else img
        Z = img.reshape((-1,3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        avg_label = np.mean(center, axis=1)
        if avg_label[0]<avg_label[1]:
            center = np.uint8([[255, 255, 255],[0,0,0]])
        else:
            center = np.uint8([[0,0,0], [255, 255, 255]])
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))
        res2 = 255 - res2 if inverse else res2
        self = np.copy(res2)
        return (self)

