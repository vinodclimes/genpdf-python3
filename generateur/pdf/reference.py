from .assistant import lire_octets


class ReferenceObjetPDF:

    # Exemple : 42 0 R
    # Est une référence vers l'objet n°42 en version 0.

    SEPARATEUR = b" "
    MARQUEUR_REFERENCE = b"R"

    def __init__(self, numero, version=0):
        self.numero = numero
        self.version = version

    def lire_octets(self):
        return (lire_octets(self.numero)
                + self.SEPARATEUR
                + lire_octets(self.version)
                + self.SEPARATEUR
                + self.MARQUEUR_REFERENCE)
