# cesar cryptographie
alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]
numbers = [i for i in range(1, 27)]
dico = dict(zip(alphabet, numbers))
dico[' '] = 27
def cesar_fermer(mot):
    mot = [lettre for lettre in mot] 
    # mot_crypter = [ str(dico[l]) for l in mot]
    return '_'.join([ str(dico[l]) for l in [lettre for lettre in mot]])

def get_keys_by_value(dictionary, value_to_find):
    return [key for key, val in dictionary.items() if val == value_to_find][0]


def cesar_ouvrer(char):
    nombres_str = char.split('_')
    nombres = list(map(lambda x: int(x), nombres_str))
    mot_decrypter = []
    for chiffre in nombres:
        mot_decrypter.append(get_keys_by_value(dico, chiffre))
    return mot_decrypter



alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]  
alphabet_decaler = alphabet[3:] + alphabet[:3]


dico = dict(zip(alphabet, alphabet_decaler))
char_particuliere = [' ', '\'', '.', ',', '!', '?', ';', ':', '-', '_', '(', ')', '[', ']', '{', '}', '\n', '\t']
for char in char_particuliere:
    dico[char] = char


def cesar_fermer_v2(mot):
    mot = [lettre for lettre in mot] 
    return ''.join([ dico[l] for l in mot])

print(cesar_fermer_v2('ibrahima thiongane va a l\'ecole se matin '))


def cesar_ouvrer_v2(mot):
    dico_inverse = {v: k for k, v in dico.items()}
    mot = [lettre for lettre in mot] 
    return ''.join([ dico_inverse[l] for l in mot])

print(cesar_ouvrer_v2('leudklpd wklrqjdqh yd d o\'hfroh vh pdwlq'))


