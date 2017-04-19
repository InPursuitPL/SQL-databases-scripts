#!python3
# product_management_program.py - simple CRUD program that uses sqlite database
# to manage products. I am aware that there is some boilerplate code in it but
# I wanted the program to be explicit as I was learning handling SQL while
# writing it.

import sqlite3
import sys


class Menu:
    """Handles simple CRUD program"""
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.menuText = """
Product Table Menu

1. (Re)Create Product Table
2. Add new product
3. Edit existing product
4. Delete existing product
5. Search for products
0. Exit

"""
        actions = {
            '1': self.create_table,
            '2': self.add_product,
            '3': self.edit_product,
            '4': self.delete_product,
            '5': self.search_for_products,
            '0': sys.exit,
            }
        while True:
            print(self.menuText)
            answer = input('Please select an option: ')
            if answer in actions:
                actions[answer]()
                continue
            else:
                print('This is not a valid choice.')

    def create_table(self):
        """Enables recreation of table in database."""
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name='Product'")
            result = cursor.fetchall()
            keep_table = True
            if len(result) == 1:
                response = input("The table 'Product' already exists, do you wish to recreate it? (y/n): ")
                if response == "y":
                    keep_table = False
                    print("The 'Product' table will be recreated - all existing data will be lost.")
                    cursor.execute("drop table if exists 'Product'")
                    db.commit()
                else:
                    print("The existing table was kept.")
                    input()
            else:
                keep_table = False
            if not keep_table:
                sql = """create table Product
                 (ProductID integer,
                 Name text,
                 Price real,
                 primary key(ProductID))"""
                cursor.execute(sql)
                db.commit()
                input('Done.')

    def add_product(self):
        """Adds product to the database."""
        name = input('Please enter name of new product: ')
        try:
            price = float(input(
                'Please enter the price of Lemonade (example: 2.45): '
            ))
        except ValueError:
            input("Wrong price format, please try again.")
            return
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            sql = "insert into Product (Name, Price) values (?,?)"
            cursor.execute(sql, (name, price))
            db.commit()
        input('Product added to the database.')

    def edit_product(self):
        """Shows products in formatted table and enables to edit product."""
        # Show products part.
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            cursor.execute("select * from Product")
            answer = cursor.fetchall()
            self.print_in_table(answer)
        # Edit product part.
            try:
                id = int(input('Please enter the id of the product to edit: '))
            except ValueError:
                input("Wrong id format, please try again.")
                return
            if not self.check_id_in_products(id):
                input("No product with given id in the database.")
                return
            name = input('Please enter new name for the product: ')
            price = float(input('Please enter the price of {}: '.format(name)))
            sql = "update Product set Name=?, Price=? where ProductID=?"
            cursor.execute(sql, (name,price,id))
            db.commit()
        input('Done')

    def delete_product(self):
        """Shows products in formatted table and enables to delete product."""
        # Show products part.
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            cursor.execute("select * from Product")
            answer = cursor.fetchall()
            self.print_in_table(answer)
        # Delete product part.
            try:
                id = int(input('Please enter the id of the product to delete: '))
            except ValueError:
                input("Wrong id format, please try again.")
                return
            if not self.check_id_in_products(id):
                input("No product with given id in the database.")
                return
            sql = "delete from Product where ProductID=?"
            cursor.execute(sql, (id,))
            db.commit()
        input('Done')

    def search_for_products(self):
        """
        Enables search functionality by product name and
        shows result in formatted table.
        """
        name = input('Please enter the name of the product to search for: ')
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            cursor.execute("select * from Product where Name=?", (name,))
            answer = cursor.fetchall()
            self.print_in_table(answer)
        input()

    def print_in_table(self, aList):
        """Helper function - prints database table in a formatted way."""
        space = 20
        print('Product ID'.ljust(space),
              'Product Name'.ljust(space),
              'Product Price'.ljust(space))
        for productTuple in aList:
            for element in productTuple:
                element = str(element)
                print(element.ljust(space), end=' ')
            print()
        print()

    def check_id_in_products(self, id):
        """Helper function - checks if given id exists in Product table."""
        with sqlite3.connect(self.databaseName) as db:
            cursor = db.cursor()
            cursor.execute("select ProductID from Product where ProductID=?", (id,))
            answer = cursor.fetchall()
            if answer:
                return True
            else:
                return False


if __name__ == '__main__':
    Menu("product_database.db")
