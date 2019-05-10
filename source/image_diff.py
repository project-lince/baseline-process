# import the necessary packages
from skimage.measure import compare_ssim
import imutils
import cv2


#load the two input images
imageA_path = "../Image/original.png"
imageB_path = "../Image/manipulated.png"

imageA = cv2.imread(imageA_path)
imageB = cv2.imread(imageB_path)

#conver the images to grayscale
grayA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
grayB= cv2.cvtColor(imageB,cv2.COLOR_BGR2GRAY)

#compute the structural similarity index SSIM between the images,
#ensuring that the difference is retured
(score, diff) = compare_ssim(imageA, imageB, full=True, multichannel=True)
diff = (diff * 255).astype('uint8')
diff = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
#threshold the difference image, followed by finding contours
#obtain the regions of the two input images that differ
thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)





def printImageThresh():
    cv2.imshow("Image Thresh", thresh)
    cv2.waitKey(0)


def printImageContours():
    #cnts is an arary of (x,y) coordenates that descrives the shape that holds all
    #the differences
    print(cnts)
    cv2.drawContours(imageA, cnts, -1, (0, 255, 0), 3)
    cv2.imshow("Image A", imageA)
    cv2.waitKey(0)


def printDifference():
    print("SSIM: {}".format(score))
    cv2.imshow("image difference", diff)
    cv2.waitKey(0)
def showImage():
    cv2.imshow("Image A",imageA)
    cv2.imshow("Image B", imageB)
    cv2.waitKey(0)
def showImageGray():
    cv2.imshow("ImageGray A", grayA)
    cv2.imshow("ImageGray B", grayB)
    cv2.waitKey(0)
