import cv2
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