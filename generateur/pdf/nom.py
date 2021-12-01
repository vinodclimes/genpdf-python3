from .assistant import en_octets


class NomPDF:

    # Exemple : le nom "MediaBox"
    #
    #     /MediaBox
    #
    # Les noms commencent par une barre oblique.

    PREFIXE = b"/"

    def __init__(self, nom):
        self.nom = nom

    def lire_octets(self):
        return self.PREFIXE + en_octets(self.nom)
