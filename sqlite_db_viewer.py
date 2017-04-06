#! python3
# sqlite_db_viewer.py - simple script that prints tables and columns names in
# the given database.
import sqlite3

db_filename = input('Name of database file: ')
if db_filename == '':
    db_filename = 'coffee_shop.db'
    
newline_indent = '\n   '
print(db_filename)

db=sqlite3.connect(db_filename)
db.text_factory = str
cur = db.cursor()

sql = "SELECT name FROM sqlite_master WHERE type='table';"
result = cur.execute(sql).fetchall()
table_names = sorted(list(zip(*result))[0])
print("\ntables are:"+newline_indent+newline_indent.join(table_names))

for table_name in table_names:
    result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
    column_names = list(zip(*result))[1]
    print("\ncolumn names for %s:" % table_name+newline_indent+(
        newline_indent.join(column_names)))

db.close()

