from .document import Document


class Courrier:
    """Un document de type courrier.

    Le courrier ne contient qu'une seule page, au format courrier classique.
    Les méthodes de cette classe sont à appeler dans l'ordre de présentation.
    """

    MARGE_GAUCHE_MM = 25
    MARGE_HAUTE_MM = 25
    HAUTEUR_LIGNE_MM = 5.1

    TABULATION_ADRESSE = 100
    TABULATION_LIEU_DATE = 125
    TABLULATION_PARAGRAPHES = MARGE_GAUCHE_MM + 15
    TABULATION_SIGNATURE = MARGE_GAUCHE_MM + 90

    @classmethod
    def position_ligne(cls, numero_ligne):
        return cls.MARGE_HAUTE_MM + numero_ligne * cls.HAUTEUR_LIGNE_MM

    def __init__(self):
        self.document = Document()
        self.document.selectionner_page(1)
        self.document.definir_police(12, serif=False, gras=False)
        self.prochaine_ligne = 1

    def ajouter_nom_expediteur(self, nom):
        self.prochaine_ligne = 1
        self.document.positionner_curseur(
            self.MARGE_GAUCHE_MM, self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes([nom])
        self.prochaine_ligne += 2

    def ajouter_adresse_expediteur(self, lignes_adresse):
        self.document.positionner_curseur(
            self.MARGE_GAUCHE_MM, self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes(lignes_adresse)
        self.prochaine_ligne += 1 + len(lignes_adresse)

    def ajouter_contact_expediteur(self, lignes_contact):
        self.document.positionner_curseur(
            self.MARGE_GAUCHE_MM, self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes(lignes_contact)
        self.prochaine_ligne += len(lignes_contact)

    def ajouter_adresse_destinataire(self, lignes_adresse):
        self.prochaine_ligne = 6
        self.document.positionner_curseur(
            self.TABULATION_ADRESSE, self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes(lignes_adresse)
        self.prochaine_ligne += len(lignes_adresse)

    def ajouter_lieu_date(self, lieu_date):
        self.prochaine_ligne = 16
        self.document.positionner_curseur(
            self.TABULATION_LIEU_DATE,
            self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes([lieu_date])
        self.prochaine_ligne += 1

    def ajouter_objet(self, lignes_objet):
        self.document.positionner_curseur(
            self.MARGE_GAUCHE_MM, self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes(lignes_objet)
        self.prochaine_ligne += 2 + len(lignes_objet)

    def ajouter_formule_appel(self, formule):
        self.document.positionner_curseur(
            self.TABLULATION_PARAGRAPHES,
            self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes([formule])
        self.prochaine_ligne += 2

    def ajouter_paragraphe(self, lignes_paragraphe):
        self.document.positionner_curseur(
            self.TABLULATION_PARAGRAPHES,
            self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes([lignes_paragraphe[0]])
        self.prochaine_ligne += 1
        if len(lignes_paragraphe) > 1:
            self.document.positionner_curseur(
                self.MARGE_GAUCHE_MM,
                self.position_ligne(self.prochaine_ligne))
            self.document.ecrire_lignes(lignes_paragraphe[1:])
        self.prochaine_ligne += len(lignes_paragraphe)

    def ajouter_formule_politesse(self, lignes_formule):
        self.ajouter_paragraphe(lignes_formule)

    def ajouter_nom_signataire(self, nom):
        self.prochaine_ligne += 1
        self.document.positionner_curseur(
            self.TABULATION_SIGNATURE,
            self.position_ligne(self.prochaine_ligne))
        self.document.ecrire_lignes([nom])
        self.prochaine_ligne += 1
