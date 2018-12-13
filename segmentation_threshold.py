from data_loader_o_contour import DataLoaderWithOuterContours
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

dataset = DataLoaderWithOuterContours('final_data').dataset

pixels_heart_muscle_total = np.array([])
pixels_blood_pool_total = np.array([])

for image, mask_i, mask_o in dataset:
    # compute the array of the heart muscle using a bitwise XOR
    mask_heart_muscle = np.bitwise_xor(mask_o, mask_i)

    # Flatten and append the masked pixels intensities
    pixels_heart_muscle = image[mask_heart_muscle].flatten()
    pixels_blood_pool = image[mask_i].flatten()

    pixels_heart_muscle_total = np.append(pixels_heart_muscle_total, pixels_heart_muscle)
    pixels_blood_pool_total = np.append(pixels_blood_pool_total, pixels_blood_pool)

plt.title("Distribution of the pixel intensities")
sns.distplot(pixels_blood_pool_total, label='Blood pool')
sns.distplot(pixels_heart_muscle_total, label='Heart muscle')
plt.xlabel("Pixel intensity")
plt.ylabel("Occurence")
plt.legend()
plt.show()




