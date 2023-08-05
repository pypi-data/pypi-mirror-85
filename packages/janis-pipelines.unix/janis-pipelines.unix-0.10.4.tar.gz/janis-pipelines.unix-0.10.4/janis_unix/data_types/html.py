from janis_core import File


class HtmlFile(File):
    def __init__(self, optional=False, extension=".html"):
        super().__init__(optional, extension=extension)

    @staticmethod
    def name():
        return "HtmlFile"

    def doc(self):
        return "A HTML file"
