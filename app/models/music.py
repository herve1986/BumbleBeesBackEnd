
class Music:
    def __init__(
        self,
        id: int | None = None,
        title: str = "",
        group_id: int | None = None
    ):
        self.id = id
        self.title = title
        self.group_id = group_id

        