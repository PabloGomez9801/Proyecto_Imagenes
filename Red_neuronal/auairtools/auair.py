import json
import time
import math
from skimage import io
from os import listdir
from os.path import isfile, join, splitext
import cv2

from auairtools.utils import TimeStamp


class AUAIR(object):

    def __init__(self, annotation_file, data_folder) -> object:
        """Default constracture for AUAIR Dataset objects.
        Must be initiated with the annotation file and the data (image) folder.

        Args:
            annotation_file ([type]): [description]
            data_folder ([type]): [description]
        """
        print('Loading annotations into memory...')
        tic = time.time()
        dataset = json.load(open(annotation_file, 'r'))
        assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))
        print('Done (t={:0.2f}s)'.format(time.time() - tic))
        print('%d annotated frames are found.' % len(dataset['annotations']))

        print('Checking images...')
        self._valid_img_ext = ['.jpg', '.jpeg', '.png']
        onlyimgs = [f for f in listdir(data_folder) if
                    isfile(join(data_folder, f)) and splitext(f)[1] in self._valid_img_ext]
        print('%d image files found.' % len(onlyimgs))

        self.annotations = dataset['annotations']
        self.image_names = onlyimgs
        self.data_folder = data_folder
        self.categories = dataset['categories']
        self.num_samples = len(self.annotations)
        self.sorted_annotations = None
        '''
        print('Sanity check...')
        tic = time.time()
        diff = list(set([annot['image_name'] for annot in dataset['annotations']]) - set(onlyimgs))
        if(len(diff)==0):
            print('Done (t={:0.2f}s)'.format(time.time()- tic))
        else:
            raise RuntimeError('Image names in the annotation file and data folder does not match.')
        '''

    def get_data_by_index(self, index, ret_img=True, ret_ann=True):
        """Get image/annotation data according to index in the annotation file. Index range -> [0, num_samples]

        Args:
            index (int): Index of data.
            ret_img (bool, optional): Return image data. Defaults to True.
            ret_ann (bool, optional): Return annotation. Defaults to True.

        Returns:
            np.array, dict: image and annotation
        """
        #if index>=80:
        #    a = index/80
        #    index = index-80*math.floor(a)

        ann = self.annotations[index]
        img = None

        if ret_img:
            img_path = join(self.data_folder, self.annotations[index]['image_name'])
            img = cv2.imread(img_path)

        if ret_img == True and ret_ann == True:
            return img, ann
        elif ret_img == True and ret_ann == False:
            return img
        elif ret_img == False and ret_ann == True:
            return ann
        else:
            raise TypeError("ret_img and ret_ann cannot be both False. At least one of them must be True.")

    def get_data_by_name(self, img_name, ret_img=True, ret_ann=True):
        """Get image/annotation data according to image name.
        
        Args:
            img_name (str): image name
            ret_img (bool, optional): Return image data. Defaults to True.
            ret_ann (bool, optional): Return annotation. Defaults to True.
        
        Returns:
            np.array, dict: image and annotation
        """

        img_names = [f['image_name'] for f in self.annotations]
        index = img_names.index(img_name)

        return self.get_data_by_index(index, ret_img, ret_ann)

    def get_index_by_catId(self, catId):
        """Get index of images/annotations including an object belonging to catId category.
        
        Args:
            catId (int): Id of the category.
        
        Returns:
            List of int: List of image/annotation indices.
        """
        indices = []
        for i in range(len(self.image_names)):
            ann = self.get_data_by_index(i, ret_img=False)
            cat_ids = [c['class'] for c in ann['bbox']]
            if catId in cat_ids:
                indices.append(i)
        return indices

    def get_index_by_alt(self, alt, offset=10000):
        """Get index of images/annotations captured at certain altitude.
        
        Args:
            alt (float): The fligh altitude. In millimeter.
            offset (int, optional): To create a range for target altitude. Defaults to 100.
        
        Returns:
            List of int: List of image/annotation indices.
        """
        indices = []
        for i in range(len(self.image_names)):
            ann = self.get_data_by_index(i, ret_img=False)
            altitude = ann['altitude']
            if altitude - offset < alt and altitude + offset > alt:
                indices.append(i)
        return indices

    def display_image(self, id_or_name):
        """Display image which has given name or id.
        
        Args:
            id_or_name (int or name): Id (index) or name of the image.
        """

        if type(id_or_name) == int:
            img, ann = self.get_data_by_index(id_or_name)
            cv2.imshow("Name: " + ann['image_name'] + ', Altitude: ' + str(ann['altitude']), img)
        else:
            img, ann = self.get_data_by_name(id_or_name)
            cv2.imshow("Name: " + ann['image_name'] + ', Altitude: ' + str(ann['altitude']), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display_bboxes(self, id_or_name):
        """Display image with object bounding boxes which has given name or id.
        
        Args:
            id_or_name (int or name): Id (index) or name of the image.
        """
        if type(id_or_name) == int:
            img, ann = self.get_data_by_index(id_or_name)
        else:
            img, ann = self.get_data_by_name(id_or_name)

        for bbox in ann['bbox']:
            x = bbox['left']
            y = bbox['top']
            w = bbox['width']
            h = bbox['height']
            label = self.categories[bbox['class']]
            cv2.putText(img, label, (x, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), thickness=2,
                        lineType=cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

        cv2.imshow("Name: " + ann['image_name'] + ', Altitude: ' + str(ann['altitude']), img)
        io.imsave("Reconstruccion" + str(id_or_name) + ".png", img)
        cv2.waitKey()
        cv2.destroyAllWindows()
