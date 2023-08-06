import pydicom
import copy


class Image(object):
    """
    image container representing an image

    """

    def __init__(self, pixelData, cols: int, rows: int, dataset: pydicom.Dataset):
        self.pixelData = pixelData
        self.width = cols
        self.height = rows
        self.dataset = dataset

    @property
    def dtype(self):
        return self.pixelData.dtype.name

    @property
    def pixelFormat(self):
        pixelformat = self.dataset['PhotometricInterpretation'].value
        if pixelformat == 'MONOCHROME2' or pixelformat == 'MONOCHROME1':
            return 'GL'
        else:
            return pixelformat

    def Clone(self):
        pixels = copy.deepcopy(self.pixelData)
        dataset = copy.deepcopy(self.dataset)
        height = copy.deepcopy(self.height)
        width = copy.deepcopy(self.width)
        return Image(pixels, width, height, dataset)

    def MetaData(self, key):
        return self.dataset[key]
