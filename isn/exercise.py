def square(val):
  """Raise a number to it's square"""
  return val**2

def perimeter(w,l):
  """Calculates the perimeter of a rectangle"""
  return (w+l)*2

def averageMark(a,b,c):
  """Calculates the average of 2 marks"""
  return round((a+b+c)/3,1)

def calc(a,b,operand):
  """Calculates result of a calculation"""
  if operand == '+':
    return a + b
  elif operand == '-':
    return a - b
  elif operand == '/':
    return a / b
  elif operand == '*':
    return a * b

def myLen(chain):
  """Return len of chain"""
  return len(chain)

  """ # Ou alors :
  length = 0
  for i in chain :
    length += 1
  return length
  """

def spaceCount(chain):
  """Return spaces count in string"""
  spaces = 0
  for i in chain:
    if i == ' ':
      spaces += 1
  return spaces

def voyelleCount(chain):
  """Return voyelle count in string"""
  voyelles = 0
  for i in chain:
    if (i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u' or i == 'y') :
      voyelles += 1
  return voyelles

def consonneCount(chain):
  """Return voyelle count in string"""
  consonne = 0
  for i in chain:
    if not(i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u' or i == 'y') :
      consonne += 1
  return consonne

def isEven(num):
  return True if num % 2 == 0 else False

def bmiCalc(mass,heigth):
  return round(mass / heigth**2,1)

""" QCM
1)
D. ((randint(0,4)-2)*2)
2)
D. (2019,2019)
3)
A. -2
4)
B. Un entier
5)
D. 3
"""