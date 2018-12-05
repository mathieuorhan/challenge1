# Phase one of the coding challenge

## Parse the DICOM images and Contour Files

The `parsing.py` file is mostly not modified. I simply added a loading and displaying test in the `__main__`. I also documented the :raise: parameters.
The functions were tested individually, and then together to display several images with overlaying masks.

An object-oriented approach was chosen for the sake of clarity. It help to break the loading into small and simple methods. 
These methods are documented according to the convention used in the provided `parsing.py` file.
The function are tested individually, and then a display test is done (see the figure below).

![Display of the iamges and masks](/figures/dataset_visu.png)
*All the dataset is displayed on this image. We can visually inspect it.*

Improvement :
if the dataset was massive and couldn't fit in the memory, I would get the filenames and then put actual files in a queue with a fixed maximum capacity.

## Model training pipeline


