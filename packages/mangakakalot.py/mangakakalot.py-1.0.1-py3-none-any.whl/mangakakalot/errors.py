class Error(Exception):
    pass


class NotMangakakalot(Error):
    def __init__(self, message):
        self.message = message


class WrongMangaId(Error):
    def __init__(self, message):
        self.message = message
