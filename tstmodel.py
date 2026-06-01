from model.model import Model

model = Model()
model.creaGrafo(1)
print(model.getNumNodes())
print(model.getNodes())
print(model.getNumEdges())
print(model.getMaggAffl())
print(model.getTopArchi())
nodo1 = model.getNodes()
print(nodo1)
nodo2 =nodo1[0]
print(nodo2)
listaArt = model.getTopLista(nodo1[0])
for a in listaArt:
    print(a)