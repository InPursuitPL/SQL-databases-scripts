import sqlite3
import pprint

def pretty_print_results(query):
    with sqlite3.connect("movie.db") as db:
        cursor = db.cursor()
        cursor.execute(query)
        output = cursor.fetchall()
        pprint.pprint(output)

#pretty_print_results("""select * from film where filmID=183""")
#pretty_print_results("""select * from user where userID<=715 and userOccupation="technician" and userGender="M" order by userID asc""")
#pretty_print_results("""select * from user where userAge<30 and userOccupation="technician" and userGender="M" order by userID asc""")
#pretty_print_results("""select userAge, userOccupation from user where userGender="F" limit 17""")
#pretty_print_results("""select title, releaseYear from film where releaseYear=1998""")
#select title from film, genreName from genre, where title="Die Hard" film[filmID]=filmgenre[filmID] and filmgenre[genreID]=genre[genreID] where genre[genreName]
pretty_print_results("""
select film.title, genre.genreName
from film, genre, filmgenre
where film.filmID=filmgenre.filmID and filmgenre.genreID=genre.genreID
and film.title='Die Hard' """)


