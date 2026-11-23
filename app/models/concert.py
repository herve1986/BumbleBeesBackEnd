from datetime import date, time


class Concert:
    def __init__(
        self,
        id: int | None = None,
        address: str | None = None,
        city: str = "",
        date_concert: date | None = None,
        time_concert: time | None = None
    ):
        self.id = id
        self.address = address
        self.city = city
        self.date_concert = date_concert
        self.time_concert = time_concert