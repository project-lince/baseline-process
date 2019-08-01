# import the necessary packages
import logging
from copy import deepcopy

import numpy as np
from skimage.measure import compare_ssim
import imutils
import cv2
import colorgram
import matplotlib.pyplot as plt


def lower_colors(image, color_amount):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label1, center1 = cv2.kmeans(Z, color_amount, None, criteria, 10, 10, cv2.KMEANS_PP_CENTERS)
    center1 = np.uint8(center1)
    res1 = center1[label1.flatten()]
    return res1.reshape((image.shape))


class ImageDiff:
    def __init__(self, baseline, comparison, aliasing_filter=False, ignore_color=False):
        self.baseline_colors = colorgram.extract(baseline, 6)
        self.comparison_colors = colorgram.extract(comparison, 6)
        self.baseline = cv2.imread(baseline)
        self.comparison = cv2.imread(comparison)
        self.baseline = cv2.cvtColor(self.baseline, cv2.COLOR_BGR2GRAY)
        self.comparison = cv2.cvtColor(self.comparison, cv2.COLOR_BGR2GRAY)
        self.baseline = cv2.resize(self.baseline, None, fx=.5, fy=.5)
        self.comparison = cv2.resize(self.comparison, None, fx=.5, fy=.5)
        self.baseline_size = self.baseline.shape
        self.comparison_size = self.comparison.shape

        self.difference = None

        if aliasing_filter or ignore_color:
            # Kmeans for 1 image
            self.baseline = cv2.GaussianBlur(self.baseline, (9, 3), 0)
            self.comparison = cv2.GaussianBlur(self.comparison, (9, 3), 0)
            if ignore_color:
                self.baseline = cv2.Laplacian(self.baseline, cv2.CV_64F)
                self.comparison = cv2.Laplacian(self.comparison, cv2.CV_64F)

        (score, diff) = compare_ssim(self.baseline, self.comparison, full=True, multichannel=True)
        if aliasing_filter or ignore_color:
            diff[diff < .9] = 0
            diff[diff >= .9] = 1
        logging.info("Difference Score:{}".format(score))
        diff = (diff * 255).astype('uint8')

        # diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) ##TODO GRAY OUT IF ABOVE IS CHANGED
        # threshold the difference image, followed by finding contours
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # shows the images

        # cnts is an arary of (x,y) coordenates that descrives the shape that holds all
        # the differences
        self.difference = deepcopy(self.baseline)

        logging.debug(cnts)
        cv2.drawContours(self.difference, cnts, -1, (120, 120, 120), -1)

        self.baseline = cv2.resize(self.baseline, (self.baseline_size[1], self.baseline_size[0]))
        self.difference = cv2.resize(self.difference, (self.baseline_size[1], self.baseline_size[0]))
        self.comparison = cv2.resize(self.comparison, (self.comparison_size[1], self.comparison_size[0]))

        cv2.imshow("Baseline", self.baseline)
        cv2.imshow("Comparison", self.comparison)
        cv2.imshow("Difference", self.difference)

        # self.small_diff = cv2.resize(self.baseline, None,fx=0.25, fy=0.25)
        cv2.waitKey(0)
