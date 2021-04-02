import re
import sys
from flask import Flask, redirect, url_for, render_template

dataBase = {}
ocurrences = []

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html", content = ocurrences)

@app.route("/<name>")
def category(name):
    return render_template("category.html", content = dataBase.get(name.upper(), []), category = name.upper())

def getOcurrences():
    for key, value in dataBase.items():
        ocurrences.append((key, len(value)))

def processFile(filename):
    f = open(filename, "r")
    contador = 1
    inicio = 0
    fim = 0
    data = ""
    y = ""
    for linha in f:
        v = re.search(r'^[BI]', linha)
        if v:
            if v.group() == "B":
                if data != "":
                    if y.group(1) in dataBase:
                        dataBase[y.group(1)].append((data, str(inicio) + " - " + str(fim)))
                    else:
                        dataBase[y.group(1)] = []
                        dataBase[y.group(1)].append((data, str(inicio) + " - " + str(fim)))
                data = (re.search(r'[a-zA-Z0-9]{,}$', linha)).group()
                inicio = contador
            else:
                data += (" " + (re.search(r'[a-zA-Z0-9]{,}$', linha)).group())
                fim = contador
            y = re.search(r'-([a-zA-Z]+)', linha)
        contador += 1

    if y.group(1) in dataBase:
        dataBase[y.group(1)].append((data, str(inicio) + " - " + str(fim)))
    else:
        dataBase[y.group(1)] = []
        dataBase[y.group(1)].append((data, str(inicio) + " - " + str(fim)))

if __name__ == "__main__":
    processFile("train.txt")
    getOcurrences()
    app.run(debug = True)
