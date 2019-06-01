from random import randint
from Pil import Image
from pathlib import Path
import tempfile
import os


def insert_image_to_other(base_image, insert_image, coord=None):
    """
    Used to insert one image on top of other, in order to optimize space usage and reduce amount of images to mantain.
    :param base_image: path to source image which will be sent to the back. \
    Final image will the the suffix on this file.
    :param insert_image: path to image to be added on top of the base image
    :param coord: Tuple with x and y coordinates. If declared, it will force image to be set at given coordinate.
    If no coord are set, a random one will be generated.
    :return: Tuple with path to final image with the modification, and coordiantes of topleft point of insertion.
    """
    _base_image = Image.open(base_image)
    _insert_image = Image.open(insert_image)
    if not coord:
        coord = (
            randint(0, _base_image.size[0] - _insert_image.size[0]),
            randint(0, _base_image.size[1] - _insert_image.size[1])
        )

    _base_image.paste(_insert_image, coord)
    file = tempfile.TemporaryFile().name+Path(base_image).suffix
    _base_image.save(os.path.abspath(file))
    return file, coord


def generate_similar_images(base_image, image_1, image_2):
    """
    Will insert 2 images into a base image at the same location.
    :param base_image: path to image which both imates will be inserted.
    :param image_1: path to first image to be inserted
    :param image_2: path to second image to be inserted
    :return: tuple with path to image_1 and image_2 inserted to baseline.
    """
    file_1, coord = insert_image_to_other(base_image, image_1)
    file_2, _ = insert_image_to_other(base_image, image_2, coord)
    return file_1, file_2
