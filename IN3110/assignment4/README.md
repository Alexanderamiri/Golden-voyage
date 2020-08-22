# **Blur; For blurring images**

## blur_1.py
blur_1 contains the python implementation which is slow and not efficient
### Usage
To run the pythonblur() function inside blur_1.py send the function an image using opencv\
For example:\
```python
import cv2
from Blur.blur_1 import pythonblur
src = cv2.imread("image.py")
dst = pythonblur(src)
cv2.imwrite("output_file.jpg", dst)
```
Trying to send the function image that do not have shape (n,m,o) will give an error 

## blur_2.py
blur_2 contains the numpy implementation which is faster
### Usage
To run numpyblur() function inside blur_2.py send the function an image\
For example:
```python
import cv2
from Blur.blur_2 import numpyblur
src = cv2.imread("image.py")
dst = numpyblur(src)
cv2.imwrite("output_file.jpg", dst)
```
Trying to send the function image that do not have shape (n,m,o) will give an error 

## blur_3.py
blur_3 contains the numba implementation of the algorithm
### Usage
To run numbablur() function inside blur_3.py send the function a source image along side a padded image of the original source\
For example:
```python
import cv2
from Blur.blur_3 import numbablur
from numpy import pad
src = cv2.imread("image.py")
image = pad(src, 1, mode='edge')[:, :, 1:-1]
image = image.astype('uint32')
dst = numbablur(src,image)
cv2.imwrite("output_file.jpg", dst)
```
Trying to send the function image that do not have shape (n,m,o) will give an error 

## blur.py

blur.py contains a run in commandline program and a function to blur image files with numpy blur_image()

### Usage

example run for the commandline program:\
python blur.py numba beatles.jpg blurred_beatles.jpg\
\
Example for blur_image()\
```python
import cv2
from Blur.blur import blur_image
src = cv2.imread('image.jpg')
dst = blur_image(src,"blurred.jpg")
```
Trying to send the function image that do not have shape (n,m,o) will give an error 

----------------------------------------------------------------------------------------

## Building

Please ensure these directories exist by running:

```
mkdir -p modules/blur_faces
mkdir tests
```
