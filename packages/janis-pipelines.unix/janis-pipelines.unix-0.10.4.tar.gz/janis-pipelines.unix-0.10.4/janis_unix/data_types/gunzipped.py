from janis_core import File

from janis_unix.data_types.text import TextFile


class Gunzipped(File):
    def __init__(self, inner_type=File(), optional=False, extension=".gz"):
        super().__init__(optional, extension=extension)
        self.inner_type = inner_type

    def id(self):
        inner = f"Gzipped<{self.inner_type.name()}>"
        if self.optional:
            return f"Optional<{inner}>"
        return inner

    @staticmethod
    def name():
        return "Gzip"

    def doc(self):
        return "A gzipped file"
