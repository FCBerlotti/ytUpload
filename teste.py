listMine = [("sf2", "11", "01/08/2026")]

print(listMine)


for (i, a, d) in listMine:
    print(i, a, d)
    teste = True
    listMine.remove(("sf2", "11", "01/08/2026"))

print(listMine)
#listMine.remove(("sf2", "11", "01/08/2026"))
#print(listMine)