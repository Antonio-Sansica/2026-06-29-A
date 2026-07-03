from database.DB_connect import DBConnect
from model.customer import Customer


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct c.Country as Country
                from Customer c 
                order by c.Country asc
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row['Country'])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodi(country):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT distinct c.*, SUM(i.Total) as Fatturato
                    from Customer c 
                    join Invoice i on c.CustomerId = i.CustomerId 
                    where c.Country = %s
                    group by c.CustomerId
                    """

        cursor.execute(query,(country,))

        for row in cursor:
            customer = Customer(**row)
            results.append(customer)
            print(customer)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(country1, country2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT distinct t1.id1 as id_1, t2.id2 as id_2
                from
                (SELECT distinct c.CustomerId as id1, a.ArtistId as a1
                from Customer c 
                join Invoice i on c.CustomerId = i.CustomerId 
                join InvoiceLine il on i.InvoiceId = il.InvoiceId 
                join Track t on il.TrackId = t.TrackId 
                join Album a on t.AlbumId = a.AlbumId
                where c.Country = %s) t1,
                (SELECT c.CustomerId as id2, a.ArtistId as a2
                from Customer c 
                join Invoice i on c.CustomerId = i.CustomerId 
                join InvoiceLine il on i.InvoiceId = il.InvoiceId 
                join Track t on il.TrackId = t.TrackId 
                join Album a on t.AlbumId = a.AlbumId
                where c.Country = %s) t2
                where t1.a1 = t2.a2 and t1.id1 < t2.id2
                """

        cursor.execute(query, (country1, country2))

        for row in cursor:
            results.append((row['id_1'], row['id_2']))

        cursor.close()
        conn.close()
        return results