import copy

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

    def getMaggAffl(self):
        bestArt = None
        bestAffl = 0
        for n in self._grafo.nodes:
            arcEntr = 0
            arcUsc = 0
            for a in self._grafo.in_edges(n):
                arcEntr += self._grafo[a[0]][a[1]]['weight']
            for a in self._grafo.out_edges(n):
                arcUsc += self._grafo[a[0]][a[1]]['weight']
            affl = arcUsc - arcEntr
            if affl>bestAffl:
                bestArt = n
                bestAffl = affl
        return bestArt, bestAffl

    def getTopArchi(self):
        archi = list(self._grafo.edges(data="weight"))
        archi.sort(key = lambda x: x[2], reverse = True)
        return archi[:5]

    def getTopLista(self, source):
        self._bestListaArt = []
        parziale = [source]
        pesoCorr = 0
        for n in self._grafo.successors(source):
            if n not in parziale:
                if self._grafo[source][n]['weight'] > pesoCorr:
                    pesoCorr = self._grafo[source][n]['weight']
                    parziale.append(n)
                    self._ricorsione(parziale, pesoCorr)
                    parziale.pop()
        return self._bestListaArt

    def _ricorsione(self, parziale, pesoCorr):
        #cond Ottimale
        if len(parziale) > len(self._bestListaArt):
            self._bestListaArt = copy.deepcopy(parziale)
        else:
            for n in self._grafo.successors(parziale[-1]):
                if n not in parziale:
                    m = parziale[-1]
                    if self._grafo[m][n]['weight'] > pesoCorr:
                        n = pesoCorr
                        pesoCorr = self._grafo[m][n]['weight']
                        parziale.append(n)
                        self._ricorsione(parziale, pesoCorr)
                        parziale.pop()


    def getScore(self):
        pass
    def getGrafo(self):
        return self._grafo