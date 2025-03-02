from os import path

import requests
import time
import cv2
import numpy as np
from screeninfo import get_monitors


REFRESH_INTERVAL = 3600 * 4
SLIDESHOW_INTERVAL = 2
FIRST_FRAME_INTERVAL = 3
RATIO = 8 / 9
NUM_IMAGES = 33

base_url = "https://static-weather.services.siag.it/"
img_url = "sys/wforecast{}.jpg"


def getimage(num):
    r_session = requests.session()
    try:
        response = r_session.get(base_url + img_url.format(num))
        file = open("weatherimg/img{}.jpg".format(num), "wb")
        file.write(response.content)
        file.close()
        print(f"img {num} succeeded")
    except:
        print(f"img {num} failed")
        pass


def getimages():
    return
    for i in range(NUM_IMAGES):
        getimage(i)


def main():
    monitor = get_monitors()[0]
    window_size = (monitor.width // 2, monitor.height)

    cnt = 0
    cv2.namedWindow("Wetter", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Wetter", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    lastrefresh = 0

    while True:
        filename = f"weatherimg/img{cnt}.jpg"
        if path.isfile(filename):
            img = cv2.imread(filename)
        else:
            getimage(cnt)
            cnt = (cnt + 1) % NUM_IMAGES
            continue

        h, w = img.shape[:2]
        img[200:203, 545:558, :] = [0, 0, 255]
        img[195:208, 550:553, :] = [0, 0, 255]

        if w/RATIO < h:
            nh, nw = h, int(h * RATIO)
            border = np.ones(shape=(nh, nw, 3), dtype=np.uint8) * 255
        else:
            nh, nw = int(w / RATIO), w
            border = np.ones(shape=(nh, nw, 3), dtype=np.uint8) * 255

        xoff, yoff = int((nw - w) / 2), int((nh - h) / 2)
        border[yoff:h+yoff, xoff:w+xoff, :] = img
        border[nh - 20:, :int(nw / NUM_IMAGES * (cnt + 1)), :] = [0, 0, 255]
        border = cv2.resize(border, window_size, interpolation=cv2.INTER_AREA)

        cv2.imshow("Wetter", border)
        cv2.moveWindow("Wetter", 0, 0)
        cv2.waitKey(SLIDESHOW_INTERVAL)
        time.sleep(SLIDESHOW_INTERVAL)
        if cnt == 0 and time.time() - lastrefresh > REFRESH_INTERVAL:
            lastrefresh = time.time()
            getimages()
        if cnt == 0:
            time.sleep(FIRST_FRAME_INTERVAL)
        cnt = (cnt + 1) % NUM_IMAGES


if __name__ == '__main__':
    main()
