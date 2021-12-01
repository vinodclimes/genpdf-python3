from .assistant import lire_octets


class NomPDF:

    # Exemple : /MediaBox
    # Les noms commencent par une barre oblique.

    PREFIXE = b"/"

    def __init__(self, nom):
        self.nom = nom

    def lire_octets(self):
        return self.PREFIXE + lire_octets(self.nom)
