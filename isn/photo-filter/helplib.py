helpLib = { 
"all" : """=== Manuel ===
Pour commencer la modification d'une image, vous devrez tout d'abord la charger dans votre espace de travail en utilisant `load`.
Vous pourrez ensuite utiliser les commandes de manipulation d'image pour agir sur cette image, et ensuite la sauvegarder avec `save`.
Ainsi, vous pouvez appliquer plusieurs filtres à la suite.

Liste des commandes :
  help <?entry> : Affiche ce menu
  load <img> : Charge une image
  show : Affiche l'image actuelle
  pick <pos> : Recupère la valeur RGB du pixel a la <pos> x,y
  filter <filter_name> <?options>: Applique un filtre sur l'image actuelle (pour voir la liste des filtres `help filter`)
  save <img_name> : Sauvegarde l'image actuelle sous le nom <img_name>
  clear : Efface l'image actuelle
  exit : Sort du programme
  credit

Exemples de syntaxe :
  `load ./mon-image.jpg` : Charge l'image "./mon-image.jpg"
  `filter exposure 100` : Applique le filtre "exposure" sur l'image actuelle avec 100 d'intensité
  `save ./ma-nouvelle-image.jpg`: enregistre l'image actuelle sous le nom ./ma-nouvelle-image.jpg""", 

"filter" : """=== Commande filter ===
Permet d'appliquer un filtre <filter_name> sur l'image chargée

  filter <filter_name> <?options>

Exemple : 
  `filter mirror x` : Applique le filtre mirror avec l'option x sur l'image actuelle

Liste des filtres :
  exposure <intensity> : Applique un filtre qui modifie l'exposition de l'image
  tint <color> <?method> : Colore l'image en une nuance d'une seule couleur
  grayscale : Convertis l'image en echelle de gris
  black-white : Convertis l'image en noir et blanc 
  mirror <axis> : Effectue un effet mirroir sur l'image selon un axe <axis>
  reduce <range> : Reduit le nombre de couleurs pour les canaux couleur a la valeur specifiée
  pixel <number> : Effectue une mise a l'échelle selon le ratio 1:<number> pixels
  swap <channelA/channelB> : Echange les valeurs de 2 canaux de couleur (voir `help filter_swap` pour les exemples). 
  replace <target/replacement> <?proximity> : Remplace une couleur <target> par une couleur <replacement> avec un tolerance de <proximity>%

(Il est vivement recommandé pour avoir une documentation plus précise par rapport à l'un des filtres de consulter la page du manuel associée a ce filtre `help filter_<filter_name>`)""",

"filter_exposure" : """=== Filtre d'exposition ===
Permet de modifer l'exposition d'une image avec une intensité donnée.
<intensity> : Intensité de l'effet (int)

  exposure <intensity>

Exemple :
  `filter exposure 100` : Ajoute 100 de luminosité à l'image
  `filter exposure -50` : Enelève 50 de luminosité à l'image""",

"filter_tint" : """=== Filtre de tinte ===
Permet de tinter une image avec une autre couleur.
<color> : couleur sous la forme hex (#ffffff) ou rgb (255,255,255)
<method> : methode utilisée (tint/monotone) 

  tint <color> <?method>

Exemple :
  `filter tint #0080ff` : Tinte l'image en bleu
  `filter tint #0080ff tint` : meme chose (tint est la methode par defaut)
  `filter tint 128,128,0 monotone` : Tinte l'image en une seule couleur #808000 (jaune pale)""",

"grayscale" : """=== Filtre d'échelle de gris ===
Permet de tinter une image en échelle de gris

  grayscale

Exemple :
  `filter grayscale` : Voir ci-dessus
""", 

"filter_black-white" : """=== Filtre noir et blanc ===
Permet de coloriser une image uniquement avec du noir et du blanc

  black-white

Exemple :
  `filter black-white` : Voir ci-dessus
""",

"filter_mirror" : """=== Filtre mirroir ===
Permet de faire un effet mirroir sur l'image en fonction d'un axe donné.
<axis> : axe d'application de l'effet (x/y)

  mirror <axis> 

Exemple :
  `filter mirror x` : Effectue un effet mirroir vertical sur l'image
""",

"filter_reduce" : """=== Filtre de reduction de couleurs ===
Permet de reduire le nombre de valeur possibles des canaux RGB.
<range> : Le nombre de valeurs différentes possibles dans chaque canal RGB

  reduce <range>

Exemple :
  `filter reduce 8` : Reduit le nombre de couleurs de l'image à 8*8*8 = 512 couleurs.
""",

"filter_pixels" : """=== Filtre de pixelisation ===
Permet de reduire le nombre de pixel d'une image à une échelle de <number> de pixel originaux equivalent à 1 pixel sur la nouvelle image.
<number> : Le nombre de pixel d'échelle (int > 0)

  pixel <number>

Exemple :
  `filter pixel 4` : Met l'image a l'échelle 1:4 (4 fois plus petite)
""",

"filter_swap" : """=== Filtre d'inversion de canaux ===
Permet l'inversion des valeurs des canaux RGB de l'image
<channelA/channelB> : Canaux RGB à échanger (sous la forme <channelA>/<channelB> - r,g,b)

  swap <channelA/channelB>

Exemple :
  `filter swap b/r` : Inverse les canaux Rouges et Bleu de l'image
""",

"filter_replace" : """=== Filtre de remplacement de couleurs ===
Permet de remplacer une couleur cible et les couleurs similaires par une couleur de remplacement 
<target/replacement> : Couleur sous la forme hex (#ffffff) ou rgb (255,255,255)
<proximity> : Seuil de ressemblance toléré pour que la couleur soit remplacée (en %), 0 par défaut

  replace <target/replacement> <?proximity>

Exemple :
  `filter replace #ff0000/#0000ff` : Remplace le rouge avec du bleu
  `filter replace 255,255,0/#0000ff 50` : Remplace le jaune et les couleurs proches a plus de 50% du jaune par du bleu
"""}