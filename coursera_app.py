from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from bs4 import BeautifulSoup
import pandas as pd
import threading

from coursera_parser import *

app = Flask(__name__)

@app.route("/index", methods=['GET', 'POST'])
def index():
    cats, _url = init_connect()
    cat_list = [ cat.string for cat in cats ]
    if request.method == "POST":
        data = request.form.get("category")
        #col = threading.Thread(target=collect_cat_data, args=(data,))
        #col.start()
        link = collect_cat_data(data)
        return render_template('index.html', cat_list=cat_list, data=data, link=link)
    else:
        return render_template('index.html', cat_list=cat_list)

if __name__ == '__main__':
    app.run()