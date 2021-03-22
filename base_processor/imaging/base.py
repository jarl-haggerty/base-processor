# internal
from base_processor import BaseProcessor


class BaseImageProcessor(BaseProcessor):
    def __init__(self, *args, **kwargs):
        super(BaseImageProcessor, self).__init__(*args, **kwargs)

        # Output
        self.outputs = []

    def create_output_image(self, pathname, properties=None):
        raise NotImplementedError("Function create_output_image in base_processor.imaging.base has not been implemented yet.")

    def finalize(self):
        raise NotImplementedError("Function finalize in base_processor.imaging.base has not been implemented yet.")
