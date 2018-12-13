# Phase two of the coding challenge

## Parsing the outer contours

Adding the parsing of the outer contours is easy as its format is similar inner contour. I checked that quickly, replacing i-contour by o-contour in my existing code. I added the contour type as a parameter to all the relevant methods.
Some algorithms will make use of the outer contours and some will not. To cover all cases and factorize the code I leverage the object-oriented structure and inheritance in the `DataLoaderWithOuterContours` class. I also added a check in the DataLoader class to make sure that users do not supply a wrong value (e.g., 'inner' instead of 'i'). 
I ran the tests I made after my changes, and adapted my visual test to visualize both contours. Everything looks fine !

## Heuristic LV Segmentation approaches

### Thresholding

It is the simplest segmentation method. Let's observe the distributions of the pixels intensities for the blood pool and the heart muscle using `segmentation_threshold.py`. 

![Distribution of the pixels intensities](/figures/pixels_distributions.png)

This plot is instructive. The red distribution (LV heart muscle) is almost unimodal wih a main mode around 50 but is skewed-right. The blue (blood pool) is also almost unimodal with a main mode around 180, but its support is included in the red distribution support. That means a lot of pixels will be misclassified for any threshold. This approach can however separe the two main modes.

### A more advanced non-ML approach

![Plot of the LV Heart muscle](/figures/lv_heart_muscle.png)

The precedent approach does not use any smoothness prior. From observation, I suggest to include two new priors:
- The inner contour is not on the border of the outer contour
- The inner contour and the outer contour are connected space

To include these priors, I propose a discrete Markov Random Field (MRF) approach. We define the unary and pairwise potentials and optimize the energy via graph-cut. One of the advantage of using a graph is that we can ignore all the unrelevant surrounding pixels of the outer contour.
The two labels correspond to heart muscle and blood pool.

The unary potential models the intensity and the inclusion prior. For the intensity potential, we can use the l2 distance to the main mode of the assigned distribution, normalized by, say, the standard deviation of this distribution. The inclusion potential is 1 if a pixel on the border is assigned to the blood pool, and 0 otherwise.

The pairwise pontial is 1 if the labels are differents and 0 otherwise.

A linear combination of these potentials is used as an energy. The results should be good after some tweaking of the relative importance of each potential.

If necessary, more priors could be included to further improve the performance. Some ideas:
- gradient norm is likely to be higher on the inner contour
- gradient direction is likely to be distributed from the center to the borders on the inner contour

### A deep learning approach

The first thing that comes in mind is to use a U-net to predict the inner contour. Many models are available, e.g. one the best is DeepLabv3+. However I would start with my own model that I shall describe now.

The input is the image, and the output the mask. I propose to use a (deep) convolutionnal neural network with a U-net structure, regularized with batch normalisation, with the cross-entropy loss function, and a good optimizer such as rsmprop to perform gradient descent.
Adding a spatial attention mecanism should be a very good idea to explore given the aera of interest is always small and located.
Some priors could be included in the model's loss to encourage uniqueness and connexity, in the spirit of the previous section. 
Post-processing could be used to smooth the output : fill the holes, remove noise, etc. 

The main issue of the using deep learning is that the provided data is not sufficient for the training. The network could be pretrained on similar medical images, and we can augment the data with care (slight rotations, centered cropping, elastic deformations...). On a large enough dataset I have little doubt that a deep learning based approach could outperform the method of the previous section, and it does not require the outer contour. 






