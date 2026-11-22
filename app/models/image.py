
class Image:
    def __init__(
        self,
        id: int | None = None,
        title: str | None = None,
        url: str = ""
    ):
        self.id = id
        self.title = title
        self.url = url

        