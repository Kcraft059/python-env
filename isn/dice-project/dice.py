##
# 421 Dice project
# Camille THEREY
##

import turtle as trtl # Import turtle graphics
from random import randint
 
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
validDice1 = validDice2 = validDice4 = -1 # Store when a dice is valid (an array would be a better fit)

for playIter in range(0,maxPlay) : # Allow maxPlay number of tries
  input(f'Tour {playIter+1}/{maxPlay}, appuyez sur "entrer" pour {"re" if playIter != 0 else ""}lancer les dés !') # Wait before new try (turtle has a builtin keypress listener tho it uses functions)

  trtl.clear() # Clear board

  for diceIter in range(0,diceCount) : # Roll each dice
    currentX = startingPointX + (diceSize + diceSpace) * diceIter # Depending on the dice we are drawing, go to the right offset
    currentY = startingPointY

    diceValue = randint(1,6) # Get a value for the dice between 1 and 6

    ## Check for dice validity
    if validDice1 == diceIter: diceValue = 1 # If dice was previously a winning dice make its value static
    if validDice2 == diceIter: diceValue = 2
    if validDice4 == diceIter: diceValue = 4

    if (diceValue == 1 and validDice1 == -1): validDice1 = diceIter # If winning dice for value 1 or 2 or 4 hasn't been found yet, and that the diceValue is one of those, store dice index for corresponding value
    if (diceValue == 2 and validDice2 == -1): validDice2 = diceIter
    if (diceValue == 4 and validDice4 == -1): validDice4 = diceIter

    ## Dice drawing section
    # Configure pen color depending on dice is a valid dice
    trtl.fillcolor('green' if (validDice1 == diceIter or validDice2 == diceIter or validDice4 == diceIter) else 'red')
  
    trtl.teleport(currentX,currentY) # Go to box drawing start
    trtl.down(); trtl.seth(0) # Reset angle
    
    for i in range(0,4) : # Draw dice box
      trtl.forward(diceSize)
      trtl.left(90)

    trtl.up(); trtl.begin_fill(); 

    if (diceValue == 1 or diceValue == 5) : # Draw dice middle point
      trtl.teleport(currentX + diceSize / 2 ,
                    currentY + diceSize / 2 - dicePointSize) # Place pointer at the center of box
      trtl.circle(dicePointSize)

    if (diceValue == 2 or diceValue == 3): # Draw a diagonal of point
      for pointIter in range(0,diceValue):
        trtl.teleport(currentX + edge + (diceSize - edge * 2) / (diceValue - 1) * pointIter ,
                      currentY + edge + (diceSize - edge * 2) / (diceValue - 1) * pointIter - dicePointSize) # Place pointer diagonally relative to the point we're drawing
        trtl.circle(dicePointSize)

    if (diceValue == 4 or diceValue == 5 or diceValue == 6): # Draw two row of points
      pointsPerRow = diceValue // 2
      for rowIter in range(0,2): # Draw the two rows of points
        for pointIter in range(0,pointsPerRow): 
          trtl.teleport(currentX + edge + (diceSize - edge * 2) * rowIter,
                        currentY + edge + (diceSize - edge * 2) / (pointsPerRow - 1) * pointIter - dicePointSize) # Draw a colum of points starting at bottom left
          trtl.circle(dicePointSize)
    
    trtl.end_fill()

  if (validDice1 != -1 and validDice2 != -1 and validDice4 != -1): # If all values have been found, win and stop game
    win = True
    tries = playIter + 1
    break 

if win : 
  print(f'Vous avez gagné en {tries} essais !')
else :
  print(f'Vous avez perdu car vous avez dépassé le nombre maximal d\'essais ({maxPlay})')

input('Appuyez sur "entrer" pour quitter.')