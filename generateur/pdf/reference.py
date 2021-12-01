from .assistant import en_octets


class ReferenceObjetPDF:

    # Exemple : une référence vers l'objet n°42 en version 0.
    #
    #     42 0 R

    SEPARATEUR = b" "
    MARQUEUR_REFERENCE = b"R"

    def __init__(self, numero, version=0):
        self.numero = numero
        self.version = version

    def lire_octets(self):
        return (en_octets(self.numero)
                + self.SEPARATEUR
                + en_octets(self.version)
                + self.SEPARATEUR
                + self.MARQUEUR_REFERENCE)
