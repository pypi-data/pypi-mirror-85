import logging

"""
this a small example of a noop op
"""
class GenericOperation:

    def init(self, params):
        """if you have any sort of predefined varibles or  parameters tha need to be initialize

        Args:
            params : intilization parameters
        """
        logging.info('Init')  # will not print anything

    def applyTransformation(self, image, params):
        """
        Main Entry Point for operations 
        image : Image Container  
        image.pixelData = numpy array  
        image.height = cols  
        image.width = rows  
        image.dataset = dataset ( original image file  container refrence)   

        #### example : https://pydicom.github.io/pydicom/stable/auto_examples/image_processing/plot_downsize_image.html#sphx-glr-auto-examples-image-processing-plot-downsize-image-py
        ```
            get the pixel information into a numpy array
            data = ds.pixel_array
            data_downsampling = data[::8, ::8]
            data_downsampling.shape[0], data_downsampling.shape[1]))
        ```
        """
        return image
