passwd = input('enter votre password: ')

with open('Bassirou_professional_20250914_200415.txt', "r") as file:
    data = list(map(lambda word: word.strip(), file.readlines())) 

for i in data:
    if i == passwd:
        print(f'found {i}')
        break