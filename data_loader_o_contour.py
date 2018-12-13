from data_loader import DataLoader
import numpy as np

class DataLoaderWithOuterContours(DataLoader):
    """
    Load the dataset from the raw files with both the inner (i) and the outer (o) contours.
    """

    def __init__(self, data_path):
        """ Load the dataset

        :param data_path: The root path of the dataset
        """
        self.data_path = data_path
        self.load_link()
        self.load_dataset()

    def load_dataset(self):
        """ Load the entire dataset. 
        This loads and stores the dataset with the structure :
        [[image1, mask_i_1, mask_o_1], [image2, mask_i_2, mask_o_2], ...] 
        """    
        self.dataset = []
        for patient_id in self.link_dict.keys():
            patient_i_contour = self.get_patient_data(patient_id, 'i')
            patient_o_contour = self.get_patient_data(patient_id, 'o')
            patient_data = self.merge_patient_contours(patient_i_contour, patient_o_contour)
            self.dataset += patient_data

    def merge_patient_contours(self, patient_i_contour, patient_o_contour):
        """
        Merge a patient inner and outer contours and remove incomplete data.

        :param patient_i_contour: [[image1, mask_i_1], [image2, mask_i_2], ...]
        :param patient_o_contour: [[image1, mask_o_1], [image2, mask_o_2], ...]

        :returns: [[image1, mask_i_1, mask_o_1], [image2, mask_i_2, mask_o_2], ...]
        """
        patient_data = []
        for img_i, mask_i in patient_i_contour:
            for img_o, mask_o in patient_o_contour:
                if np.array_equal(img_i, img_o):
                    patient_data.append([img_i, mask_i, mask_o])
        return patient_data

if __name__ == '__main__':
    loader = DataLoaderWithOuterContours('final_data')

    # display test
    import matplotlib.pyplot as plt
    fig = plt.figure()
    # size of the grid to plot
    w = 10
    h = 10
    for i in range(w*h):
        if i<len(loader.dataset):
            ax = fig.add_subplot(h,w,i+1)
            ax.imshow(loader.dataset[i][0], cmap='gray', interpolation=None)
            ax.imshow(loader.dataset[i][1], cmap='gray', interpolation=None, alpha = 0.5)
            ax.imshow(loader.dataset[i][2], cmap='gray', interpolation=None, alpha = 0.3)      
            ax.set_axis_off()
    plt.show()
