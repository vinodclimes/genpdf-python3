from generateur.document.document import Document
from generateur.document.generateur import GenerateurDocumentPDF


def construire_pdf_test():
    document = Document()

    document.ecrire_lignes([
        "Ceci est un document PDF de démonstration",
        "composé de 2 lignes. "
    ])

    document.positionner_curseur(50, 100)
    document.definir_police(12, serif=False, gras=True)
    document.ecrire_lignes(["Changement de position et de police"])

    document.selectionner_page(3)
    document.positionner_curseur(80, 100)
    document.definir_police(8, gras=True)
    document.ecrire_lignes(["Ecriture sur la page n°3"])

    return GenerateurDocumentPDF.generer(document)


if __name__ == "__main__":

    octets_document_pdf = construire_pdf_test()
    nom_fichier_pdf = "exemple.pdf"

    nombre_octets_ecrits = 0
    with open(nom_fichier_pdf, "wb") as fichier:
        nombre_octets_ecrits = fichier.write(octets_document_pdf)

    print(f"Nombre d'octets écrits : {nombre_octets_ecrits}. ")
