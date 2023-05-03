from flask import render_template, flash, redirect, url_for
from flask import session, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for
import pandas
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session
from flask import session, make_response
from flask import Flask, render_template, request, redirect, url_for, flash
import hashlib
import pandas as pd

df = pandas.read_excel('quik.xlsx')


class Item:
    def __init__(self, name, price, gram, image_link):
        self.name = name
        self.price = price
        self.gram = gram
        self.image_link = image_link
        self.ava = ""
        self.price2 = 0
        # print(df)
        df2 = df.copy()
        print(self.name, self.gram)
        matching_productnames = df[(df['NAME']).str.contains(
            self.name, case=False)]
        try:
            self.price2 = matching_productnames.iloc[0]["PRICE"]
            print(self.price2)
        except:
            self.ava = "this item isnt available in quick"
        # print("<><><><><><<")
        # print(matching_productnames)
        # g = str(gram)
        # g.replace("םרג", "")
        # print(g)
        # print("<><><><><><<")
        # matching_productnames['GRAM'] = matching_productnames['GRAM'].astype(
        #     str).str.extract('(\d+)').astype(int)
        # matching_productgrams = matching_productnames[matching_productnames['GRAM'].astype(
        #     str).str.contains(str(self.name), case=False)]

        # print(matching_productgrams)
        # print("<><><><><><<")
        # print(matching_productgrams)
        # print(matching_product)
        # if not matching_product.empty:
        #     print(matching_product.iloc[0]['PRICE'])
        #     self.price2 = (matching_product.iloc[0]['PRICE'])
        # else:
        #     print('No matching product found')
        #     self.ava = "this item isnt available in quick"

        # try:
        #     num2 = df.loc[(df['NAME'].str.contains(self.name)) &
        #                   (df['GRAM'] == self.gram)].iloc[0]['PRICE']
        #     print("Wwe")
        # except:
        #     print("LLE")
        #     self.num2 = 0
        #     self.ava = "this item isnt available in quick"
        # self.price2 = num2

    def __str__(self):
        return f"{self.name, self.price, self.gram, self.image_link}"
