from tests.utils import insert_image_to_other, generate_similar_images


def test_aliasing_ignored():
    image_aliasing, image_no_aliasing = generate_similar_images("./resources/website_capture.png",
                                                                "./resources/aliasing.png",
                                                                "./resources/no_aliasing.png")
    # Fuzz level at 69% shows no diff
    assert difference(image_aliasing,image_no_aliasing) == 0


def test_aliasing_magnified_ignored():
    # Fuzz level at 68% shows no diff
    assert difference("tests/resources/aliasing_mag.png", "tests/resources/no_aliasing_mag.png") == 0


#red1.png and red2.png have a difference of 82% fuzz

def test_aliasing_with_differences():
    assert difference