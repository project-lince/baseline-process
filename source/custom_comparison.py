import cv2
import numpy as np
import matplotlib.pyplot as plt
def pixel_diff(path1, path2):
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)
    image1 = cv2.resize(image1, None, fx=.5, fy=.5)
    image2 = cv2.resize(image2, None, fx=.5, fy=.5)
    difference = cv2.subtract(image1, image2)
    # difference = cv2.resize(difference, None, fx=.5, fy=.5)
    cv2.imshow("difference", difference)
    cv2.waitKey()
    cv2.destroyAllWindows()


def layout_diff():
    #using information from https://www.analyticsvidhya.com/blog/2019/03/opencv-functions-computer-vision-python/

    SHAPE_MIN_AREA = 0
    #using image segmentetaion mask
    path1 = "Image/google1.png"
    path2 = "Image/google2.png"
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)

    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)

    _, threshold = cv2.threshold(img1, 240, 255, cv2.THRESH_BINARY)
    contours1, hierarchy1 = cv2.findContours(threshold, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    _, threshold = cv2.threshold(img2, 240, 255, cv2.THRESH_BINARY)
    contours2, hierarchy2 = cv2.findContours(threshold, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    height,width = img1.shape[:2]
    blank1 = np.zeros(shape = [height,width], dtype=np.uint8)
    height, width = img2.shape[:2]
    blank2 = np.zeros(shape=[height, width], dtype=np.uint8)

    for cnt in contours1:
        cnt = cv2.convexHull(cnt)
        area = cv2.contourArea(cnt)

        (x, y, w, h) = cv2.boundingRect(cnt)

        if area >= SHAPE_MIN_AREA:
            cv2.rectangle(img=blank1,
                      pt1=(x, y),
                      pt2=(x + w, y + h),
                      color=(255, 255, 255),
                      thickness=2)
        # cnt = cv2.convexHull(cnt)
        # area = cv2.contourArea(cnt)
        #
        # if area >= SHAPE_MIN_AREA :
        #     approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        #     cv2.drawContours(blank1, [approx], 0, (255), 2)


    for cnt in contours2:
        cnt = cv2.convexHull(cnt)
        area = cv2.contourArea(cnt)

        (x, y, w, h) = cv2.boundingRect(cnt)

        if area >= SHAPE_MIN_AREA:
            cv2.rectangle(img=blank2,
                          pt1=(x, y),
                          pt2=(x + w, y + h),
                          color=(255, 255, 255),
                          thickness=2)
        # cnt = cv2.convexHull(cnt)
        # area = cv2.contourArea(cnt)
        # if area >= SHAPE_MIN_AREA:
        #     approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        #     cv2.drawContours(blank2, [approx], 0, (255), 2)

    cv2.imshow("shapes 1", img1)
    cv2.imshow("shapes 2", img2)
    cv2.imshow("BLANK1", blank1)
    cv2.imshow("BLANK2", blank2)
    difference = cv2.subtract(blank1, blank2)
    # difference = cv2.resize(difference, None, fx=.5, fy=.5)
    cv2.imshow("difference", difference)
    cv2.waitKey(0)
    cv2.destroyAllWindows()