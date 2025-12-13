import PIL.Image as pimg
from helplib import helpLib 

currentImg = None

## Commandes du programme
def printHelp(args) :
  helpKeyword = args[0] if len(args) > 0 else None

  if helpKeyword != None and helpKeyword in helpLib.keys():
    print(f'Resultats pour l\'entrée de manuel "{helpKeyword}":')
    helpmsg = helpLib[helpKeyword]
  else :
    if helpKeyword != None and not(helpKeyword in helpLib.keys()):
      print(f'Pas d\'entré de manuel pour "{helpKeyword}"')
    helpmsg = helpLib["all"]

  print(helpmsg)

def loadImg(args) :
  global currentImg

  if len(args) < 1 or args[0] == "":
    print("Pas assez d'arguments (`load <img_path>`).")
    return

  clearImg(None)

  imgPath = args[0]
  currentImg = pimg.open(imgPath)
  print(f'Image chargée : {imgPath}')

def showImg(args) :
  global currentImg

  if currentImg == None:
    print("Pas d'image chargée.")
    return

  print("L'image va s'ouvrir...")
  currentImg.show()

def clearImg(args) :
  global currentImg;
  if currentImg == None: 
    print("Pas d'image a effacer.")
    return
  currentImg.close()
  currentImg = None;
  print("Image effacée.")

def fileSave(args) : 
  global currentImg
  if len(args) < 1 or args[0] == "":
    print("Pas assez d'arguments (`save <img_name>`).")
    return
  if currentImg == None: 
    print("Aucune image chargée.")
    return
  currentImg.save(args[0])
  print(f'Image enregistrée en tant que "{args[0]}".')

def printCredit(args) :
  print("""=== Projet filtre NSI === 
- Camille Therey""")

def pickColor(args) :
  global currentImg
  argc = len(args)
  if argc < 1 or args[0] == "":
    print("Pas assez d'arguments (`pick <position>` voir `help`).")
    return
  if currentImg == None: 
    print("Aucune image chargée.")
    return

  pos = tuple(int(i) for i in args[0].split(",")[:2])
  values = currentImg.getpixel(pos)[:3]

  hexvalue = "#"
  for value in values:
    hexvalue += str(hex(value))[2:]

  print(f'Value of pixel {pos} is {values} or {hexvalue}.')

def filterApply(args) :
  global currentImg
  argc = len(args)
  if argc < 1 or args[0] == "":
    print("Pas assez d'arguments (`filter <filter_name> <?options>` voir `help filters`).")
    return

  currentFilter = args[0]

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
    print(f'Filtre inconnu \"{currentFilter}\" ou avec trop peu d\'arguments.')
    return

## Filtres
def imageExposure(img,coeff) :
  if img == None: 
    print("Aucune image chargée.")
    return img

  def rbgcoeffadd(coords, values, newimg):
    (r,g,b) = values[:3] # transparence
    newimg.putpixel(coords, (r+coeff, g+coeff, b+coeff))

  newimg = perPixelAct(img, rbgcoeffadd)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageTint(img,color,method) :
  if img == None: 
    print("Aucune image chargée.")
    return img

  (mr,mg,mb) = getColor(color)

  if method == "monotone" :
    def colortint(coords, values, newimg):
      (r,g,b) = values[:3]
      avrg = (r+g+b) // 3
      newimg.putpixel(coords, ((avrg*mr)//255,(avrg*mg)//255,(avrg*mb)//255))
  elif method == "tint" or method == None :
    def colortint(coords, values, newimg):
      (r,g,b) = values[:3]
      newimg.putpixel(coords, ((r*mr)//255,(g*mg)//255,(b*mb)//255))
  else :
    print(f'Aucune methode "{method}" trouvée. (`help filter_tint`)')
    return img

  newimg = perPixelAct(img,colortint)
  print(f'Filtre appliqué avec la methode {method}.')
  
  img.close()
  return newimg

def imageGrayscale(img) :
  if img == None: 
    print("Aucune image chargée.")
    return img
  return imageTint(img,"#ffffff","monotone")

def imageBlackAndWhite(img) :
  if img == None: 
    print("Aucune image chargée.")
    return img

  def blackWhite(coords, values, newimg):
      (r,g,b) = values[:3]
      avrg = (r+g+b) // 3
      newimg.putpixel(coords, (255,255,255) if avrg > 127 else (0,0,0))

  newimg = perPixelAct(img,blackWhite)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageMirror(img,axis) :
  if img == None: 
    print("Aucune image chargée.")
    return img

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
    print(f'Axe inconnu "{axis}".')
    return img

  newimg = perPixelAct(img,mirror)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imageReduce(img,valueRange) :
  if img == None: 
    print("Aucune image chargée.")
    return img

  def rdc(coords, values, newimg):
      values = tuple((i*valueRange//255)*(255//valueRange) for i in values[:3])
      newimg.putpixel(coords , values)
  
  newimg = perPixelAct(img,rdc)
  print(f'Filtre appliqué.')
  
  img.close()
  return newimg

def imagePixel(img,pixels) :
  if img == None: 
    print("Aucune image chargée.")
    return img

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
  if img == None: 
    print("Aucune image chargée.")
    return img

  primaryValues = tuple(0 if i == "r" else 1 if i == "g" else 2 for i in primaryValues.split("/")[:2])

  def swap(coords,values,newimg):
    nvalues = list(i for i in values[:3])
    nvalues[primaryValues[0]] = values[primaryValues[1]]
    nvalues[primaryValues[1]] = values[primaryValues[0]]
    newimg.putpixel(coords,tuple(i for i in nvalues))

  newimg = perPixelAct(img,swap)
  print('Filtre appliqué.')
  
  img.close()
  return newimg

def imageColorReplace(img,colors,proximity) :
  if img == None: 
    print("Aucune image chargée.")
    return img
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
def perPixelAct(img,pixelFunction):
  (w,h) = img.size
  newimg = pimg.new("RGB",(w,h))

  for x in range(w):
    for y in range(h):
      pixelFunction((x,y),img.getpixel((x,y)),newimg)
  
  return newimg

def getColor(color) :
  if color[0] == "#" :
    rgb = tuple(int(i,16) for i in (color[1:3],color[3:5],color[5:7]));
  else :
    rgb = tuple(int(i) for i in color.split(",")[:3])
  return rgb

## Liste de commandes
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
    commandList[cmdkeyword](cmdargs[1:])
  elif cmdkeyword == "exit":
    commandList["clear"](None)
    print("Aurevoir !")
    break;
  else :
    print(f'Commande inconnue "{cmdkeyword}"')