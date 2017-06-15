import re


with open('AC15.txt', 'r') as f:
    lista = f.readlines()
    pre_lista = lista
    lista1 = []
    lista2 = []
    lista3 = []
    with open('newAC15.txt', 'w') as nf:

        for i, l in enumerate(pre_lista):
            if i <= 13:
                lista1.append(l)
            elif 15 <= i <= 28:
                lista2.append(l)
            elif 30 <= i <= 37:
                lista3.append(l)

        lista1 = [line.lstrip('\ufeff').rstrip('\n') for line in lista1]
        lista2 = [line.lstrip('\ufeff').rstrip('\n') for line in lista2]
        lista3 = [line.lstrip('\ufeff').rstrip('\n') for line in lista3]
        new_file = open('newAC15.txt', 'w')
        for i in lista1:
            line = re.sub('@', ' ', i)
            # pat = re.findall('[a-zA-Z_.]+', line)
            nf.write(re.sub(r'\w*\d\w*', '', line).strip() + '\n')

        nf.write('\n')

        for i in lista2:
            line = re.sub('@', ' ', i)
            newl = re.split(" ", line)
            str_nuevo = ""
            for j in newl:
                if ".correcta" not in j:
                    continue
                else:
                    bb = re.sub('\.correcta', '', j)
                    str_nuevo += bb + " "
            nf.write(str_nuevo + "\n")

        nf.write('\n')

        for i in lista3:
            line = re.sub('@', ' ', i).strip()
            line = line.split(' ')
            kkk = ''
            for word in line:
                mo = re.search('\.\w*', word)
                if mo:
                    kkk += re.sub('\.', '', word) + ' '
            kkk += '\n'
            nf.write(kkk)
