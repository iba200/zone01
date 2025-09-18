prenom = "Ibrahima"
age = 13
taille = 1.90

def calculatrice(a, b, o):
    if isinstance(a, (int, float)) and isinstance(b, (int,float)):
        if o == "+":
            return f"Resultat de {a} + {b} = {a+b}."
        elif o == "-":
            return f"Resultat de {a} - {b} = {a-b}."
        elif o == "x":
            return f"Resultat de {a} x {b} = {a*b}."
        elif o == "/":
            if b == 0:
                return "Impossible division par zero!"
            else:
                return f"Resultat de {a} ÷ {b} = {a/b}."
        elif o == "%":
            return f"Resultat de {a} % {b} = {a%b}."
        elif o == "=":
            if a == b:
                return f"Resultat de {a} = {b} est vrai."
            else:
                return f"Resultat de {a} = {b} est fausse."
        else:
            return "Operation non connu."
    else:
        return 'L\'entrer n\'est pas un nombre.' 

a = input("Entre le premier nombre (a): ")
b = input("Entre le deuxieme nombre (b): ")

print(calculatrice(int(a), int(b)))