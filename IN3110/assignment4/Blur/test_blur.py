from numpy import pad, random
from Blur.blur_1 import pythonblur
from Blur.blur_2 import numpyblur


def test_pythonblur():
    src = random.randint(0, 255, (1000, 1000, 3))
    image = pad(src, 1, mode="edge")[:, :, 1:-1]
    image = image.astype("uint32")
    dst = pythonblur(src, image)
    dst = dst.astype("uint8")
    avg_pixels = (
        image[1, 1, 0]
        + image[0, 1, 0]
        + image[2, 1, 0]
        + image[1, 0, 0]
        + image[1, 2, 0]
        + image[0, 1, 0]
        + image[0, 2, 0]
        + image[2, 0, 0]
        + image[2, 2, 0]
    ) / 9
    msg = "average of first pixel wasent the average of the nine pixels around"
    assert (dst[0, 0, 0] - avg_pixels) <= 1e-1


def test_numpyblur():
    src = random.randint(0, 255, (1000, 1000, 3))
    image = pad(src, 1, mode="edge")[:, :, 1:-1]
    image = image.astype("uint32")
    dst = numpyblur(image)
    dst = dst.astype("uint8")
    avg_pixels = (
        image[1, 1, 0]
        + image[0, 1, 0]
        + image[2, 1, 0]
        + image[1, 0, 0]
        + image[1, 2, 0]
        + image[0, 1, 0]
        + image[0, 2, 0]
        + image[2, 0, 0]
        + image[2, 2, 0]
    ) / 9
    msg = "average of first pixel wasent the average of the nine pixels around"
    assert (dst[0, 0, 0] - avg_pixels) <= 1e-1


if __name__ == "__main__":
    test_pythonblur()
    test_numpyblur()
