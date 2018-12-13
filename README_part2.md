# Phase two of the coding challenge

## Parsing the outer contours

Adding the parsing of the outer contours is easy as the structure is the same as the inner contour. I checked that quickly, replacing i-contour by o-contour in my existing code. I start by adding this as a parameter to all the relevant methods.
Some algorithms will make use of the outer contours and some will not. To cover all cases and factorize the code I leverage the object-oriented structure and inheritance in the `DataLoaderWithOuterContours` class. I also added a check in the DataLoader class to make sure that the user does not supply a wrong value (e.g., 'inner' instead of 'i'). 
I ran the tests I made after my changes, and adapted my visual test to visualize both contours. Everything looks fine !

## Heuristic LV Segmentation approaches



