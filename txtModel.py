from database.DAO import DAO
from model.model import Model

mymodel = Model()

mymodel.build_graph('Canada')

#attori = DAO.getAllActors(valore1, valore2)

# print(len(attori))

#NODI
#n = DAO.getAllNodi('Canada')
#print(n)
#print(f"il Grafo ha {len(n) } nodi")
#archi = DAO.getAllArchi()

#archi

#tutto dettagli
n, m = mymodel.get_dettagli_grafo()
print(f"Grafo creato: {n} nodi, {m} archi")