# import the necessary packages
from skimage.measure import compare_ssim
import imutils
import cv2


def pixelbypixelComparison(imageA_path, imageB_path):
    # load the two input images
    imageA_path = imageA_path
    imageB_path = imageB_path

    imageA = cv2.imread(imageA_path)
    imageB = cv2.imread(imageB_path)

    # compute the structural similarity index SSIM between the images,
    # ensuring that the difference is retured
    (score, diff) = compare_ssim(imageA, imageB, full=True, multichannel=True)
    diff = (diff * 255).astype('uint8')
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # threshold the difference image, followed by finding contours
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #shows the images
    cv2.imshow("Image A",imageA)
    cv2.imshow("Image B", imageB)

    # cnts is an arary of (x,y) coordenates that descrives the shape that holds all
    # the differences
    print(cnts)
    cv2.drawContours(imageA, cnts, -1, (225, 255, 120), 1)
    cv2.imshow("Image A", imageA)

    cv2.waitKey(0)