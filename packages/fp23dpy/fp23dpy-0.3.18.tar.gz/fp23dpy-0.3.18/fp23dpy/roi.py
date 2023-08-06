"""
Module for manipulating rectangle of interest stuff
"""
import numpy as np

class Roi:
    """
    Class for manipulating rectangle of interest (roi) stuff using cropping of images
    """
    def __init__(self, l=None):
        """
        l is the input of roi information that can either be of length 4 or 6
        if length 4
            l = [min_row, max_row, min_col, max_col]
        if length 6
            add from original image [height, width]
            with this you can also unapply (go from small image to large)
        """
        if not l is None and not len(l) == 6 or len(l) == 4:
            raise AttributeError("Wrong length of list in constructor")
        if len(l) == 6: # indicies can be negative which is fixed here
            l[1] = l[1] if l[1] > 0 else l[-2] + l[1]
            l[3] = l[3] if l[3] > 0 else l[-1] + l[3]
        self.roi = l

    def full(shape):
        """ Roi with same shape as shape """
        h, w = shape
        return Roi([0, h, 0, w, h, w])

    def find_from_mask(mask):
        """
        With a mask where false values are of interest. Find the smallest rectangle than enclose all unmasked values
        """
        [h, w] = mask.shape
        r, c = np.where(~mask)
        edge = 10
        minr = max(0, np.min(r) - edge)
        minc = max(0, np.min(c) - edge)
        maxr = min(mask.shape[0], np.max(r) + edge)
        maxc = min(mask.shape[1], np.max(c) + edge)
        return Roi([minr, maxr, minc, maxc, h, w])

    def mask_from_roi(self):
        """
        With the roi return a mask where false values are inside Roi
        """
        assert not self.full_shape() is None, 'Full shape of the original image has not been given when constructing this roi'
        mask = np.ones(self.full_shape(), dtype=bool)
        roi = self.roi
        mask[roi[0]:roi[1], roi[2]:roi[3]] = False
        return mask

    def apply(self, image):
        """
        Crop an image using the roi. Extract only the rows and columns of interest.
        For a three dimensional array a matching is attempted to see which dimension should be broadcasted.
        """
        if self.empty():
            return image
        roi = self.roi
        if len(image.shape) == 2:
            image = image[roi[0]:roi[1], roi[2]:roi[3]]
        elif len(image.shape) == 3:
            assert not self.full_shape() is None, 'Full shape of the original image has not been given when constructing this roi'
            full_shape = tuple(self.full_shape())
            if image.shape[1:] == full_shape:
                image = image[:, roi[0]:roi[1], roi[2]:roi[3]]
            elif image.shape[:2] == full_shape:
                image = image[roi[0]:roi[1], roi[2]:roi[3], :]
            else:
                raise ValueError('Shape added as two last values in constructor {} does not match any of the image dimensions {}'.format(full_shape, image.shape))
        else:
            raise ValueError('Wrong number of image dimensions or not able to detemine the channel axis of images')
        return image

    def unapply(self, image):
        """
        Pad a cropped image (from apply) with zeros to get back to the full shape of the image
        """
        assert not self.full_shape() is None, 'Full shape of the original image has not been given when constructing this roi'
        roi = self.roi
        if self.empty():
            return image

        if len(image.shape) == 2:
            full_image = np.ma.zeros(roi[4:])
            full_image.mask = True
            full_image[roi[0]:roi[1], roi[2]:roi[3]] = image
        elif len(image.shape) == 3 and image.shape[0] == 3:
            full_shape = [image.shape[0],] + self.full_shape()
            full_image = np.ma.zeros(full_shape)
            full_image.mask = True
            full_image[:, roi[0]:roi[1], roi[2]:roi[3]] = image
        elif len(image.shape) == 3 and image.shape[0] == 3:
            full_shape = self.full_shape() + [image.shape[2],]
            full_image = np.ma.zeros(full_shape)
            full_image.mask = True
            full_image[roi[0]:roi[1], roi[2]:roi[3], :] = image
        else:
            raise ValueError('Wrong number of image dimensions or not able to detemine the channel axis of images')
        return full_image

    def apply_to_points(self, points):
        """
        Each row in the points array is point and the columns are x and y
        Update the points so that zero is on top left of roi
        """
        if self.empty():
            return points
        points = np.array(points)
        points[:, 0] -= self.roi[2]
        points[:, 1] -= self.roi[0]
        return points

    def unapply_to_points(self, points):
        """
        Each row in the points array is point and the columns are x and y
        Update the points that are in the roi coordinate system so that zero is on top left of the original image
        """
        if self.empty():
            return points
        points = np.array(points)
        points[:, 0] += self.roi[2]
        points[:, 1] += self.roi[0]
        return points

    def rebase(self, full_roi):
        """ Use a new roi as full image shape """
        if self.empty() or full_roi.empty():
            return
        full_roi = full_roi.roi
        new_roi = self.roi.copy()
        new_roi[0] -= full_roi[0]
        new_roi[1] -= full_roi[0]
        new_roi[2] -= full_roi[2]
        new_roi[3] -= full_roi[2]
        new_roi[4] = full_roi[1] - full_roi[0]
        new_roi[5] = full_roi[3] - full_roi[2]
        self.roi = new_roi

    def maximize(self, roi2):
        """ update this roi as one roi is large enough to enclose both self and roi2 """
        roi1 = self.roi
        roi2 = roi2.roi
        if roi1 is None and roi2 is None:
            roi = None
        elif roi1 is None:
            roi = roi2
        elif roi2 is None:
            roi = roi1
        else:
            roi = [min(roi1[0], roi2[0]),
                   max(roi1[1], roi2[1]),
                   min(roi1[2], roi2[2]),
                   max(roi1[3], roi2[3]),
                   max(roi1[4], roi2[4]),
                   max(roi1[5], roi2[5])]
        self.roi = roi
        
    def empty(self):
        return self.roi is None

    def full_shape(self):
        if self.empty() or len(self.roi) == 4:
            return None
        else:
            return tuple(self.roi[4:])

    def shape(self):
        h = self.roi[1] - self.roi[0]
        w = self.roi[3] - self.roi[2]
        return (h, w)

    def copy(self):
        if self.empty():
            return Roi()
        else:
            return Roi(self.roi.copy())

    def __str__(self):
        return "Roi: " + self.roi.__str__()

    def write(self, path):
        np.savetxt(path, self.roi, fmt='%d')
