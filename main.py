import logging

import cv2
import numpy as np
import optparse
import os
import shutil

from source.custom_comparison import layout_diff

from source.imagediff import ImageDiff


def _parse_args():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('-o', '--out', dest="output_path", help="Set output folder path")
    opt_parser.add_option('-l', '--logs', dest="logs_path", help="Set logs folder path")
    opt_parser.add_option('-q', '--quiet', action="store_true", dest="quiet", help="Prints only warning and error logs")
    opt_parser.add_option('-v', '--verbose', action="store_true", dest="verbose", help="Prints debugging logs")
    parsed_options, args = opt_parser.parse_args()
    if len(args) <= 1:
        opt_parser.error('missing baseline and comparison images')
    if parsed_options.verbose and parsed_options.quiet:
        opt_parser.error('options -v and -q are mutually exclusive')
    # Remove argument delimiting quotes included by OptionParser when file name contains spaces
    baseline_path = args[len(args) - 2].strip('"')
    comparison_path = args[len(args) - 1].strip('"')
    output_path = parsed_options.output_path.strip('"')
    logs_path = parsed_options.logs_path.strip('"') if parsed_options.logs_path else None
    return baseline_path, comparison_path, output_path, logs_path, parsed_options.verbose, parsed_options.quiet

def _init_dir(dir_path):
    if not dir_path:
        return
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

def main():

    from source.custom_comparison import pixel_diff

    logging.getLogger().setLevel(logging.INFO)
    #pixelbypixelComparison("Image/SC21.png","Image/SC22.png")
    baseline_path, comparison_path, output_path, logs_path, verbose, quiet = _parse_args()

    # pixel_diff(baseline_path, comparison_path)

##STABLE
    layout_diff()
    # pixel_diff = ImageDiff(baseline_path, comparison_path)
    # visual_diff = ImageDiff(baseline_path, comparison_path, aliasing_filter=True)
    # color_diff = ImageDiff(baseline_path, comparison_path, ignore_color=True)

    #  # Extract 6 colors from an image.

    # # colorgram.extract returns Color objects, which let you access
    #  # RGB, HSL, and what proportion of the image was that color.

    # color_view = np.zeros((350, 350, 3), dtype="uint8")

    # pad = 10
    # for i in range(0,len(pixel_diff.baseline_colors)):
    #     pad = pad*i
    #     color = pixel_diff.baseline_colors[i]
    #     cv2.rectangle(color_view, (pad+34*i, 0), (pad+34+34*i, 34), (color.rgb.b, color.rgb.g, color.rgb.r), -1)
    # cv2.imshow('Color view', color_view)
    cv2.waitKey()

if __name__ == "__main__":
    main()