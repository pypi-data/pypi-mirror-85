import math
from pathlib import Path
import numpy as np
from PIL import Image, ImageStat
import cv2
from math import sqrt
import scipy
from scipy.stats import kurtosis, skew
from matplotlib import pyplot as plt
import ast


class LightFeaturesDetector(object):
    """
    Input: Input RGB image file path
    Output: Image light, colorfulness and laplacian, histogram value of input image along with various values of
    brightness distribution
    """

    def __init__(self, image_path, width=800, height=600):
        """
        LightFeaturesDetector constructor, default resize is to 600*450
        """
        self.__image_path = image_path
        self.image = Image.open(self.__image_path).resize((width, height), Image.ANTIALIAS)
        self.cv_image = np.array(self.image)

    def compute_metrics(self):
        """
        Input: None
        Output : Dictionary with the 8 light scores of interest (on the image) such as brightness, colorfulness,
        laplacian, histogram, brightness mean from image stat, brightness_std, brightness skewness and brightness
        kurtosis. The last 4 metrics are computed on each channel separately whereas the first (brightness and
        colorfulness) are gathered on the three channels in R,G,B order.
        """
        image = self.cv_image
        dico = {"brightness": self.brightness(self.image), "colorfulness":  self.image_colorfulness(image),
                "laplacian": self.laplacian_variance(image), "histogram": self.histogram(image),
                "brightness_mean": self.brightness_mean(self.image), "brightness_std": self.brightness_std(self.image),
                "brightness_skew": self.brightness_skew(image), "brightness_kurt": self.brightness_kurt(image)}
        return dico

    def compute_brightness(self):
        """
        Input: None
        Output : Dictionary with the 8 light scores of interest (on the image) such as brightness, colorfulness,
        laplacian, histogram, brightness mean from image stat, brightness_std, brightness skewness and brightness
        kurtosis. The last 4 metrics are computed on each channel separately whereas the first (brightness and
        colorfulness) are gathered on the three channels in R,G,B order.
        """
        image = self.cv_image
        dico = {"brightness": self.brightness(self.image)}
        return dico

    @staticmethod
    def brightness(image):
        '''
        Input : Image
        Output : brightness score
        '''
        levels = np.linspace(0, 255, num=10)
        #image = Image.fromarray(image)
        image_stats = ImageStat.Stat(image)
        red_channel_mean, green_channel_mean, blue_channel_mean = image_stats.mean
        image_bright_value = math.sqrt(0.299 * (red_channel_mean ** 2)
                                       + 0.587 * (green_channel_mean ** 2)
                                       + 0.114 * (blue_channel_mean ** 2))
        #image_bright_level = np.digitize(image_bright_value, levels, right=True)
        return round(image_bright_value, 1)

    @staticmethod
    def image_colorfulness(image):
        '''
        input : Array of PIL format image
        Output : Colorfulness score as defined by Hasler and Süsstrunk, Measuring Colorfulness in Natural Images, 2003
        '''
        image = np.array(image)
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]
        # red-green and yellow-blue opponents metrics
        rg = np.absolute(R - G)
        yb = np.absolute(0.5 * (R + G) - B)

        # compute mean and standard deviation 
        (rbMean, rbStd) = (np.mean(rg), np.std(rg))
        (ybMean, ybStd) = (np.mean(yb), np.std(yb))

        # combine mean and standard deviations to return colorfulness metric
        stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
        meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))

        return stdRoot + (0.3 * meanRoot)

    @staticmethod
    def generate_subsection(image):
        """

        :param image: cv2 image
        :return: array of size 9 with each subsections mean brightness over the image
        """
        height = image.shape[0]
        width = image.shape[1]
        x = [0, int(width / 3), int(2 * width / 3), width]
        y = [0, int(height / 3), int(2 * height / 3), height]
        subsection_brightness = []

        for i in range(3):
            for j in range(3):
                subsection = image[y[i]:y[i + 1], x[j]:x[j + 1]]
                avg_brightness = np.mean(subsection)
                subsection_brightness.append(avg_brightness)
        return subsection_brightness

    @staticmethod
    def generate_peak_grayscale(image):
        """

        :param image: cv2 image
        :return: max indice of histogram peak
        """
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        histr = cv2.calcHist([image_grayscale], [0], None, [256], [0, 256])
        max_indices = np.argmax(histr, axis=0)
        return max_indices

    @staticmethod
    def laplacian_variance(image):
        '''
        Input : Array of PIL image
        Output: Laplacian score
        '''
        return cv2.Laplacian(image, cv2.CV_64F).var()

    @staticmethod
    def old_histogram(image):
        '''
        Input : Array of PIL image
        Output : array histogram of the image
        '''
        color = ('r', 'g', 'b')
        hist = []
        for i, col in enumerate(color):
            hist.append(cv2.calcHist([image], [i], None, [256], [0, 256]))
        return hist

    @staticmethod
    def histogram(image):
        '''
        Input : Array of PIL image
        Output : array histogram of the image in a list format
        '''
        color = ('r', 'g', 'b')
        hist = []
        for i, col in enumerate(color):
            hist.append(cv2.calcHist([image], [i], None, [256], [0, 256]))
        histogram = hist #[1:-1]
        for i in range(len(histogram)):
            histogram[i] = histogram[i].tolist()
            histogram[i] = [x[0] for x in histogram[i]]
        return histogram


    @staticmethod
    def brightness_mean(image):
        '''
        Input : PIL Image
        Output : Array of brightness mean score on each channel (R,G,B)
        '''
        image_stats = ImageStat.Stat(image)
        mean = image_stats.mean
        mean = [np.round(x, 3) for x in mean]
        return mean

    @staticmethod
    def brightness_std(image):
        '''
        Input : PIL image
        Output : Array of brightness std score on each channel (R,G,B)
        '''
        image_stats = ImageStat.Stat(image)
        stddev = image_stats.stddev
        stddev = [np.round(x, 3) for x in stddev]
        return stddev

    @staticmethod
    def brightness_skew(image):
        '''
        Input : PIL Image in array format
        Output : Array of brightness skewness score on each channel (R,G,B)
        '''
        image = image / 255.0
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]
        skewness_r = scipy.stats.skew(R, axis=None)
        skewness_g = scipy.stats.skew(G, axis=None)
        skewness_b = scipy.stats.skew(B, axis=None)
        skewness = [round(skewness_r, 5), round(skewness_g, 5), round(skewness_b, 5)]
        return skewness

    @staticmethod
    def brightness_kurt(image):
        '''
        Input : PIL image in array format
        Output : Array of brightness kurtosis score on each channel (R,G,B)
        '''
        image = image / 255.0
        R = image[:, :, 0]
        G = image[:, :, 1]
        B = image[:, :, 2]
        kurtosis_r = scipy.stats.kurtosis(R, axis=None)
        kurtosis_g = scipy.stats.kurtosis(G, axis=None)
        kurtosis_b = scipy.stats.kurtosis(B, axis=None)
        kurt = [round(kurtosis_r, 5), round(kurtosis_g, 5), round(kurtosis_b, 5)]
        return kurt

    def metrics(self):
        '''
        Old method for metrics calculations - to be removed
        Input : None
        Output : 4 of the 8 metrics of interest
        '''
        my_file = Path(self.__image_path)
        assert my_file.is_file()
        image = Image.open(self.__image_path)
        image.resize((800, 600), Image.ANTIALIAS)
        mean, std, skew, kurt = self.__light_metrics(image)
        return mean, std, skew, kurt

    def brightness2(self):
        '''
        Another method for brightness calculation - more time consuming - TBR if needed
        Input : None
        Output : brightness mean score calculated on each pixel
        '''
        # check bgr or rgb order
        cv_image = self.cv_image[:, :, ::-1].copy()
        height, width, _ = cv_image.shape
        pixel_lum = 0
        for i in range(height):
            for j in range(width):
                red = cv_image[i, j, 2]
                green = cv_image[i, j, 1]
                blue = cv_image[i, j, 0]
                pixel_lum += sqrt(0.299 * (red ** 2) + 0.587 * (green ** 2) + 0.114 * (blue ** 2))
        img_lum = pixel_lum / (width * height)
        scaled_img_lum = round(img_lum * 10 / 255, 2)

        return scaled_img_lum

    @staticmethod
    def __light_metrics(image):
        '''
        Old method for metrics calculations - to be removed
        '''
        cv_image = np.array(image)
        cv_image = cv_image[:, :, ::-1].copy()
        cv_image = cv_image / 255.0
        image_stats = ImageStat.Stat(image)
        mean = image_stats.mean
        mean = [np.round(x, 3) for x in mean]
        stddev = image_stats.stddev
        stddev = [np.round(x, 3) for x in stddev]
        B = cv_image[:, :, 0]
        G = cv_image[:, :, 1]
        R = cv_image[:, :, 2]
        skewness_b = scipy.stats.skew(B, axis=None)
        skewness_g = scipy.stats.skew(G, axis=None)
        skewness_r = scipy.stats.skew(R, axis=None)
        skewness = [round(skewness_b, 5), round(skewness_g, 5), round(skewness_r, 5)]
        kurtosis_b = scipy.stats.kurtosis(B, axis=None)
        kurtosis_g = scipy.stats.kurtosis(G, axis=None)
        kurtosis_r = scipy.stats.kurtosis(R, axis=None)
        kurt = [round(kurtosis_b, 5), round(kurtosis_g, 5), round(kurtosis_r, 5)]

        return mean, stddev, skewness, kurt