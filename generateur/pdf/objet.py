from .composant import ComposantPDF
from .document import DocumentPDF


class ObjetPDF(ComposantPDF):
    """Un objet interne, référençable dans la structure d'un document PDF.

    Un objet PDF possède un numéro, une version, et un contenu
    placé entre deux marqueurs : "obj" et "endobj".

    #Exemple : objet n°1 version 0

         1 0 obj
         ... contenu ...
         endobj

    """

    SEPARATEUR_SEQUENCE_DEMARRAGE = b" "
    OUVERTURE = "obj"
    FERMETURE = "endobj"

    def __init__(self, numero, contenu=None, version=0):
        super().__init__(separateur=DocumentPDF.SAUT_LIGNE)
        self.numero_objet = numero
        composant_interne_sequence = (
            ComposantPDF(separateur=self.SEPARATEUR_SEQUENCE_DEMARRAGE))
        composant_interne_sequence.inserer(numero)
        composant_interne_sequence.inserer(version)
        composant_interne_sequence.inserer(self.OUVERTURE)
        self.inserer(composant_interne_sequence)
        if contenu is not None:
            self.inserer(contenu)
        self.inserer(self.FERMETURE)
