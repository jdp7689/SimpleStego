from PIL import Image
import os.path
import simplePicStegoError
import simplePicStegoDefines


class SimplePicStegoReveal(object):
    def __init__(self, jpeg_filename):
        self.filename = jpeg_filename
        self.image = None
        self.pix_array = []
        self.picture_size = 0
        self.pix_iter = None

    def reveal(self):
        """
        Reveals the message embedded in the image

        :return: Message retrieved
        """
        self._open_image()

        self.pix_array = self.image.load()
        self.picture_size = (self.image.size[0] * self.image.size[1])
        self.pix_iter = self._get_next_pixel()

        self._search_for_indicator()

        message_len = self._get_len_of_message()

        return self._get_message(message_len)

    def _get_message(self, msg_len):
        """

        :param msg_len: length of message
        :return: message extracted from picture
        """
        message = ""

        for i in range(msg_len):
            message += chr(self._get_byte_from_pix())

        return message

    def _search_for_indicator(self):
        """
        Searches image for indicator. Raises except of none found.

        Should be run first when extracting message
        :return: None
        """
        # Indicator will be 2 bytes
        indicator = self._get_byte_from_pix()
        try:
            while True:
                indicator = (indicator << 8) & 0xffff
                indicator = indicator | self._get_byte_from_pix()
                if indicator == simplePicStegoDefines.indicator:
                    return

        except simplePicStegoError.Error:
            raise simplePicStegoError.Error("Could not find indicator")

    def _get_len_of_message(self):
        """
        Gets the length of the message from the file. Should be 4 bytes
        :return: size of message
        """
        str_len = 0

        for i in range(4):
            str_len = str_len << 4
            str_len = str_len | self._get_byte_from_pix()

        return str_len

    def _get_byte_from_pix(self):
        """
        Retrieve the next byte from the image

        :return: next byte extracted from image
        """
        if not self.pix_iter:
            self.pix_iter = self._get_next_pixel()
        byte = 0
        for i in range(8):
            byte = byte << 1
            pixel = self.pix_iter.__next__()
            byte = byte | (pixel[0] & 1)

        return byte

    def _get_next_pixel(self):
        image_width, image_height = self.image.size
        for i in range(image_height):
            for j in range(image_width):
                self.current_height = i
                self.current_width = j
                yield self.pix_array[i, j]
        else:
            raise simplePicStegoError.Error("All out of picture")

    def _open_image(self):
        if not os.path.isfile(self.filename):
            raise simplePicStegoError.Error("Could not find file %s." % self.filename)

        self.image = Image.open(self.filename)
