from .composant import ComposantPDF
from .document import DocumentPDF
from .nom import NomPDF


class DictionnairePDF(ComposantPDF):
    """Un dictionnaire de clés/valeurs dans la structure d'un document PDF.

    Les dictionnaires PDF s'écrivent entre doubles flèches (<< ... >>).
    Les clés/valeurs sont écrites séquentiellement, séparées par des espaces.

    Exemple :
    Un dictionnaire avec 3 entrées (Type, Size, Info), pourrait s'écrire :
        << /Type /Catalog /Size 88 /Info 87 0 R >>

    Le nom d'une clé permet de connaître le type de sa valeur, et donc de
    tenir compte des éventuels espaces internes à cette valeur à la relecture.

    Mais pour plus de clarté dans l'écriture, cette classe sépare les paires de
    clés/valeurs avec des sauts de lignes.

    Exemple :

         <<
         /Type /Catalog
         /Size 88
         /Info 87 0 R
         >>

    """

    SEPARATEUR_CLE_VALEUR = b" "
    OUVERTURE = "<<"
    FERMETURE = ">>"

    def __init__(self):
        super().__init__(separateur=DocumentPDF.SAUT_LIGNE)
        self.composant_interne_sequence = (
            ComposantPDF(separateur=DocumentPDF.SAUT_LIGNE))
        super().inserer(self.OUVERTURE)
        super().inserer(self.composant_interne_sequence)
        super().inserer(self.FERMETURE)

    def inserer(self, cle, valeur):
        composant_interne_cle_valeur = (
            ComposantPDF(separateur=self.SEPARATEUR_CLE_VALEUR))
        composant_interne_cle_valeur.inserer(NomPDF(cle))
        composant_interne_cle_valeur.inserer(valeur)
        self.composant_interne_sequence.inserer(composant_interne_cle_valeur)
