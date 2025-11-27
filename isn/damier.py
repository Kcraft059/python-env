import turtle as trtl
trtl.speed("fastest")
trtl.ht()

def drawShape(x,y,size,color,shape) :
  trtl.seth(0)
  trtl.teleport(x,y - (size if shape == "circle" else 0))
  trtl.begin_fill()
  trtl.fillcolor(color)
  if (shape == "square") :
    for i in range(0,4) :
      trtl.forward(size)
      trtl.left(90)
  if (shape == "circle"):
    trtl.circle(size)
  trtl.end_fill()


size = 8
length = 50
peonRow = 3
peonSize = length / 3
offset = [0 - (length*size)/2, 0 - (length*size)/2]

for x in range(0,size):
  for y in range(0,size):
    drawShape(length * x + offset[0],length * y + offset[1],length,
              "BlanchedAlmond" if ((x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1)) else "DarkGoldenrod", "square");

for side in range(0,2):
  for y in range(0,peonRow):
    for x in range(0,size):
      py = y + side * (size - peonRow)
      if (not((x % 2 == 1 and py % 2 == 0) or (x % 2 == 0 and py % 2 == 1))):
        drawShape(length * x + length /2 + offset[0], 
                  length * py + length /2 + offset[1], peonSize,
                  "aliceBlue" if (side > 0) else "red", "circle");

      

trtl.done()