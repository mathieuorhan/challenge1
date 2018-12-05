import unittest
import numpy as np
from data_provider import DataProvider
 
class TestDataProvider(unittest.TestCase):
    """ Unit tests for the DataProvider class 
    """
 
    def test_batchsize(self):
        """ Check if the batch size
        """
        provider = DataProvider('final_data', 8)
        img, _ = provider.get_batch()
        self.assertEqual(len(img), provider.batch_size)

    def test_img_masks_size(self):
        # Check if images and labels have the same size
        provider = DataProvider('final_data', 8)
        img, masks = provider.get_batch()
        self.assertEqual(len(img), len(masks))

    def test_epoch_complete(self):
        # check if every element of the dataset is really seen at the end
        provider = DataProvider('final_data', 8)
        dataset_img = [img.tostring() for img in provider.images]
    
        while provider.next_batch_available():
            batch_img, _ = provider.get_batch()
            for img in batch_img:
                if img.tostring() in dataset_img:
                    dataset_img.remove(img.tostring())
        self.assertEqual(len(dataset_img), 0)

if __name__ == '__main__':
    unittest.main()