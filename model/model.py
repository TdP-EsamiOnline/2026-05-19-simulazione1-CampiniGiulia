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
        # PROBLEMA 0: il grafo che abbiamo costruito aveva archi che andavano dal nodo con popolarità più alta a
        # nodo con popolarità più bassa. Quindi la tua soluzione era corretta (ed infatti tornava con gli screen). Il
        # problema è che quando cerchiamo una lista di nodi a pesi di archi crescenti, per come è costruito questo grafo
        # questi cammini non possono che essere lunghi due, perchè tutti gli archi uscenti vanno verso nodi che hanno
        # popolarità più grande, per cui dopo un solo arco, sono già finito su un nodo con popolarità molto grande e tutti
        # gli archi uscenti hanno pesi più piccoli. Infatti, se invertiamo il senso dell'arco quando costruiamo il grafo,
        # e decidiamo che gli arci vanno dal nodo con popolarità minore al nodo con popolarità maggiore, i cammini vengono
        # decisamente più lunghi.
            if c.artista1.popolarita < c.artista2.popolarita:
                self._grafo.add_edge(c.artista1, c.artista2, weight = c.artista1.popolarita+c.artista2.popolarita)
            elif c.artista1.popolarita > c.artista2.popolarita:
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

    #QUESTA è una mia soluzione verbosa.
    # def getTopLista(self, source):
    #     self._bestListaArt = [source]
    #     self._ricorsione([source], 0)
    #     return self._bestListaArt
    #
    # def _ricorsione(self, parziale, pesoCorr):
    #     if len(parziale) > len(self._bestListaArt):
    #         self._bestListaArt = copy.deepcopy(parziale)
    #
    #     last = parziale[-1]
    #     print("NODE:", last, "PESO CORRENTE:", pesoCorr)
    #
    #     for _, succ, data in self._grafo.out_edges(last, data=True):
    #         pesoArco = data["weight"]
    #         print("  CANDIDATO:", succ, "PESO:", pesoArco)
    #
    #         if succ not in parziale and pesoArco > pesoCorr:
    #             print("  -> SCENDO")
    #             parziale.append(succ)
    #             self._ricorsione(parziale, pesoArco)
    #             parziale.pop()
    #         else:
    #             print("  -> SCARTO")


    def getTopLista(self, source):
        self._bestListaArt = []
        parziale = [source]
        pesoCorr = 0
        for n in self._grafo.successors(source):
            if n not in parziale:
                if self._grafo[source][n]['weight'] > pesoCorr:
                    # Stessa cosa di sotto.
                    # pesoCorr = self._grafo[source][n]['weight']
                    parziale.append(n)
                    self._ricorsione(parziale, self._grafo[source][n]['weight'])
                    parziale.pop()
        return self._bestListaArt

    def _ricorsione(self, parziale, pesoCorr):
        #cond Ottimale
        if len(parziale) > len(self._bestListaArt):
            self._bestListaArt = copy.deepcopy(parziale)
        # PROBLEMA2: qui c'era un else. In pratica, quando veniva trovata una soluzione ottima,
        # l'algoritmo non continuava ad esplorare quella traccia, il che è sbagliato. Non si stratta di una condizione di terminazione.
        for n in self._grafo.successors(parziale[-1]):
            if n not in parziale:
                m = parziale[-1]
                if self._grafo[m][n]['weight'] > pesoCorr:
                #PROBLEMA 1: aggiornare il nome della variabile pesoCorr qui va a modificarne il riferimento, per cui
                # quello che nella nostra logica era il peso dell'ultimo arco, veniva copiato anche ai rami "fratelli".
                # Va bene passare come parametro il pesoCorr ma non rinominiamolo dentro la ricorsione. Il problema non
                # è passare il peso corrente invece di calcolarlo on the fly, il problema è dagli lo stesso nome.
                    # pesoCorr = self._grafo[m][n]['weight']
                    parziale.append(n)
                    self._ricorsione(parziale, self._grafo[m][n]['weight'])
                    parziale.pop()


    def getScore(self):
        pass
    def getGrafo(self):
        return self._grafo