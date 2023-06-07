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
import re

df = pandas.read_excel("quik.xlsx")


class Item:
    def __init__(self, name, price, gram, image_link):
        df = pandas.read_excel("quik.xlsx")
        self.name = name
        self.price = price
        self.gram = gram
        self.image_link = image_link
        self.ava = ""
        self.price2 = 0
        # print(df)
        df2 = df.copy()
        print(self.name, self.gram)
        matching_productnames = df[(df["NAME"]).str.contains(self.name, case=False)]
        if matching_productnames.empty:
            words = self.name.split()
            first_two_words = " ".join(words[:2])
            print(first_two_words)
            matching_productnames = df[
                (df["NAME"]).str.contains(first_two_words, case=False)
            ]
            if matching_productnames.empty:
                last_two_words = " ".join(words[-2:])
                matching_productnames = df[
                    (df["NAME"]).str.contains(first_two_words, case=False)
                ]

        print("***********")
        print(matching_productnames)
        gramsstr = str(self.gram + "")
        print("***")
        print(self.gram)
        print("***")
        gramnumber = re.sub(r"\D", "", self.gram)
        print(gramnumber)  # המתוקן
        print("***??????????????")
        # matching_productgrams = matching_productnames[
        #     matching_productnames["GRAM"].astype(str).str.contains(gramsstr, case=False)
        # ]
        # print("***")
        # print(matching_productgrams)

        try:
            i = -1
            x = True
            # lendf = len(matching_productnames)
            while x:
                i = i + 1
                print(i)
                print(matching_productnames)
                gram2 = matching_productnames.iloc[i]["GRAM"]
                print(gramnumber)
                print(gram2)
                print("hiiiiiiiiii")
                try:
                    gram2 = re.sub(r"\D", "", gram2)
                except:
                    print("hh")

                print(matching_productnames.iloc[i]["PRICE"])

                if int(gramnumber) == int(gram2):
                    self.price2 = matching_productnames.iloc[i]["PRICE"]
                    x = False
                if i > matching_productnames.shape[0]:
                    x = False
                # if i == lendf:
                #     x = False
                #     self.ava = "this item isnt available in quick"

                print(self.price2)
        except:
            self.ava = "this item isnt available in quick"
        print("**********")

        print(self.name, self.gram)
        if self.price2 > 0:
            self.ava = ""
        self.price2 = round(self.price2, 1)

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
