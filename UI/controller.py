import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.genereSelezionato = None

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        generiOpt = list(map(lambda x: ft.dropdown.Option(data = x, text = x.Name, on_click = self.readDDGenere), generi))
        self._view._ddGenre.options= generiOpt


    def readDDGenere(self, e):
        if e.control.data is None:
            self.genereSelezionato = None
        else:
            self.genereSelezionato = e.control.data
            print(self.genereSelezionato)
    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass