#!/usr/bin/env python3
from jakesutils.database import Database
import pandas as pd
import inquirer
from os import system
import tabview


class DatabaseReader:
    def __init__(self):
        self.database = Database()
        self.database.connect()
        self.client = self.database.client

    def get_databases(self) -> list:
        """Return all database names"""
        return self.client.list_database_names()

    def get_collections(self, database: str) -> list:
        """Return all collections in given database"""
        return self.client[database].list_collection_names()

    def get_documents(self, database: str, collection: str) -> list:
        """Return all documents in the collection passed in"""
        return self.client[database][collection].find({})

    def ask_question(self, items: list) -> str:
        """List items and ask for selection"""
        questions = [inquirer.List('size', choices=items)]
        answers = inquirer.prompt(questions)
        return answers['size']

    def get_user_requested_documents(self) -> list:
        """Get the documents from the collection and database, the user requested"""
        database = self.ask_question(self.get_databases())
        collection = self.ask_question(self.get_collections(database))
        documents = self.get_documents(database, collection)
        return documents

    def make_table(self):
        """Put the values and the labels in the order tabview can render"""
        documents = self.get_user_requested_documents()
        labels = [key for key in documents[0].keys()]
        table = [labels]
        for document in documents:
            values = [value for value in document.values()]
            table.append(values)
        return table

    def render_table(self):
        table = self.make_table()
        tabview.view(table)


def main():
    dbr = DatabaseReader()
    dbr.render_table()

if __name__ == "__main__":
    main()
