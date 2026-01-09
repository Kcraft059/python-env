import PIL.Image as pimg
from helplib import helpLib # Récupère les entrées du manuel depuis helplib.py

currentImg = None

## Commandes du programme
def printHelp(args) :
  """Affiche une entrée manuel pour un mot donné"""
  helpKeyword = args[0] if len(args) > 0 else None # Si un mot est donné en argument sinon None

  if helpKeyword != None and helpKeyword in helpLib.keys(): # Cherche le mot dans la librairie
    print(f'Resultat pour l\'entrée de manuel "{helpKeyword}":')
    helpmsg = helpLib[helpKeyword]
  else :
    if helpKeyword != None:
      print(f'Pas d\'entré de manuel pour "{helpKeyword}"')
    helpmsg = helpLib["all"] # par défaut, si aucun mot n'est donné/trouvé, afficher l'aide genérale

  print(helpmsg)

def loadImg(args) :
  """Charge une image dans le programme"""
  global currentImg

  if len(args) < 1 or args[0] == "":
    raise Exception("Pas assez d'arguments (`load <img_path>`).")

  clearImg(None) # Efface l'image chargée précédemment

  imgPath = args[0]
  currentImg = pimg.open(imgPath) # Charge l'image dans le programme
  print(f'Image chargée : {imgPath}')

def showImg(args) :
  """Affiche une image"""
  global currentImg

  if currentImg == None:
    raise Exception("Pas d'image chargée.")

  print("L'image va s'ouvrir...")
  currentImg.show()

def clearImg(args) :
  """Efface l'image chargée dans le programme"""
  global currentImg;

  if currentImg == None: 
    return 

  currentImg.close()
  currentImg = None;
  print("Image effacée.")

def fileSave(args) : 
  """Enregistre l'image chargée dans le programme"""
  global currentImg

  if len(args) < 1 or args[0] == "":
    raise Exception("Pas assez d'arguments (`save <img_name>`).")
  if currentImg == None: 
    raise Exception("Aucune image chargée.")

  currentImg.save(args[0])

  print(f'Image enregistrée en tant que "{args[0]}".')

def printCredit(args) :
  """Affiche l'auteur du projet"""
  print("""=== Projet filtre NSI === 
- Camille Therey""")

def pickColor(args) :
  """Récupère la valeur d'un pixel de l'image chargée"""
  global currentImg

  argc = len(args)
  if argc < 1 or args[0] == "":
    raise Exception("Pas assez d'arguments (`pick <position>` voir `help`).")
    return
  if currentImg == None: 
    raise Exception("Aucune image chargée.")
    return

  pos = tuple(int(i) for i in args[0].split(",")[:2]) # Recupère les coordonnées dans un tuple

  (w,h) = currentImg.size

  if not(pos[0] >= 0 and pos[0] < w) or not(pos[1] >= 0 and pos[1] < h) : # Verifie si les coordonnées sont correctes
     raise Exception(f"Coordonnées invalides (0<=x<{w} 0<=x<{h})!")

  values = currentImg.getpixel(pos)[:3] # Recupère la valeur du pixel

  hexvalue = "#"
  for value in values:
    hexvalue += str(hex(value))[2:] # Récupère la deuxième partie du hex 0xFF -> FF pour chaque canal RBG

  print(f'Value of pixel {pos} is rgb: {values} or hex: {hexvalue}.')

def filterApply(args) :
  """Applique une filtre sur l'image chargée"""
  global currentImg
  argc = len(args)
  
  if argc < 1 or args[0] == "":
    raise Exception("Pas assez d'arguments (`filter <filter_name> <?options>` voir `help filters`).")

  currentFilter = args[0]

  ## Choisi le filtre et verifie si tous les arguments sont présents
  if currentFilter == "exposure" and argc == 2 :
    currentImg = imageExposure(currentImg, int(args[1]))
  elif currentFilter == "tint" and argc >= 2 :
    currentImg = imageTint(currentImg, args[1], args[2] if argc > 2 else None)
  elif currentFilter == "grayscale" :
    currentImg = imageGrayscale(currentImg)
  elif currentFilter == "black-white" :
    currentImg = imageBlackAndWhite(currentImg)
  elif currentFilter == "mirror" and argc == 2 :
    currentImg = imageMirror(currentImg,args[1])
  elif currentFilter == "reduce" and argc == 2 :
    currentImg = imageReduce(currentImg,int(args[1]))
  elif currentFilter == "pixel" and argc == 2 :
    currentImg = imagePixel(currentImg,int(args[1]))
  elif currentFilter == "swap" and argc == 2 :
    currentImg = imageSwap(currentImg,args[1])
  elif currentFilter == "replace" and argc >= 2 :
    currentImg = imageColorReplace(currentImg,args[1],int(args[2]) if argc > 2 else None)

  else :
    raise Exception(f'Filtre inconnu \"{currentFilter}\" ou avec trop peu d\'arguments.')
    return

## Filtres
def imageExposure(img,coeff) :
  """Modifie l'exposition d'une image"""
  imgCheck(img)

  def rbgcoeffadd(coords, values, newimg):
    (r,g,b) = values[:3] # transparence
    newimg.putpixel(coords, (r+coeff, g+coeff, b+coeff))

  newimg = perPixelAct(img, rbgcoeffadd)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageTint(img,color,method) :
  """Teinte une image avec une couleur"""
  imgCheck(img)

  if method == None: 
    method = "tint"

  (mr,mg,mb) = getColor(color) # Enregistre les valeurs de la teinte

  ## Choisi la methode de coloration en fonction de la methode donnée en argument
  if method == "monotone" :
    def colortint(coords, values, newimg):
      (r,g,b) = values[:3]
      avrg = (r+g+b) // 3
      newimg.putpixel(coords, ((avrg*mr)//255,(avrg*mg)//255,(avrg*mb)//255))

  elif method == "tint" :
    def colortint(coords, values, newimg):
      (r,g,b) = values[:3]
      newimg.putpixel(coords, ((r*mr)//255,(g*mg)//255,(b*mb)//255))

  else :
    raise Exception(f'Aucune methode "{method}" trouvée. (`help filter_tint`)')
    return img

  newimg = perPixelAct(img,colortint) # Applique la fonction de modification sur chaque pixel de l'image
  print(f'Filtre appliqué avec la methode {method}.')
  
  img.close()
  return newimg

def imageGrayscale(img) :
  imgCheck(img)
  return imageTint(img,"#ffffff","monotone")

def imageBlackAndWhite(img) :
  imgCheck(img)

  def blackWhite(coords, values, newimg):
      (r,g,b) = values[:3]
      avrg = (r+g+b) // 3
      newimg.putpixel(coords, (255,255,255) if avrg > 127 else (0,0,0))

  newimg = perPixelAct(img,blackWhite)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageMirror(img,axis) :
  imgCheck(img)

  (w,h) = img.size
  if axis == "x" :
    def mirror(coords, values, newimg):
      coords = (w - 1 - coords[0],coords[1])
      newimg.putpixel(coords , values)

  elif axis == "y" :
    def mirror(coords, values, newimg):
      coords = (coords[0],h - 1 - coords[1])
      newimg.putpixel(coords , values)

  else :
    raise Exception(f'Axe inconnu "{axis}".')

  newimg = perPixelAct(img,mirror)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageReduce(img,valueRange) :
  imgCheck(img)

  def rdc(coords, values, newimg):
      values = tuple((i*valueRange//255)*(255//valueRange) for i in values[:3])
      newimg.putpixel(coords , values)
  
  newimg = perPixelAct(img,rdc)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imagePixel(img,pixels) :
  imgCheck(img)

  (w,h) = img.size
  newimg = pimg.new("RGB",tuple(i//pixels for i in img.size))

  for x in range(newimg.width):
    for y in range(newimg.height): 
      adjpos = []
      for ix in range(pixels):
        for iy in range(pixels):
          adjpos.append((x*pixels + ix,y*pixels + iy))

      avrg = [0,0,0]
      for pos in adjpos:
        (r,g,b) = img.getpixel(pos)[:3]
        avrg = [avrg[0] + r, avrg[1] + g, avrg[2] + b]

      avrg = tuple(i//(pixels**2) for i in avrg)

      newimg.putpixel((x,y), avrg)

  print('Filtre appliqué.')
  
  img.close()
  return newimg

def imageSwap(img,primaryValues) :
  imgCheck(img)

  primaryValues = tuple(0 if i == "r" else 1 if i == "g" else 2 for i in primaryValues.split("/")[:2])

  def swap(coords,values,newimg):
    nvalues = list(values[:3])
    nvalues[primaryValues[0]] = values[primaryValues[1]]
    nvalues[primaryValues[1]] = values[primaryValues[0]]
    newimg.putpixel(coords,tuple(nvalues))

  newimg = perPixelAct(img,swap)
  print('Filtre appliqué.')
  
  img.close()
  return newimg

def imageColorReplace(img,colors,proximity) :
  imgCheck(img)

  if proximity == None:
    proximity = 0

  proximity = proximity*255/100

  (replacedColor, newColor) = tuple(getColor(i) for i in colors.split("/")[:2])

  def replace(coords,values,newimg):
    colorscore = tuple(abs(v - replacedColor[i]) for i,v in enumerate(values[:3]))
    if all(i <= proximity for i in colorscore):
      values = newColor
    newimg.putpixel(coords,values)

  newimg = perPixelAct(img,replace)
  print('Filtre appliqué.')
  
  img.close()
  return newimg

## Helpers 
def imgCheck(img):
  if img == None:
    raise Exception("Aucune image chargée.")

def perPixelAct(img,pixelFunction):
  (w,h) = img.size
  newimg = pimg.new("RGB",(w,h))

  for x in range(w):
    for y in range(h):
      pixelFunction((x,y),img.getpixel((x,y)),newimg)
  
  return newimg

def getColor(color) :
  if color[0] == "#" and len(color) == 7:
    return tuple(int(i,16) for i in (color[1:3],color[3:5],color[5:7]));
  elif len(color.split(",")) == 3:
    return tuple(int(i) for i in color.split(",")[:3])
  else:
    raise Exception(f'Invalid color format: "{color}" (should be 255,255,255 or #ffffff)')

## Liste de commandes -> reference vers fonction
commandList = { "help" : printHelp, 
                "load" : loadImg, 
                "filter" : filterApply,
                "pick" : pickColor,
                "show" : showImg, 
                "clear" : clearImg, 
                "save" : fileSave,
                "credit" : printCredit}

## REPL (Read eval print loop) -> pour afficher la console du programme
print("[Tip] Tappez `help` pour voir la liste des commandes disponibles disponibles.")

while True:
  cmdline = input("> ");
  cmdargs = cmdline.split(" ")
  cmdkeyword = cmdargs[0]

  if cmdkeyword in commandList :
    try: 
      commandList[cmdkeyword](cmdargs[1:])
    except Exception as error:
      print(f'[Err] {cmdkeyword}: {error}')
      
  elif cmdkeyword == "exit":
    commandList["clear"](None)
    print("Aurevoir !")
    break;
  else :
    print(f'Commande inconnue "{cmdkeyword}"')