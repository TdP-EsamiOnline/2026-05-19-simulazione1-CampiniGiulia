
from database.DB_connect import DBConnect
from model.artista import Artista
from model.collegamenti import Collegamento
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.GenreId, g.Name 
                    from genre g """

        cursor.execute(query)

        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtisti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId , a.Name 
                   from artist a"""

        cursor.execute(query)

        for row in cursor:
            result.append(Artista(ArtistId=row["ArtistId"], Name=row["Name"], popolarita=0))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistiSelezionati(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId , a.Name 
                from artist a, album a2, track t 
                where a.ArtistId = a2.ArtistId and t.AlbumId = a2.AlbumId and t.GenreId =%s """

        cursor.execute(query, (genere, ))

        for row in cursor:
            result.append(Artista(ArtistId=row["ArtistId"], Name = row["Name"], popolarita=0))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistiPopolarita(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId, a.Name,  count(*) as popolarita
                    from artist a, album a2, track t, invoiceline i 
                    where a.ArtistId = a2.ArtistId and t.AlbumId = a2.AlbumId and i.TrackId = t.TrackId and t.GenreId =%s
                    group by a.ArtistId, a.Name"""

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(Artista(ArtistId=row["ArtistId"], Name=row["Name"], popolarita=row["popolarita"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistiArchi(idMap, genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c1.artista as a1, c2.artista as a2
                    from (select distinct a.ArtistId as artista, i2.CustomerId as cliente
		            from album a, track t, invoiceline i, invoice i2
		            where a.AlbumId =t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId and t.GenreId =%s) as c1,
		            (select distinct a.ArtistId as artista, i2.CustomerId as cliente
		            from album a, track t, invoiceline i, invoice i2
		            where a.AlbumId =t.AlbumId and t.TrackId = i.TrackId and i.InvoiceId = i2.InvoiceId and t.GenreId =%s) as c2
                    where c1.cliente = c2.cliente and c1.artista < c2.artista
                    order by c1.artista"""

        cursor.execute(query, (genere, genere,))

        for row in cursor:
            result.append(Collegamento(artista1=idMap[row["a1"]], artista2=idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result