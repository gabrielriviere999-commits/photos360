from pathlib import Path
from urllib.parse import quote

# CONFIGURATION
DOSSIER = Path(r".")
FICHIER_SORTIE = Path("photos360.js")


# GÉNÉRATION
if not DOSSIER.exists():
    print(f"ERREUR : le dossier n'existe pas : {DOSSIER}")
    input("Appuie sur Entrée pour fermer...")
    exit()

if not DOSSIER.is_dir():
    print(f"ERREUR : le chemin indiqué n'est pas un dossier : {DOSSIER}")
    input("Appuie sur Entrée pour fermer...")
    exit()


# Récupération des fichiers uniquement
fichiers = sorted(
    [
        f for f in DOSSIER.iterdir()
        if f.is_file()
        and f.suffix.lower() != ".py"
        and f.name != "photos360.js"
    ],
    key=lambda f: f.name.lower()
)


# DÉBUT DU JAVASCRIPT
lignes = []

lignes.append("window.popupPhotos360HTML =")
lignes.append(
    "    '<b class=\"titleb\">Photos 360°</b><hr class=\"titlehr\">' +"
)

# Filtre
lignes.append(
    "    '<input type=\"text\" id=\"filterPhotos360\" "
    "style=\"width:100%;box-sizing:border-box;\" "
    "placeholder=\"Filtrer...\" "
    "onkeyup=\"var f=sansAccents(this.value.toLowerCase());"
    "var li=document.getElementById(\\'photos360List\\').getElementsByTagName(\\'li\\');"
    "for(var i=0;i<li.length;i++){"
    "var a=li[i].getElementsByClassName(\\'photo360Nom\\')[0];"
    "li[i].style.display="
    "sansAccents(a.textContent.toLowerCase()).indexOf(f)>=0?\\'\\':\\'none\\';"
    "}\">' +"
)

lignes.append("    '<div id=\"photos360List\">' +")
lignes.append("    '<ul>' +")


# AJOUT DES FICHIERS
for fichier in fichiers:

    nom = fichier.name

    # Encodage URL
    nom_url = quote(nom, safe="")

    lignes.append(
        f"    '<li>"
        f"<a class=\"photo360Nom\" href=\"?file=../photos360/{nom_url}\">{nom}</a>"
        f"<a href=\"../photos360/{nom_url}\" download> [↓]</a>"
        f"</li>' +"
    )


# FIN DU JAVASCRIPT
lignes.append("    '</ul>' +")
lignes.append("    '</div>';")

lignes.append("")


# FONCTION SANS ACCENTS
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
print("=" * 60)
print("GÉNÉRATION TERMINÉE")
print("=" * 60)
print(f"Dossier analysé : {DOSSIER}")
print(f"Nombre de fichiers trouvés : {len(fichiers)}")
print(f"Fichier généré : {FICHIER_SORTIE.resolve()}")
print("=" * 60)

for fichier in fichiers:
    print(f"  - {fichier.name}")
