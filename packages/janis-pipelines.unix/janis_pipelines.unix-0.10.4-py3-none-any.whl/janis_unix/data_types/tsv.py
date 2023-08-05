from janis_core import File

from janis_unix.data_types.text import TextFile


class Tsv(TextFile):
    def __init__(self, optional=False, extension=".tsv"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "tsv"

    def doc(self):
        return "A tab separated file"
