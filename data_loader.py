from csv import DictReader
from glob import glob
import os

class DataLoader:

    def __init__(self, data_path):
        self.data_path = data_path
        self.load_link()

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


    def get_patient_data(self, patient_id):
        """ Load the data (images + labels) of a given patient
        :param patient_id: string, the id of the patient
    
        :raises:
        """            
        dicom_fnames = self.get_patient_dicom_fnames(patient_id)
        label_fnames = self.get_patient_label_fnames(patient_id)
        return self.filter_out_patient_missing_values(patient_id, dicom_fnames, label_fnames)


    def filter_out_patient_missing_values(self, patient_id, dicom_fnames, label_fnames):
        """ Remove the missing values for given a patient
        :type self:
        :param self:
    
        :type dicom_fnames:
        :param dicom_fnames:
    
        :type label_fnames:
        :param label_fnames:
    
        :raises:
    
        :rtype:
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

    def load_dataset(self):
        pass


if __name__ == '__main__':
    loader = DataLoader('final_data')
    

    