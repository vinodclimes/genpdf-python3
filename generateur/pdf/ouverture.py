from .ligne import LignePDF


class OuverturePDF:

    MARQUEUR_VERSION = b"%PDF-1.4"

    def lire_octets(self):
        return LignePDF(self.MARQUEUR_VERSION).lire_octets()
