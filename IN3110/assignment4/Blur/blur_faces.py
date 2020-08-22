import cv2
import time
from numpy import array, pad, size, shape
from Blur.blur_2 import numpyblur


# This is not used to blur faces but could be used to blur a specific region in an image
def numpyblur2(
    src, x, y, dx, dy
):  # numpy implementation takes face location as
    """A blur function to blur a specifically one part of an image

    Args:
        x (int): starting x coordinate
        y (int): starting y coordinate
        dx (int): width of the image
        dy (int): height of the image

    Returns:
        The input image with the specified area blurred
    """
    image = array(src)  # duplicates the incoming image into an array
    r = image
    r[y : y + dy, x : x + dx, :] = (
        image[y : y + dy, x : x + dx, :]
        + image[y - 1 : y + dy - 1, x : x + dx, :]
        + image[y + 1 : y + dy + 1, x : x + dx, :]
        + image[y : y + dy, x - 1 : x + dx - 1, :]
        + image[y : y + dy, x + 1 : x + dx + 1, :]
        + image[y - 1 : y + dy - 1, x - 1 : x + dx - 1, :]
        + image[y - 1 : y + dy - 1, x + 1 : x + dx + 1, :]
        + image[y + 1 : y + dy + 1, x - 1 : x + dy - 1, :]
        + image[y + 1 : y + dy + 1, x + 1 : x + dx + 1, :]
    ) / 9  # Blurs r by applying
    # formula to height and width axis
    return r  # returns blur with average of  the 9 pixels in a 3x3


def blur_faces(image):
    """
    A blurs faces in an image

    Args:
       image (uint8): source image read using openCV

    Returns:
        The input image with the faces blurred
    """
    dst = image
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        image, scaleFactor=1.025, minNeighbors=5, minSize=(30, 30)
    )  # finds faces and stores them in an array
    for x, y, w, h in faces:
        face = dst[y - 1 : y + h + 1, x - 1 : x + w + 1, :].astype("uint32")
        blur = numpyblur(
            face
        )  # Sends an image the size of a face into numpyblur
        dst[
            y : y + h, x : x + w, :
        ] = blur  # overwrite the existing face of the source image with the blurred face
    return dst.astype("uint8")


if __name__ == "__main__":
    start = time.perf_counter()
    src = cv2.imread("beatles.jpg")
    dst = blur_faces(src)
    cv2.imwrite("testfaceblur2.jpg", dst)
    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} second(s)")
