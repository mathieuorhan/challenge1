# Phase one of the coding challenge

## Parse the DICOM images and Contour Files

All the code of this part is in the `data_loader.py` file.

The `parsing.py` file is mostly not modified. I simply added a loading and displaying test in the `__main__`.
The functions were tested individually, and then together to display several images with overlaying masks.

An object-oriented approach was chosen for the sake of clarity. It helps to break the loading component into small and simple methods. 
These methods are documented according to the convention used in the provided `parsing.py` file.
The function are tested individually, and then a display test is done (see the figure below).

![Display of the iamges and masks](/figures/dataset_visu.png)
*All the dataset is displayed on this image. We can visually inspect it.*

Improvements :
If the dataset was massive and couldn't fit in the memory, I would store only the filenames and then put actual files in a queue with a fixed maximum capacity.

Tests :
The part is rather clear, I think visualisation and indivual inspection of methods outputs are enough.


## Model training pipeline

All the code of this part is in the `data_provider.py` and `tests.py` files.

We use an object oriented approach, again for the sake of clarity. Except the mentionned improvement, I don't think modifications are necessary on the first part, performance should be good if the dataset fits the memory. I didn't modified the first part. I don't see any major deficiency in my code.

Tests :
I added some unit tests for this part, to make sure in particular that epoches were properly completed. I also visually inspected the batches (see figure below).

Improvements :
One could (easily) make a generator (for e.g. Keras), but this was not asked. 

![Display of the iamges and masks](/figures/three_batches.png)

*We generate three different batches of the right size*


