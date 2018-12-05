import os
from csv import DictReader
from glob import glob
import parsing

class DataLoader:
    """ Load the dataset from the raw files
    """

    def __init__(self, data_path):
        """ Load the dataset

        :param data_path: The root path of the dataset
        """
        self.data_path = data_path
        self.load_link()
        self.load_dataset()

    def load_link(self):
        """ Load the link file and parse it
        :param fname: The filename of the link file

        :raises: csv.Error if any error in encoutered by the csv package
        :raises: FileNotFoundError if the file is missing

        :return: A dictonary whose keys are the dicoms and values contourfiles for each patient
        """
        link_fname = os.path.join(self.data_path, 'link.csv')
        self.link_dict = {}
        with open(link_fname, mode='r') as infile:
            reader = DictReader(infile, delimiter=',')
            for row in reader:
                self.link_dict[row['patient_id']] = row['original_id']


    def get_patient_fnames(self, patient_id):
        """ Load the data filenames (images + labels) of a given patient
        :param patient_id: string, the id of the patient
    
        :return: [[image fname1, label f_name1], ...]
        """            
        dicom_fnames = self.get_patient_dicom_fnames(patient_id)
        label_fnames = self.get_patient_label_fnames(patient_id)
        return self.filter_out_patient_missing_values(patient_id, dicom_fnames, label_fnames)


    def filter_out_patient_missing_values(self, patient_id, dicom_fnames, label_fnames):
        """ Remove the missing values for given a patient. Return a unified list if [image fname, label f_name]
        :param patient_id: string, the id of the patient

        :param dicom_fnames: [fname1, fname2, ...] a list of the dicom filenames
    
        :param label_fnames: [fname1, fname2, ...] a list of the i-contour filenames
    
        :return: [[image fname1, label f_name1], ...]
        """    
        filtered_fnames = []
        label_id = self.link_dict[patient_id]
        for dicom_fname in dicom_fnames:
            # extract number from the filenames
            number = os.path.basename(dicom_fname) # remove path
            number, _ = os.path.splitext(number) # remove extension 
            label_fname = "IM-0001-%04d-icontour-manual.txt" % (int(number))
            label_fname =  os.path.join(self.data_path, 'contourfiles', label_id, 'i-contours', label_fname)
            if label_fname in label_fnames:
                filtered_fnames.append([dicom_fname,label_fname])
        return filtered_fnames
            

    def get_patient_dicom_fnames(self, patient_id):    
        """ Get the filenames of the DICOM files for a given patient

        :param patient_id: string, the id of the patient
    
        :return: The DICOM filenames as a list
        """    
        patient_dicom_pattern = os.path.join(self.data_path, 'dicoms', patient_id, '*.dcm')
        fnames = glob(patient_dicom_pattern)
        fnames = [fname for fname in fnames if not os.path.basename(fname).startswith('.')]
        return fnames
    
    def get_patient_label_fnames(self, patient_id):
        """ Get the filenames of the label (i-contour) files for a given patient

        :param patient_id: string, the id of the patient
    
        :return: The label filenames as a list
        """    
        label_id = self.link_dict[patient_id]
        patient_label_pattern = os.path.join(self.data_path, 'contourfiles', label_id, 'i-contours', '*.txt')
        fnames = glob(patient_label_pattern)
        fnames = [fname for fname in fnames if not os.path.basename(fname).startswith('.')]
        return fnames

    def get_patient_data(self, patient_id): 
        """ Get the image and masks for a given patient

        :param patient_id: string, the id of the patient  
    
        :return: [[image1, mask1], [image2, mask2], ...]
        """    
        patient_data = []
        fnames = self.get_patient_fnames(patient_id)
        for dicom_fname, label_fname in fnames:
            image = parsing.parse_dicom_file(dicom_fname)
            if not image == None:
                image = image['pixel_data']
                w, h = image.shape
                mask = parsing.parse_contour_file(label_fname)
                if not mask == None:
                    mask = parsing.poly_to_mask(mask, w, h)
                    patient_data.append([image, mask])
        return patient_data

    def load_dataset(self):
        """ Load the entire dataset

        """    
        self.dataset = []
        for patient_id in self.link_dict.keys():
            self.dataset += self.get_patient_data(patient_id)


if __name__ == '__main__':
    loader = DataLoader('final_data')

    # display test
    import matplotlib.pyplot as plt
    fig = plt.figure()
    # size of the grid to plot
    w = 10
    h = 10
    for i in range(w*h):
        if i<len(loader.dataset):
            ax = fig.add_subplot(w,h,i+1)
            ax.imshow(loader.dataset[i][0], cmap='gray', interpolation=None)
            ax.imshow(loader.dataset[i][1], cmap='gray', interpolation=None, alpha = 0.3)      
            ax.set_axis_off()
    plt.show()
    

    