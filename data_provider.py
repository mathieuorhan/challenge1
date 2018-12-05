import numpy as np
from data_loader import DataLoader

class DataProvider:
    """ Provider of data batches
    """

    def __init__(self, data_path, batch_size):
        """
        :param data_path: The root path of the dataset

        :param batch_size: The batch size
        """    
        self.batch_size = batch_size
        dataset = DataLoader(data_path).dataset
        self.dataset_size = len(dataset)

        # separate images and labels
        self.images = np.array([pair[0] for pair in dataset])
        self.labels = np.array([pair[1] for pair in dataset])
        
        self.seen = np.zeros(self.dataset_size)

    def next_batch_available(self):
        """ Tell if there are still batches missing to complete the current epoch.
        Reinitilize the epoch if there are no more batch.

        :return: True if there are still unseen images in the epoch,
        False when the epoch is complete
        """
        if sum(self.seen)<self.dataset_size:
            return True
        else:
            self.seen = np.zeros(self.dataset_size)
            return False

    def get_batch(self):
        """ Return a random batch from the dataset

        :return: a tuple of two numpy array, the first one contains the images and the second one the masks
        """
        indexes = self.get_batch_indexes()
        self.seen[indexes] = 1 # mark indexes as "seen"
        return self.images[indexes], self.labels[indexes]
        

    def get_batch_indexes(self):
        """ Return indexes to prepare a batch
        """
        # get the list of non-seen elements
        available_indexes = np.array([i for i in range(self.dataset_size) if not self.seen[i]])
 
        if len(available_indexes)>self.batch_size:
            choice = np.random.choice(len(available_indexes), self.batch_size)
            return available_indexes[choice]
        else:
            # we have to take seen elements if batch_size is not a divider from the dataset length
            remaining_indexes_number = self.batch_size-len(available_indexes) 
            choice = np.random.choice(self.dataset_size, remaining_indexes_number)
            indexes_all = np.arange(self.dataset_size)[choice]
            return np.concatenate([indexes_all, available_indexes], axis=0)


if __name__ == '__main__':
    #provider = DataProvider('final_data', 100)
    provider = DataProvider('final_data', 8)
    
    import matplotlib.pyplot as plt
    fig = plt.figure()
    # size of the grid to plot
    w = 8
    h = 3
    for i in range(w*h):
        if i%provider.batch_size==0:
            images, labels = provider.get_batch()
        ax = fig.add_subplot(h,w,i+1)
        ax.imshow(images[i%provider.batch_size], cmap='gray', interpolation=None)
        ax.imshow(labels[i%provider.batch_size], cmap='gray', interpolation=None, alpha = 0.3)      
        ax.set_axis_off()
    plt.show()

