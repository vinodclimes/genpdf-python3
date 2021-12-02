from .composant import ComposantPDF
from .document import DocumentPDF
from .dictionnaire import DictionnairePDF
from .nom import NomPDF


class FermeturePDF(ComposantPDF):
    """Un fichier PDF se termine par une séquence spécifique.

    Cette séquence est constituée de 3 sections :
    - un dictionnaire final dans la section "trailer"
    - la position de la table des références dans la section "startxref"
    - un marqueur de fin de fichier

    Exemple :

        trailer
        <<
        ...
        >>
        startxref
        123
        %%EOF

    """

    OUVERTURE_TRAILER = "trailer"
    OUVERTURE_STARTXREF = "startxref"
    FERMETURE_FICHIER = "%%EOF"

    def __init__(self, taille_table, position_table, reference_catalogue):
        super().__init__(separateur=DocumentPDF.SAUT_LIGNE)
        self.inserer(self.OUVERTURE_TRAILER)
        self.inserer(DictionnaireFermeture(taille_table, reference_catalogue))
        self.inserer(self.OUVERTURE_STARTXREF)
        self.inserer(position_table)
        self.inserer(self.FERMETURE_FICHIER)


class DictionnaireFermeture(DictionnairePDF):
    """Le dictionnaire de fermeture du document PDF.

    Clés obligatoires :
    - Size = le nombre d'entrées dans la table des références du document PDF
    - Root = une référence vers l'objet interne contenant le catalogue PDF

    Exemple :

        <<
        /Size 88
        /Root 6 0 R
        ...
        >>

    """

    def __init__(self, taille_table, reference_catalogue):
        super().__init__()
        self.inserer((NomPDF("Size"), taille_table))
        self.inserer((NomPDF("Root"), reference_catalogue))
