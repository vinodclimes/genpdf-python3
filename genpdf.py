from generateur.document.courrier import Courrier
from generateur.document.generateur import GenerateurDocumentPDF


def construire_courrier_pdf():

    courrier = Courrier()
    courrier.ajouter_nom_expediteur("Jean DUPOND")
    courrier.ajouter_adresse_expediteur([
        "42, rue Principale",
        "75001 Paris"
    ])
    courrier.ajouter_contact_expediteur([
        "06 06 06 06 06",
        "jean.dupond@example.com"
    ])
    courrier.ajouter_adresse_destinataire([
        "Services municipaux",
        "Mairie de Paris",
        "1, rue Principale",
        "75001 Paris"
    ])
    courrier.ajouter_lieu_date("Paris, le 1er décembre 2021. ")
    courrier.ajouter_objet([
        "Objet : demande de renseignements. ",
        "PJ : avis d'imposition. "
    ])
    courrier.ajouter_formule_appel("Madame, Monsieur")
    courrier.ajouter_paragraphe([
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod",
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        "nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis",
        "aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla",
        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia",
        "deserunt mollit anim id est laborum."
    ])
    courrier.ajouter_paragraphe([
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium",
        "doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore",
        "veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam",
        "voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur",
        "magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, ",
        "qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non",
        "numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat",
        "voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis",
        "suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? "
    ])
    courrier.ajouter_formule_politesse([
        "En espérant que ma demande retiendra votre attention, veuillez agréer,",
        "Madame, Monsieur, ma considération distinguée. "
    ])
    courrier.ajouter_nom_signataire("Jean DUPOND")

    return GenerateurDocumentPDF.generer_courrier(courrier)


if __name__ == "__main__":

    octets_document_pdf = construire_courrier_pdf()
    nom_fichier_pdf = "exemple.pdf"

    nombre_octets_ecrits = 0
    with open(nom_fichier_pdf, "wb") as fichier:
        nombre_octets_ecrits = fichier.write(octets_document_pdf)

    print(f"Nombre d'octets écrits : {nombre_octets_ecrits}. ")
