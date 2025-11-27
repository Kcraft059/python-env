# Cahier des charges

## Principe du jeu

Le joueur lance 3 dès (aléatoires).
Si un des dès est valide (4,2 ou 1), il reste vert a l'écran et est validé.
Au bout de 3 dés valides (soit 421), le joueur à gagné.
Si le joueur dépasse 3 tours, il a perdu

## Fonctionnement

Pour chaque tour, le jeu dessine d'abord la bordure du dès, puis génère une valeur aléatoire correspondante.
Le jeu verifie si la valeur du dès est une valeur valide, dans ce cas, il verrouille le dès en enregistrant son index.

Si le dès à l'index est dejà validé, sa valeur est mise a 4,2 ou 1 en fonction de la valeur validée, et les points sont dessinés en vert.
Sinon, les points sont rouge.

Pour dessiner les points, le programme utilise 3 fonctionnalités:
 - Une pour dessiner le points du milieu
 - Une pour dessiner un nombre de points en diagonal
 - Une pour dessiner des rangées de points sur les cotés

Chaque dessin de point utilise une position relative à des coordonées actuelles définies sur l'index du dès defini.

Si tous les dès sont valides alors, le jeu est terminé.