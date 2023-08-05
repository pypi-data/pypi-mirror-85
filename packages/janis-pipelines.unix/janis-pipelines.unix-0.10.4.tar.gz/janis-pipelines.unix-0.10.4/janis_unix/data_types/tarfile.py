from janis_core import File


class TarFile(File):
    def __init__(self, optional=False, extension=".tar"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "TarFile"

    def doc(self):
        return "A tarfile, ending with .tar"


class TarFileGz(File):
    def __init__(self, optional=False, extension=".tar.gz"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "CompressedTarFile"

    def doc(self):
        return "A gzipped tarfile"
