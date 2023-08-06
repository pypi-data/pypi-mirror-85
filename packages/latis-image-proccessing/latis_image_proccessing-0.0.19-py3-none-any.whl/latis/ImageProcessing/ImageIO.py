import gdcm
import pydicom
import numpy as np
from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000, RLELossless, ImplicitVRLittleEndian
from pydicom.filebase import DicomFileLike

from .Image import Image


class ImageIO:
    # private
    @staticmethod
    def ensure_even(stream):
        # Very important for some viewers
        if len(stream) % 2:
            return stream + b"\x00"
        return stream

    @staticmethod
    def loadImage(file):
        ds = pydicom.dcmread(file)
        pixel_array = np.uint16(ds.pixel_array)
        cols = ds.Columns
        rows = ds.Rows
        return Image(pixel_array, cols, rows, ds)

    @staticmethod
    def saveImage(image):
        # TODO : edit height and width elements
        dataset = ImageIO.buildDataSetImplicitVRLittleEndian(image)
        return ImageIO.write_dataset_to_bytes(dataset)

    @staticmethod
    def save_as(image, filename):
        # TODO : edit height and width elements
        dataset = ImageIO.buildDataSetImplicitVRLittleEndian(image)
        dataset.save_as(filename)
        return filename

    @staticmethod
    def buildDataSetJPEG2000(image):
        from io import BytesIO
        from PIL import Image as PImage
        dataset = image.dataset
        pixels = image.pixelData
        frame_data = []
        with BytesIO() as output:
            image = PImage.fromarray(pixels)
            image.save(output, format="JPEG2000")
            frame_data.append(output.getvalue())
        dataset.PixelData = encapsulate(frame_data)
        dataset.file_meta.TransferSyntaxUID = JPEG2000
        dataset.is_implicit_VR = False
        return dataset

    @staticmethod
    def buildDataSetImplicitVRLittleEndian(image):
        dataset = image.dataset
        pixels = image.pixelData
        dataset.PixelData = pixels.tobytes()
        dataset.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
        dataset.is_implicit_VR = True
        return dataset

    @staticmethod
    def write_dataset_to_bytes(dataset):
        # create a buffer
        with BytesIO() as buffer:
            # create a DicomFileLike object that has some properties of DataSet
            memory_dataset = DicomFileLike(buffer)
            # write the dataset to the DicomFileLike object
            dcmwrite(memory_dataset, dataset)
            # to read from the object, you have to rewind it
            memory_dataset.seek(0)
            # read the contents as bytes
            return memory_dataset.read()

    @staticmethod
    def toJSON(image:Image):
        return image.dataset.to_json_dict()
