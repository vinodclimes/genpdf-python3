from .composant import ComposantPDF
from .document import DocumentPDF
from .nom import NomPDF


class BlocTextePDF(ComposantPDF):
    """Un bloc de lignes de texte à insérer dans le contenu d'une page PDF.

    Les lignes de texte sont dessinées en utilisant des opérateurs PDF.
    Par exemple : un opérateur pour déclarer la police, la position,
    ou encore pour écrire une séquence de codes (caractères Latin1).
    """

    SEPARATEUR = b" "
    OUVERTURE = "BT"
    FERMETURE = "ET"
    OUVERTURE_CODES = "("
    FERMETURE_CODES = ")"
    OPERATION_SAUVEGARDE_CONTEXTE = "q"
    OPERATION_RESTAURATION_CONTEXTE = "Q"
    OPERATION_COULEUR_NOIRE = "0 0 0 rg"
    OPERATEUR_POLICE = "Tf"
    OPERATEUR_POSITION = "Td"
    OPERATEUR_CODES = "Tj"
    OPERATEUR_SAUT_LIGNE = "T*"

    RESERVATION = (len(OUVERTURE_CODES)
                   + len(FERMETURE_CODES)
                   + len(SEPARATEUR)
                   + len(OPERATEUR_CODES)
                   + len(DocumentPDF.SAUT_LIGNE))

    DISPONIBLE = DocumentPDF.LONGUEUR_MAX_LIGNE - RESERVATION

    CARACTERES_A_ECHAPPER = "()\\"

    @classmethod
    def ajouter_code(cls, code_unicode, codes, sequences_codes):
        if len(codes) < cls.DISPONIBLE:
            codes += bytes([code_unicode])
        else:
            sequences_codes.append(codes)
            codes = bytes([code_unicode])
        return codes

    @classmethod
    def ajouter_code_echappement(cls, code_unicode, codes, sequences_codes):
        if len(codes) < cls.DISPONIBLE - 1:
            codes += b"\\"
            codes += bytes([code_unicode])
        else:
            sequences_codes.append(codes)
            codes = b"\\"
            codes += bytes([code_unicode])
        return codes

    @classmethod
    def decouper_ligne(cls, ligne):
        sequences_codes = []
        codes = b""
        for caractere in ligne:
            code_unicode = ord(caractere)
            if code_unicode < 256:  # Latin1
                if caractere in cls.CARACTERES_A_ECHAPPER:
                    codes = cls.ajouter_code_echappement(
                        code_unicode, codes, sequences_codes)
                else:
                    codes = cls.ajouter_code(
                        code_unicode, codes, sequences_codes)
        sequences_codes.append(codes)
        return sequences_codes

    def __init__(self, position, police, lignes=None):
        super().__init__()
        self.position = position
        self.police = police
        if lignes is not None:
            for ligne in lignes:
                super().inserer(ligne)

    def construire_composant_position(self):
        composant = ComposantPDF(separateur=self.SEPARATEUR)
        composant.inserer(self.position)
        composant.inserer(self.OPERATEUR_POSITION)
        return composant

    def construire_composant_police(self):
        composant = ComposantPDF(separateur=self.SEPARATEUR)
        composant.inserer(NomPDF(self.police.nom_interne))
        composant.inserer(self.police.taille)
        composant.inserer(self.OPERATEUR_POLICE)
        return composant

    def construire_composant_codes(self, codes):
        composant_codes = ComposantPDF()
        composant_codes.inserer(self.OUVERTURE_CODES)
        composant_codes.inserer(codes)
        composant_codes.inserer(self.FERMETURE_CODES)
        composant_operation = ComposantPDF(separateur=self.SEPARATEUR)
        composant_operation.inserer(composant_codes)
        composant_operation.inserer(self.OPERATEUR_CODES)
        return composant_operation

    def __bytes__(self):
        composant_rendu = ComposantPDF(separateur=DocumentPDF.SAUT_LIGNE)
        composant_rendu.inserer(self.OPERATION_SAUVEGARDE_CONTEXTE)
        composant_rendu.inserer(self.OPERATION_COULEUR_NOIRE)
        composant_rendu.inserer(self.OUVERTURE)
        composant_rendu.inserer(self.construire_composant_position())
        composant_rendu.inserer(self.construire_composant_police())
        for ligne in self.elements:
            sequences_codes = self.decouper_ligne(ligne)
            for codes in sequences_codes:
                composant_rendu.inserer(self.construire_composant_codes(codes))
            composant_rendu.inserer(self.OPERATEUR_SAUT_LIGNE)
        composant_rendu.inserer(self.FERMETURE)
        composant_rendu.inserer(self.OPERATION_RESTAURATION_CONTEXTE)
        return bytes(composant_rendu)
