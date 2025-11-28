##
# 421 Dice project
# Camille THEREY
##

import turtle as trtl # Import turtle graphics
from random import randint
 
def dice_square(x_start,y_start, size):
  """Draw a square starting at x,y"""
  trtl.teleport(x_start,y_start) # Go to box drawing start

  trtl.down(); trtl.seth(0) # Reset angle
  for i in range(0,4) : # Draw dice box
    trtl.forward(size)
    trtl.left(90)

  trtl.up();

def dice_circle(x_start,y_start,size,color):
  """Draw circle with center at x,y"""
  trtl.teleport(x_start,y_start - size) # Place pointer at the center of box
  trtl.fillcolor(color); trtl.begin_fill(); 
  trtl.circle(dicePointSize)
  trtl.end_fill()

def dice_face(x_start,y_start,color,diceValue,diceSize,dicePointSize,edge):
  """Draw a given number of point"""
  if (diceValue == 1 or diceValue == 5) : # Draw dice middle point
    dice_circle(currentX + diceSize / 2 ,
                currentY + diceSize / 2 , dicePointSize, color) # Place pointer at the center of box

  if (diceValue == 2 or diceValue == 3): # Draw a diagonal of point
    for pointIter in range(0,diceValue):
      dice_circle(currentX + edge + (diceSize - edge * 2) / (diceValue - 1) * pointIter ,
                  currentY + edge + (diceSize - edge * 2) / (diceValue - 1) * pointIter, 
                  dicePointSize, color) # Place pointer diagonally relative to the point we're drawing

  if (diceValue == 4 or diceValue == 5 or diceValue == 6): # Draw two row of points
    pointsPerRow = diceValue // 2
    for rowIter in range(0,2): # Draw the two rows of points
      for pointIter in range(0,pointsPerRow): 
        dice_circle(currentX + edge + (diceSize - edge * 2) * rowIter,
                    currentY + edge + (diceSize - edge * 2) / (pointsPerRow - 1) * pointIter, 
                    dicePointSize, color) # Draw a colum of points starting at bottom left

def store_validity(validVals, currentVal, currentIndex):
  """Stores an index in a dict if it's a valid value and that's it's not already stored""" 
  for key in validVals:
    if validVals[key] == None and key == str(currentVal):
      validVals[key] = currentIndex

def check_validity(validVals, currentIndex):
  """Check value for index if already store"""
  for key in validVals:
    if validVals[key] == currentIndex :
      return int(key)
  return None

def check_all(validVals):
  """Check if all keys are set"""
  for key in validVals:
    if validVals[key] == None:
      return False
  return True

## Defaults
maxPlay = 3
diceCount = 3
diceSize = 120 # Arbitrary dice render values (which actually look good)
diceSpace = 80
dicePointSize = diceSize / 10
edge = diceSize / 5
startingPointX = -(((diceSize+diceSpace) * diceCount) - diceSpace) / 2 # Center the dices on the middle of X axis
startingPointY = -diceSize / 2                                         # Center dices on the middle of Y axis

## Turtle graphics config
trtl.speed("fastest"); trtl.ht(); trtl.up() 

## Start main loop 
win = False
tries = 0
validPos = {"1": None, "2": None, "4": None};

for playIter in range(0,maxPlay) : # Allow maxPlay number of tries
  input(f'Tour {playIter+1}/{maxPlay}, appuyez sur "entrer" pour {"re" if playIter != 0 else ""}lancer les dés !') # Wait before new try

  trtl.clear() # Clear board

  for diceIter in range(0,diceCount) : # Roll each dice
    currentX = startingPointX + (diceSize + diceSpace) * diceIter # Depending on the dice we are drawing, go to the right offset
    currentY = startingPointY
    diceValue = randint(1,6) # Get a value for the dice between 1 and 6

    ## Check if given value is correct
    newVal = check_validity(validPos, diceIter)
    if newVal != None:
      diceValue = newVal
    else:
      store_validity(validPos, diceValue, diceIter) # Store

    ## Dice drawing section
    dice_square(currentX,currentY,diceSize)
    dice_face(currentX,currentY,
              'green' if (check_validity(validPos, diceIter) != None) else 'red',
              diceValue,diceSize,dicePointSize,edge)
 
  if check_all(validPos): # If all values have been found, win and stop game
    win = True
    tries = playIter + 1
    break 

print(f'Vous avez gagné en {tries} essais !' if win else f'Vous avez perdu car vous avez dépassé le nombre maximal d\'essais ({maxPlay})')
input('Appuyez sur "entrer" pour quitter.')