# import the necessary packages
import logging

from skimage.measure import compare_ssim
import imutils
import cv2


class ImageDiff:
    def __init__(self, baseline, comparison):
        self.baseline = cv2.imread(baseline)
        self.comparison = cv2.imread(comparison)
        self.difference = None


class PixelDiff(ImageDiff):
    def __init__(self, baseline, comparison):
        super(PixelDiff, self).__init__(baseline, comparison)

        # compute the structural similarity index SSIM between the images,
        # ensuring that the difference is retured
        (score, diff) = compare_ssim(self.baseline, self.comparison, full=True, multichannel=True)
        diff = (diff * 255).astype('uint8')
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # threshold the difference image, followed by finding contours
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # shows the images
        cv2.imshow("Image A", self.baseline)
        cv2.imshow("Image B", self.comparison)

        # cnts is an arary of (x,y) coordenates that descrives the shape that holds all
        # the differences
        logging.debug(cnts)
        cv2.drawContours(self.baseline, cnts, -1, (225, 255, 120), -1)
        cv2.imshow("Image A", self.baseline)

        cv2.waitKey(0)


class VisualDiff(ImageDiff):
    def __init__(self, baseline, comparison):
        super(VisualDiff, self).__init__(baseline, comparison)
        # conver the images to grayscale
        _gray_baseline = cv2.cvtColor(self.baseline, cv2.COLOR_BGR2GRAY)
        _gray_comparison = cv2.cvtColor(self.comparison, cv2.COLOR_BGR2GRAY)

        self.baseline_threshold = cv2.threshold(_gray_baseline, 0, 255, cv2.THRESH_BINARY)[1]
        self.comparison_threshold = cv2.threshold(_gray_comparison, 0, 255, cv2.THRESH_BINARY)[1]

        self.baseline_laplacian = cv2.Laplacian(self.baseline, cv2.CV_64F)
        self.comparison_laplacian = cv2.Laplacian(self.comparison, cv2.CV_64F)

        # compute the structural similarity index SSIM between the images,
        # ensuring that the difference is retured
        self.laplacian_ssim_score, self.laplacian_ssim_diff = compare_ssim(self.baseline_laplacian,
                                                                           self.comparison_laplacian, full=True,
                                                                           multichannel=True)
        diff = (self.laplacian_ssim_diff * 255).astype('uint8')
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # threshold the difference image, followed by finding contours
        # obtain the regions of the two input images that differ
        self.diff_thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        _cnts = cv2.findContours(self.diff_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.diff_thresh_contours = imutils.grab_contours(_cnts)

    def show_image_thresh(self):
        # displays the image thresh

        cv2.imshow("Image Thresh", self.diff_thresh)
        cv2.waitKey(0)

        # Draws the image contours on the first image

    def show_image_contours(self):
        # cnts is an arary of (x,y) coordenates that descrives the shape that holds all
        # the differences
        logging.debug(self.diff_thresh_contours)
        cv2.drawContours(self.baseline, self.diff_thresh_contours, -1, (225, 255, 120), -1)
        cv2.imshow("Baseline differences", self.baseline)
        cv2.waitKey(0)

        # Display a black and white image of the difference found in the two images

    def show_difference(self):
        logging.info("SSIM: {}".format(self.laplacian_ssim_score))
        if (self.laplacian_ssim_score == 1):
            logging.info("No Diference")
        cv2.imshow("image difference", self.laplacian_ssim_diff)
        cv2.waitKey(0)

        # Displays the loaded images

    def show_image(self):
        cv2.imshow("Image A", self.baseline)
        cv2.imshow("Image B", self.comparison)
        cv2.waitKey(0)

        # Displays the loaded images in black and white

    def show_image_gray(self):
        cv2.imshow("laplacian A", self.baseline_laplacian)
        cv2.imshow("laplacian B", self.comparison_laplacian)
        cv2.imshow("thresh A", self.baseline_threshold)
        cv2.imshow("thresh B", self.comparison_threshold)
        cv2.waitKey(0)
