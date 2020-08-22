import cv2
import time
from numpy import pad


def pythonblur(src):  # regular implementation,

    """A blur function to blur a specifically one part of an image

    Args:
        src (uint8): source image
        image (uint32): source image padded at the edges

    Returns:
        A Blurred image of the source image
    """
    src = pad(src, 1, mode="edge")[:, :, 1:-1]
    image = src.astype("uint32")
    r = src
    for c in range(len(r[0, 0, :])):  # For each color
        for h in range(1, len(r) + 1):  # for each pixel in the height
            for w in range(1, len(r[0]) + 1):  # for each pixel in the width
                r[h - 1, w - 1, c] = (
                    image[h, w, c]
                    + image[h - 1, w, c]
                    + image[h + 1, w, c]
                    + image[h, w - 1, c]
                    + image[h, w + 1, c]
                    + image[h - 1, w - 1, c]
                    + image[h - 1, w + 1, c]
                    + image[h + 1, w - 1, c]
                    + image[h + 1, w + 1, c]
                ) / 9
    return r.astype(
        "uint8"
    )  # returns blur with average of  the 9 pixels in a 3x3


if __name__ == "__main__":
    start = time.perf_counter()
    src = cv2.imread("beatles.jpg")
    dst = pythonblur(src)
    cv2.imwrite("testblur.jpg", dst)
    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} second(s)")
