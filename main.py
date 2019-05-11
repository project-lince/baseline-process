from source.image_diff import showDifference
from source.pixelbypixel_diff import pixelbypixelComparison


def main():
    pixelbypixelComparison("a","b")
    showDifference()
    #image_diff.showImage()
    #image_diff.showImageGray()
    #image_diff.showImageThresh()
    #image_diff.showImageContours()

if __name__ == "__main__":
    main()