#Ecrire un programme qui demande trois longueurs à l'utilisateur
#, indique si ces trois longueurs peuvent être les longueurs des trois
#côtés d'un triangle et, le cas échéant, s'il s'agit d'un triangle équilatéral,
#, isocèle, rectangle ou scalène (trois côtés de longueurs différentes)

# Get the maximum value and index from list
def max_of(vlist) :
    maxv = vlist[0]
    index = 0
    for i,v in enumerate(vlist) :
        if v > maxv :
            maxv = v
            index = i
    return {'max' : int(maxv), 'index' : index }

# Return how often each item appears
def find_occurences(vlist) :
    matches = dict()
    for i in vlist :
        if not(i in matches.keys()):
            matches[i] = 1
        else:
            matches[i] = matches[i] + 1
    return matches

lengths = input('Lengths comma separated (3 values): ').split(',')

if len(lengths) != 3 :
    raise Exception('Too much values')

tmp = max_of(lengths)
max_value = tmp['max']
max_index = tmp['index']
same_vals=find_occurences(lengths).values()

lengths.pop(max_index)

a_value = int(lengths[0])
b_value = int(lengths[1])

if max_value > a_value + b_value :
    raise Exception('Not a triangle')

if 3 in same_vals :
    print('Equilateral')
elif 2 in same_vals :
    print('Isosceles')
elif max_value**2 == a_value**2 + b_value**2 :
    print('Rectangle')
else :
    print('Ordinary')

    