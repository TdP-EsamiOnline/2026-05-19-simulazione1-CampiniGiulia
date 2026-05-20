from dataclasses import dataclass

from model.artista import Artista


@dataclass
class Collegamento:
    artista1: Artista
    artista2: Artista

    def __hash__(self):
        return hash((self.artista1.ArtistId, self.artista2.ArtistId))

    def __eq__(self, other):
        return (self.artista1.ArtistId== other.artista1.ArtistId, self.artista2.ArtistId== other.artista2.ArtistId)