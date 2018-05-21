from PIL import Image
import os.path
import simplePicStegoError
import struct
import simplePicStegoDefines


class SimplePicStegoFileDoesNotExist(simplePicStegoError.Error):
    def __init__(self, message=None):
        self.message = message


class PicEmbed(object):
    def __init__(self, filename):
        """
        Class to embed message into a picture

        :param filename: picture to use
        :param message_to_embed: message to embed
        """
        self.filename = filename
        self.image = None
        self.pix_array = []
        self.current_width = 0
        self.current_height = 0

    def embed_message(self, message):
        self._open_image()
        self.pix_array = self.image.load()

        # the message packet will look like <indicator><msg_len><msg>

        # ensure that there is enough room in the picture to store the message
        # Indicator will be max of 2 bytes, length = 4, and the message * 8
        full_msg_len = 2 + 4 + (len(message) * 8)
        if full_msg_len > (self.image.size[0] * self.image.size[1]):
            raise simplePicStegoError.Error("Message is too large")

        # set indicator
        message_to_embed = struct.pack(">H", simplePicStegoDefines.indicator)
        # append length
        message_to_embed += struct.pack(">I", len(message))

        # append message as byte string
        for c in message:
            message_to_embed += struct.pack(">B", ord(c))

        next_pixel_iter = self._get_next_pixel()
        for byte in message_to_embed:
            for bit_shift in range(8):
                new_bit = ((byte << bit_shift) & 0x80) >> 7
                pixel = next_pixel_iter.__next__()
                # Going to use the red pixel for now. Can configure later
                pixel = ((pixel[0] & 0xfe | new_bit), pixel[1], pixel[2])
                self.pix_array[self.current_height, self.current_width] = pixel

        self.image.save(self.filename.split(".")[1] + "_new.png")
        print("Finished encoding")

    def _open_image(self):
        if not os.path.isfile(self.filename):
            raise SimplePicStegoFileDoesNotExist("Could not find file %s." % self.filename)

        self.image = Image.open(self.filename)

    def _get_next_pixel(self):
        image_width, image_height = self.image.size
        for i in range(image_height):
            for j in range(image_width):
                self.current_height = i
                self.current_width = j
                yield self.pix_array[i, j]
        else:
            raise simplePicStegoError.Error("All out of picture")


if __name__ == "main":
    pass
