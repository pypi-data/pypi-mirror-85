import time

import numpy as np
import os
import matplotlib.pyplot as plt

from typing import List, Iterable, Tuple
from skimage import io
from concurrent.futures import ProcessPoolExecutor
from numba import jit

import warnings
warnings.filterwarnings("ignore")

@jit(nopython=True)
def stretch_contrast(img: np.ndarray, ignore: float = 0.005) -> np.ndarray:
    """
    Function to stretch the contrast of an image

    :param img: The image
    :param ignore: Percentage of pixels on each edge to ignore
    :return: The image with stretched contrast
    """
    # Calculate contrast stretch ratio for image
    height, width = img.shape
    hist = np.histogram(img, bins=255)
    threshold = ignore * (height * width)
    a_min = round(hist[1][0])
    a_max = round(hist[1][-1])
    t_min = 0
    t_max = 0
    for ind2 in range(len(hist)):
        t_min += hist[0][ind2]
        t_max += hist[0][254 - ind2]
        if t_min < threshold:
            a_min += 1
        if t_max < threshold:
            a_max -= 1
    ratio = 255 / (a_max - a_min)
    return img * ratio


@jit(nopython=True)
def adjust_contrast(img: np.ndarray, alpha: float) -> np.ndarray:
    """
    Function to adjust the contrast of img according to c_adjust

    :param img: The image
    :param alpha: The amount of contrast stretching
    :return: The image with adjusted contrast
    """
    return img * alpha


def get_batch(ind: int = 0, batch_size: int = 1, vals: List = Iterable) -> Iterable:
    """
    Function to get a batch from a given iterable

    :param ind: The index of the batch
    :param batch_size: The size of an individual batch
    :param vals: The values to get the batch from
    :return: The batch
    """
    return vals[ind:ind + batch_size if ind + batch_size < len(vals) else len(vals)]


def modify_image(img: str, c_adjust: Tuple[float] = (1.25, 1.5, 2, 2.5, 3),
                 target_folder: str = "") -> bool:
    """
    Method to create the training images from the given source image

    :param img: The path leading to the image
    :param c_adjust: The contrast values to adjust the image to
    :param target_folder: The folder to save the created images to
    :return: Bool to indicate that the modification was successful
    """
    # Load image and stretch contrast
    name = os.path.basename(img)
    img = np.clip(stretch_contrast(io.imread(img)), 0, 255).astype("uint8")
    var = np.var(img)
    # Save original image
    io.imsave(os.path.join(target_folder, f"{name}_c_adjust_{var:.4f}_1.0.png"),
              img)
    # Adjust contrast
    for alpha in c_adjust:
        timg = np.clip(adjust_contrast(img.astype("uint16"), alpha), 0, 255).astype("uint8")
        io.imsave(os.path.join(target_folder, f"{name}_c_adjust_{var:.4f}_{alpha:.2f}.png"),
                  timg)
    return True


if __name__ == "__main__":
    # Define paths to needed folders
    target_folder = r"D:\NucDetect\Overexposure Detection\images"
    source_folders = (r"D:\NucDetect\Nucleus Detection Training\images",
                      r"D:\NucDetect\Foci Detection Training\images")

    # Define contrast adjust
    c_adjust = (1.25, 1.5, 2, 2.5, 3)
    ind = 0
    batch_size = 16
    files = []
    # Create argument lists for mapping
    target_paths = [target_folder for _ in range(batch_size)]
    target_adj = [c_adjust for _ in range(batch_size)]
    # Iterate over source folders
    for folder in source_folders:
        files.extend([os.path.join(folder, x) for x in os.listdir(folder)])
    files = tuple(files)
    start = time.time()
    # Create ProcessPool
    with ProcessPoolExecutor(max_workers=None) as e:
        for batch in range(round(len(files) / batch_size)):
            # Get batches
            paths = get_batch(batch, batch_size, files)
            # Map batches
            res = e.map(modify_image, paths, target_adj, target_paths)
            for r in res:
                pass
            print(f"Completed batch {batch}, time:{time.time() - start} ")