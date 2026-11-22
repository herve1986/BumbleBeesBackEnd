
class Concert:
    def __init__(
        self,
        id: int | None = None,
        address: str | None = None,
        city: str = "",
        date: str | None = None,
        hour: str | None = None
    ):
        self.id = id
        self.address = address
        self.city = city
        self.date = date
        self.hour = hour

        