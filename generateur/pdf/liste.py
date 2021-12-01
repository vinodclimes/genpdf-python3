class ListePDF:

    PREFIXE = b"["
    SEPARATEUR = b" "
    SUFFIXE = b"]"

    def __init__(self):
        self.elements = []

    def ajouter(self, octets):
        self.elements.append(octets)

    def lire_octets(self):
        octets = b""
        octets += self.PREFIXE
        octets += self.SEPARATEUR.join(self.elements)
        octets += self.SUFFIXE
        return octets
