from pathlib import Path
from urllib.parse import quote

# CONFIGURATION
DOSSIER = Path(r".")
FICHIER_SORTIE = Path("photos360.js")


# VÉRIFICATION DU DOSSIER
if not DOSSIER.exists():
    print(f"ERREUR : le dossier n'existe pas : {DOSSIER}")
    input("Appuie sur Entrée pour fermer...")
    exit()

if not DOSSIER.is_dir():
    print(f"ERREUR : le chemin indiqué n'est pas un dossier : {DOSSIER}")
    input("Appuie sur Entrée pour fermer...")
    exit()


# CONSTRUCTION DE L'ARBORESCENCE
def construire_arbre(dossier):
    """
    Construit une structure récursive en ne conservant
    que les dossiers contenant au moins une image JPG/JPEG/PNG.
    """

    elements = []

    try:
        contenus = sorted(
            list(dossier.iterdir()),
            key=lambda f: (
                0 if f.is_dir() else 1,
                f.name.lower()
            )
        )
    except Exception:
        return elements

    for fichier in contenus:
        # DOSSIER
        if fichier.is_dir():

            # On construit d'abord son contenu
            enfants = construire_arbre(fichier)

            # On n'ajoute le dossier que s'il contient
            # au moins une image, directement ou indirectement
            if len(enfants) > 0:
                elements.append({
                    "type": "dir",
                    "name": fichier.name,
                    "children": enfants
                })

        # FICHIER
        elif fichier.is_file():

            # Uniquement les images autorisées
            if fichier.suffix.lower() not in (
                ".jpg",
                ".jpeg",
                ".png"
            ):
                continue

            chemin_relatif = fichier.relative_to(DOSSIER)

            elements.append({
                "type": "file",
                "name": fichier.name,
                "path": str(chemin_relatif)
            })

    return elements


arbre = construire_arbre(DOSSIER)


# GÉNÉRATION DU HTML
lignes = []
lignes.append("window.popupPhotos360HTML =")
lignes.append("    '<b class=\"titleb\">Photos 360°</b><hr class=\"titlehr\">' +")


# FILTRE
lignes.append(
    "    '<input type=\"text\" id=\"filterPhotos360\" "
    "style=\"width:100%;box-sizing:border-box;\" "
    "placeholder=\"Filtrer...\" "
    "onkeyup=\"filtrerPhotos360(this.value);\">' +"
)


# DÉBUT DE L'ARBORESCENCE
lignes.append("    '<div id=\"photos360List\" class=\"photos360Tree\">' +")


# FONCTION POUR ÉCHAPPER LE HTML
def echapper_html(texte):
    return (
        texte
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


#GÉNÉRATION RÉCURSIVE
def generer_html(elements, profondeur=0):

    for element in elements:

        # DOSSIER
        if element["type"] == "dir":

            nom = element["name"]

            lignes.append(
                "    '<div class=\"photo360Dossier\">"
                "<span class=\"photo360Toggle\" "
                "onclick=\"togglePhotos360Dossier(this)\">▾</span>"
                "<span class=\"photo360DossierNom\">"
                + echapper_html(nom)
                + "</span>"
                "</div>' +"
            )

            lignes.append(
                "    '<div class=\"photo360DossierContenu\">' +"
            )

            lignes.append("    '<ul>' +")

            generer_html(
                element["children"],
                profondeur + 1
            )

            lignes.append("    '</ul>' +")
            lignes.append("    '</div>' +")

        # FICHIER
        else:

            nom = element["name"]
            chemin = element["path"]

            # Conversion en chemin URL avec /
            chemin_url = chemin.replace("\\", "/")

            # Encodage de chaque partie du chemin
            morceaux = chemin_url.split("/")

            morceaux_url = []

            for morceau in morceaux:
                morceaux_url.append(
                    quote(morceau, safe="")
                )

            chemin_url = "/".join(morceaux_url)

            lignes.append(
                "    '<li class=\"photo360Fichier\">"
                "<a class=\"photo360Nom\" "
                "href=\"?file=../photos360/"
                + chemin_url
                + "\">"
                + echapper_html(nom)
                + "</a>"
                "<a href=\"../photos360/"
                + chemin_url
                + "\" download> [↓]</a>"
                "</li>' +"
            )


generer_html(arbre)


# FIN DE L'ARBORESCENCE
lignes.append("    '</div>';")


# JAVASCRIPT : OUVERTURE / FERMETURE DES DOSSIERS
lignes.append("")
lignes.append("function togglePhotos360Dossier(el){")
lignes.append("    var contenu=el.parentNode.nextSibling;")
lignes.append("    if(!contenu)return;")
lignes.append("    if(contenu.style.display==='none'){")
lignes.append("        contenu.style.display='';")
lignes.append("        el.innerHTML='▾';")
lignes.append("    }else{")
lignes.append("        contenu.style.display='none';")
lignes.append("        el.innerHTML='▸';")
lignes.append("    }")
lignes.append("}")


# JAVASCRIPT : FILTRE
lignes.append("")
lignes.append("function filtrerPhotos360(texte){")
lignes.append("    texte=sansAccents(texte.toLowerCase());")
lignes.append("    var racine=document.getElementById('photos360List');")
lignes.append("    if(!racine)return;")
lignes.append("    var dossiers=racine.getElementsByClassName('photo360Dossier');")
lignes.append("    var fichiers=racine.getElementsByClassName('photo360Fichier');")

# FICHIERS
lignes.append("    var i,j;")
lignes.append("    for(i=0;i<fichiers.length;i++){")
lignes.append("        var lien=fichiers[i].getElementsByClassName('photo360Nom')[0];")
lignes.append("        var nom=sansAccents(lien.textContent.toLowerCase());")
lignes.append(
    "        fichiers[i].style.display="
    "nom.indexOf(texte)>=0?'':'none';"
)
lignes.append("    }")

# DOSSIERS
lignes.append("    for(i=0;i<dossiers.length;i++){")
lignes.append("        var dossier=dossiers[i];")
lignes.append(
    "        var nomDossier="
    "sansAccents(dossier.getElementsByClassName("
    "'photo360DossierNom')[0].textContent.toLowerCase());"
)
lignes.append("        var contenu=dossier.nextSibling;")
lignes.append("        var visible=false;")

# LE NOM DU DOSSIER CORRESPOND
lignes.append("        if(texte==='' || nomDossier.indexOf(texte)>=0){")
lignes.append("            visible=true;")
lignes.append("        }")
# CHERCHER UN FICHIER VISIBLE DANS LE DOSSIER
lignes.append("        if(!visible && contenu){")
lignes.append("            var enfants=contenu.getElementsByTagName('li');")
lignes.append("            for(j=0;j<enfants.length;j++){")
lignes.append("                if(enfants[j].style.display!=='none'){")
lignes.append("                    visible=true;")
lignes.append("                    break;")
lignes.append("                }")
lignes.append("            }")
lignes.append("        }")

# AFFICHAGE
lignes.append("        dossier.style.display=visible?'':'none';")
lignes.append("        if(texte!=='' && visible && contenu){")
lignes.append("            contenu.style.display='';")
lignes.append(
        "            var bouton=dossier.getElementsByClassName("
        "'photo360Toggle')[0];"
)
lignes.append("            if(bouton)bouton.innerHTML='▾';")
lignes.append("        }")
lignes.append("    }")
lignes.append("}")


# FONCTION SANS ACCENTS
lignes.append("")
lignes.append("function sansAccents(str){return str")
lignes.append('        .replace(/[_]/g, " ")')
lignes.append('        .replace(/[àáâãäå]/g, "a")')
lignes.append('        .replace(/[ç]/g, "c")')
lignes.append('        .replace(/[èéêë]/g, "e")')
lignes.append('        .replace(/[ìíîï]/g, "i")')
lignes.append('        .replace(/[ñ]/g, "n")')
lignes.append('        .replace(/[òóôõö]/g, "o")')
lignes.append('        .replace(/[ùúûü]/g, "u")')
lignes.append('        .replace(/[ýÿ]/g, "y");')

lignes.append("}")


# ÉCRITURE DU FICHIER
FICHIER_SORTIE.write_text(
    "\n".join(lignes),
    encoding="utf-8"
)


# INFORMATIONS
def compter_fichiers(elements):

    total = 0

    for element in elements:

        if element["type"] == "file":
            total += 1

        elif element["type"] == "dir":
            total += compter_fichiers(
                element["children"]
            )

    return total


def compter_dossiers(elements):

    total = 0

    for element in elements:

        if element["type"] == "dir":
            total += 1
            total += compter_dossiers(
                element["children"]
            )

    return total


nombre_fichiers = compter_fichiers(arbre)
nombre_dossiers = compter_dossiers(arbre)


print("=" * 60)
print("GÉNÉRATION TERMINÉE")
print("=" * 60)
print(f"Dossier analysé : {DOSSIER}")
print(f"Dossiers trouvés : {nombre_dossiers}")
print(f"Fichiers trouvés : {nombre_fichiers}")
print(f"Fichier généré : {FICHIER_SORTIE.resolve()}")
print("=" * 60)
