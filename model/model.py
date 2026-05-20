import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        allArtisti = DAO.getAllArtisti()
        self.idMapArtisti = {}
        for a in allArtisti:
            self.idMapArtisti[a.ArtistId] = a

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def creaGrafo(self, genere):
        self._grafo.clear()
        self.nodi = DAO.getArtistiSelezionati(genere)
        self.nodiPop = []
        self.artistiPopolarita = DAO.getArtistiPopolarita(genere)
        for a in self.artistiPopolarita:
            self.idMapArtisti[a.ArtistId].popolarita = a.popolarita
        for n in self.nodi:
            self.nodiPop.append(self.idMapArtisti[n.ArtistId])
        self._grafo.add_nodes_from(self.nodiPop)
        self.addEdges(genere)

    def addEdges(self, genere):
        self.collegamenti = DAO.getArtistiArchi(self.idMapArtisti,genere)
        for c in self.collegamenti:
            if c.artista1.popolarita > c.artista2.popolarita:
                self._grafo.add_edge(c.artista1, c.artista2, weight = c.artista1.popolarita+c.artista2.popolarita)
            elif c.artista1.popolarita < c.artista2.popolarita:
                self._grafo.add_edge(c.artista2, c.artista1, weight=c.artista1.popolarita + c.artista2.popolarita)
            elif c.artista1.popolarita == c.artista2.popolarita:
                self._grafo.add_edge(c.artista1, c.artista2, weight=c.artista1.popolarita + c.artista2.popolarita)
                self._grafo.add_edge(c.artista2, c.artista1, weight=c.artista1.popolarita + c.artista2.popolarita)
            else:
                print("che succede")
    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNodes(self):
        return self._grafo.nodes
    def getNumEdges(self):
        return len(self._grafo.edges)