# ----------------------------------------------------------- class: ImageUrls ----------------------------------------------------------- #

class ImageUrls:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        d: dict
    ):
        self.raw = d['raw']
        self.full = d['full']
        self.regular = d['regular']
        self.small = d['small']
        self.thumb = d['thumb']
        core = self.raw.split('?')[0]
        self.hd = core + '?ixlib=rb-1.2.1&fm=jpg&crop=entropy&cs=tinysrgb&w={}&fit=max'.format(720)
        self.fullHD = core + '?ixlib=rb-1.2.1&fm=jpg&crop=entropy&cs=tinysrgb&w={}&fit=max'.format(1080)


# ---------------------------------------------------------------------------------------------------------------------------------------- #