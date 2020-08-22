from distutils.core import setup

setup(
    name="Blur",
    version="1",
    packages=[".", "modules", "tests", "modules/blur_faces",],
    author="alexaami",
    author_email="alexaami@matnat.uio.bo",
    description="Contain modules for blurring of images",
    requires=["numpy", "cv2", "numba",],
    classifiers=[
        "Programming language : Python 3",
        "Operating system : OS independent",
    ],
    package_data={"": ["*.txt", "*.jpg",]},
)
