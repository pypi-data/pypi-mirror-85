from janis_core import File


class ZipFile(File):
    def __init__(self, optional=False, extension=".zip"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "Zip"

    def doc(self):
        return "A zip archive, ending with .zip"
