from .composant import ComposantPDF
from .document import DocumentPDF


class TableReferencesPDF(ComposantPDF):
    """La table des références d'un document PDF.

    Cette table contient les positions des objets internes à la structure PDF.

    Elle démarre par le marqueur "xref".
    La ligne suivante indique son premier indice (0) et sa taille (1+N).
    Elle comporte une entrée "zéro", suivie de N entrées d'indices 1 à N.
    L'entrée d'indice <i> indique la position et la version de l'objet <i>.

    Exemple :

        xref
        0 4
        0000000000 65535 f
        0000025914 00000 n    <== Objet n°1 version 0, situé en 25914
        0000026000 00000 n    <== Objet n°2 version 0, situé en 26000
        0000000192 00000 n    <== Objet n°3 version 0, situé en 192

    """

    SEPARATEUR_INDICES = b" "
    SEPARATEUR_ELEMENTS_ENTREE = b" "
    OUVERTURE = "xref"
    ENTREE_ZERO = "0000000000 65535 f"
    MARQUEUR_OCCUPATION = "n"
    ESPACE_FINAL = " "

    @classmethod
    def creer_entree_zero(cls):
        return ComposantPDF(cls.ENTREE_ZERO)

    @classmethod
    def creer_entree(cls, position, version=0):
        composant_entree = (
            ComposantPDF(separateur=cls.SEPARATEUR_ELEMENTS_ENTREE))
        texte_position = f"{position:010}"
        texte_version = f"{version:05}"
        composant_entree.inserer(texte_position)
        composant_entree.inserer(texte_version)
        composant_entree.inserer(cls.MARQUEUR_OCCUPATION)
        return composant_entree

    @classmethod
    def finaliser_entree(cls, composant_entree):
        # Un espace final est nécessaire pour atteindre 20 octets
        # si le marqueur de fin de ligne ne fait pas 2 octets de long.
        if len(DocumentPDF.SAUT_LIGNE) < 2:
            composant_englobant = ComposantPDF(composant_entree)
            composant_englobant.inserer(cls.ESPACE_FINAL)
            return composant_englobant
        else:
            return composant_entree

    def __init__(self):
        super().__init__(self.OUVERTURE, separateur=DocumentPDF.SAUT_LIGNE)
        self.entrees = []

    def ajouter_entree(self, position_objet_dans_fichier):
        self.entrees.append(position_objet_dans_fichier)
        return self

    def finaliser(self):
        composant_indices = ComposantPDF(separateur=self.SEPARATEUR_INDICES)
        composant_indices.inserer(0)
        composant_indices.inserer(self.lire_nombre_entrees())
        self.inserer(composant_indices)
        self.inserer(self.finaliser_entree(self.creer_entree_zero()))
        for position in self.entrees:
            composant = self.finaliser_entree(self.creer_entree(position))
            self.inserer(composant)
        return self

    def lire_nombre_entrees(self):
        return (1 + len(self.entrees))
