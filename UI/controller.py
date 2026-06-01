import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.genereSelezionato = None
        self.grafoCreato = None

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        generiOpt = list(map(lambda x: ft.dropdown.Option(data = x, text = x.Name, on_click = self.readDDGenere), generi))
        self._view._ddGenre.options= generiOpt


    def readDDGenere(self, e):
        if e.control.data is None:
            self.genereSelezionato = None
        else:
            self.genereSelezionato = e.control.data.GenreId
            print(self.genereSelezionato)

    def handleCreaGrafo(self, e):
        if self.genereSelezionato == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere", color = "red"))
            self._view.update_page()
            return
        self._model.creaGrafo(self.genereSelezionato)
        self.grafoCreato = True
        self.fillDDArtisti()
        art, affl = self._model.getMaggAffl()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato:", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumNodes()}:", color="gree"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumEdges()}:", color="gree"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più affluente: {art.Name} Con affluenza: {affl}", color="gree"))
        topArtisti = self._model.getTopArchi()
        self._view.txt_result.controls.append(ft.Text("Top 5 Artisti", color="green"))
        for a in topArtisti:
            self._view.txt_result.controls.append(ft.Text(f"{a[0].Name} -->{a[1].Name}: {a[2]} ", color="green"))
        self._view.update_page()

    def fillDDArtisti(self):
        artisti = self._model.getNodes()
        artistiOpt = list(map(lambda x: ft.dropdown.Option(data = x, text = x.Name, on_click = self.readDDArt), artisti))
        self._view._ddArtist.options= artistiOpt

    def readDDArt(self, e):
        if e.control.data is None:
            self.artistaSelezionato = None
        else:
            self.artistaSelezionato = e.control.data
            print(self.artistaSelezionato)

    def handleCammino(self,e):
        if self.grafoCreato:
            nodiCamminoLungo = self._model.getTopLista(self.artistaSelezionato)
            if len(nodiCamminoLungo) != 0:
                self._view.txt_result.controls.append(ft.Text(f"Cammino trovato lungo {len(nodiCamminoLungo)}"))
                # PROBLEMA3: qui c'era un piccolo problema con la stampa, perchè non cambiava l'indice di nodiCamminoLungo.
                # Me lo sono riscritto sotto perchè non trovavo il problema, ma basta passare n ed n+1 come argomenti nelle []
                # for n in range(0, len(nodiCamminoLungo)-1):
                #     self._view.txt_result.controls.append(ft.Text(f"{nodiCamminoLungo[0].Name} - {nodiCamminoLungo[1].Name} -- {self._model.getGrafo()[nodiCamminoLungo[0]][nodiCamminoLungo[1]]['weight']}", color="green")) #{self._model.getGrafo[nodiCamminoLungo[0]][nodiCamminoLungo[1]]['weight']}
                for n in range(len(nodiCamminoLungo) - 1):
                    u = nodiCamminoLungo[n]
                    v = nodiCamminoLungo[n + 1]
                    w = self._model.getGrafo()[u][v]['weight']

                    self._view.txt_result.controls.append(
                        ft.Text(f"{u.Name} - {v.Name} -- {w}", color="green")
                    )


            else:
                self._view.txt_result.controls.append(ft.Text("Cammino non trovato"))

        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Creare il grafo prima di usare questo metodo"))
        self._view.update_page()
        pass