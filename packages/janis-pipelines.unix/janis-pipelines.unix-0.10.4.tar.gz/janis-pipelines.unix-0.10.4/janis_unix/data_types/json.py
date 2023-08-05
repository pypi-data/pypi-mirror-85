from janis_core import File


class JsonFile(File):
    def __init__(self, optional=False, extension=".json"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "jsonFile"

    def doc(self):
        return "A JSON file file"
