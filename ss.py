import numpy as np
import matplotlib.pyplot as plt
import mss
import cv2

cap = mss.mss()
game_location = {'top': 275, 'left': 501, 'width': 343, 'height': 103}
raw = np.array(cap.grab(game_location))[:,:,:3].astype(np.uint8)
print(raw.shape)
raw = np.mean(raw, axis=-1).astype(np.uint8)
cv2.imwrite("kill.png", raw)