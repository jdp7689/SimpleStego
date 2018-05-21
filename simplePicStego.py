import argparse
import simplePicStegoEmbed
import simplePicStegoError
import simplePicStegoReveal


class UnknownFunctionError(simplePicStegoError.Error):
    """
    Raise error when unknown commands are given
    """
    def __init__(self, message):
        self.message = message;


version = "1.0"


def init_program():
    parser = argparse.ArgumentParser(description="An app that embeds strings into images")
    # parser.add_argument("--version", action="version", version="%(prog)s %s" % version)
    parser.add_argument("-e", action="store", dest="encode_file", help="The file name to store the string",
                        default=False)
    parser.add_argument("-m", action="store", dest="message", help="The message to store. Combine with -e",
                        default=None)
    parser.add_argument("-d", action="store", dest="decode_file", help="The file to extract the message")

    results = parser.parse_args()

    if (results.encode_file and results.decode_file) or (not results.emcode_file and not results.decode_file):
        raise UnknownFunctionError("Must either encode or decode a file")

    elif results.encode_file:  # create object to encode message into file and perform operation
        if results.encode_file.split(".")[1] != "png":
            raise simplePicStegoError.Error("Can only support png file right now")
        simplePicStegoEmbed.PicEmbed(results.encode_file, results.message).embed_message()

    elif results.decode_file:  # create object to attempt to find a message within an image file
        if results.decode_file.split(".")[1] != "png":
            raise simplePicStegoError.Error("Can only support png file right now")
        message = simplePicStegoReveal.SimplePicStegoReveal(results.decode_file).reveal()
        print(message)


def main():
    init_program()


if __name__ == '__main__':
    main()
