import cv2
import numpy as np


def histogram_encoder(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return {
        "blue": np.concatenate(
            cv2.calcHist(
                images=[img_cv], 
                channels=[0], 
                mask=None,
                histSize=[4],
                ranges=[0, 256]
                )
            ).ravel().astype(int).tolist(),

        "green": np.concatenate(
            cv2.calcHist(
                images=[img_cv], 
                channels=[1], 
                mask=None,
                histSize=[4],
                ranges=[0, 256]
                )
            ).ravel().astype(int).tolist(),

        "red": np.concatenate(
            cv2.calcHist(
                images=[img_cv], 
                channels=[2], 
                mask=None,
                histSize=[4],
                ranges=[0, 256]
                )
            ).ravel().astype(int).tolist(),
    }