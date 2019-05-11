#from source.image_diff import showDifference
import source.image_diff
from source.pixelbypixel_diff import pixelbypixelComparison


def main():
    #pixelbypixelComparison("Image/SC21.png","Image/SC22.png")

    source.image_diff.showDifference()
    source.image_diff.showImage()
    source.image_diff.showImageGray()
    source.image_diff.showImageThresh()
    source.image_diff.showImageContours()

if __name__ == "__main__":
    main()