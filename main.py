import logging
import optparse
import os
import shutil

from source.imagediff import ImageDiff, PixelDiff


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
    #pixelbypixelComparison("Image/SC21.png","Image/SC22.png")
    baseline_path, comparison_path, output_path, logs_path, verbose, quiet = _parse_args()
    # image_diff = ImageDiff(baseline_path, comparison_path)
    PixelDiff(baseline_path, comparison_path)
    # image_diff.showDifference()
    # image_diff.showImage()
    # image_diff.showImageGray()
    # image_diff.showImageThresh()
    # image_diff.showImageContours()

if __name__ == "__main__":
    main()