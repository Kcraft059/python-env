import random as r

def numberGuess(min,max,maxTries) :
    if min > max : # Notice if wronf max min format
        raise Exception('Vous n\'avez pas respecté min < max !')
    
    nbr = r.randint(min,max)
    tries = 0
    win = None

    while win == None : # Try until there's a win or a loss
        try :
            if tries >= maxTries :
                win = False
    
            else :
                guess = int(input(f'Devinez un nombre entre {min} et {max}:'))
            
                if guess > max or guess < min : # Notice out of bounds
                    raise Exception(f'Vous avez entré un nombre hors limites {min} > guess > {max} !')
            
                diff = abs(nbr - guess)
                tries = tries+1
        
                if guess == nbr:
                    win = True
                elif diff < 5 :
                    print('Bouillant')
                elif diff < 10 :
                    print('Chaud')
                elif diff < 15 :
                    print('Tiède')
                else :
                    print('Froid')
                    
        except Exception as e:
            print(e,'\nCela ne comptera pas comme un essai.')
    
    returnDict = {'tries' : tries, 'win' : win, 'number' : nbr}
    
    return returnDict

maxTries = 10
result = numberGuess(-50,100,maxTries)
tries = result['tries']; number = result['number']

if result['win'] :
    print(f'Vous avez gagné en {tries} essais et vous avez deviné {number}')
elif not result['win'] and tries >= maxTries :
    print(f'Vous avez perdu en {tries} essais (vous avez dépassé le nombre d\'éssais max) et vous n\'avez deviné {number}')
else :
    print(f'Vous avez perdu en {tries} essais et vous n\'avez deviné {number}')