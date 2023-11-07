import numpy as np
import matplotlib.pyplot as plt
import mss
import cv2

cap = mss.mss()
game_location = {'top': 275, 'left': 510, 'width': 343, 'height': 103}
new_dimensions = (60, 20)
# i=0


while True:
    raw = np.array(cap.grab(game_location))[:,:,:3].astype(np.uint8)
    raw = np.mean(raw, axis=-1).astype(np.uint8)
    _, raw = cv2.threshold(raw, 200, 255, cv2.THRESH_BINARY)
    raw2 = raw.copy()
    _, thresh = cv2.threshold(raw2, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 250
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    border = 8
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(raw2, (x- border, y - border), (x + w + border, y + h + border), (0, 0, 0), -1)

    raw2 = cv2.resize(raw2, new_dimensions, interpolation=cv2.INTER_LANCZOS4)
    _, raw2 = cv2.threshold(raw2, 195, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(cv2.bitwise_not(raw2), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 1
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    filtered_contours = filtered_contours[::-1]

    if (len(filtered_contours) < 1): 
        _ = (100,100,100, 100,100,100)
    
    elif (len(filtered_contours) == 1):
        x, y, w, h = cv2.boundingRect(filtered_contours[0])
        _ = (x,h,w, 100,100,100)
    else:
        x1, y1, w1, h1 = cv2.boundingRect(filtered_contours[0])
        x2, y2, w2, h2 = cv2.boundingRect(filtered_contours[1])
        _ = (x1,h1,w1,x2,h2,w2)

    

    # for contour in filtered_contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(raw2, (x, y), (x + w, y + h), (100, 100, 100), -1)
    #     if (k<2):
    #         print(f"Object{k}: Distance{x}, Height: {h}, Width: {w}")
    #     k+=1