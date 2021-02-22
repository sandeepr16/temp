from flask import Flask, render_template, request
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import datetime
import os
app = Flask(__name__, template_folder='templates')

nseid = ''


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route('/comp', methods=['GET'])
def comp():
    return render_template('stock.html')


@app.route('/swot', methods=['GET', 'POST'])
def swot():
    for filename in os.listdir('static/images/'):
        if filename.startswith('graph'):
            os.remove('static/images/' + filename)
    s1 = request.form["companyname"]
    if(s1 == ''):
        return render_template('error.html')
    name1, st1, we1, op1, tt1, x1, y1, url1 = myfun(s1, 0)
    s2 = request.form["companyname1"]
    if (s2 == ''):
        return render_template('error.html')
    name2, st2, we2, op2, tt2, x2, y2, url2 = myfun(s2, 1)
    return render_template("stock.html", urla=url1, urlb=url2, compname=name1, strn=st1, weak=we1, oppr=op1, thrt=tt1, headings=x1, values=y1, compname1=name2, strn1=st2, weak1=we2, oppr1=op2, thrt1=tt2, headings1=x2, values1=y2, name11="STRENGTH", name2="WEAKNESS", name3="OPPURTUNITIES", name4="THREATS")


def myfun(s, count):
    new_graph_name = ""
    imgurl = ""
    df = pd.read_csv('Swot.csv')
    nse = df[df['Title'] == s]
    nse = list(nse['NSE'])
    nse1 = nse[0]
    p = df[df["NSE"] == nse1]
    st = []
    we = []
    op = []
    tt = []
    for x in p["Strength"]:
        x = list(map(str, x.split("', '")))
        for o in x:
            st.append(o.replace("']", "").replace("['", ""))
    for x in p["Weakness"]:
        x = list(map(str, x.split("', '")))
        for o in x:
            we.append(o.replace("']", "").replace("['", ""))
    for x in p["Oppurtunity"]:
        x = list(map(str, x.split("', '")))
        for o in x:
            op.append(o.replace("']", "").replace("['", ""))
    for x in p["Threat"]:
        x = list(map(str, x.split("', '")))
        for o in x:
            tt.append(o.replace("']", "").replace("['", ""))
    filedf = pd.read_csv('BaseData.csv')
    dfr = pd.DataFrame(filedf.loc[filedf['NSE'] == nse1].dropna(axis=1))
    qx = list(dfr.columns[3:])
    qyy = dfr.values.tolist()[0][3:]
    qy = []
    for j in range(len(qyy)):
        qy.append(qyy[j])
    Finaldf = []
    for k in range(4):
        filelist = ["Quarterly.csv", "pandlNetp.csv",
                    "Cash-flow.csv", "Balance Sheet.csv"]
        filedf = pd.read_csv(filelist[k])
        dfr = pd.DataFrame(filedf.loc[filedf['NSE'] == nse1].dropna(axis=1))
        qxx = list(dfr.columns[3:])
        qyyyy = dfr.values.tolist()[0][3:]
        qyyy = []
        for j in range(len(qyyyy)):
            qyyy.append(qyyyy[j])
        Finaldf.append(qxx)
        Finaldf.append(qyyy)
    plottitle = ["", "Quarterly Results",
                 "Profit and Loss", "Cash Flow", "Balance Sheet"]
    xlabels = ['', 'Quarters', 'Years', 'Years']
    ylabels = ['', 'Net Profit', 'Net Profit', 'Net Cash Flow']
    fig, ax = plt.subplots(4, 1, figsize=(18, 20))
    it = 0
    for i in range(3):
        ax[i].plot(Finaldf[it], Finaldf[it+1])
        ax[i].axhline(0, color='black')
        ax[i].set_xlabel(xlabels[i+1])
        ax[i].set_ylabel(ylabels[i+1])
        ax[i].set_title(plottitle[i+1])
        it = it+2
    x = np.arange(len(Finaldf[7]))
    width = 0.3
    rects1 = ax[3].bar(x - width/2, Finaldf[7], width, label='Assets')
    rects2 = ax[3].bar(x + width/2, Finaldf[7], width, label='Liabilities')
    ax[3].set_ylabel('Amount in Crores')
    ax[3].set_title(plottitle[4])
    ax[3].set_xticks(x)
    ax[3].set_xticklabels(Finaldf[6])
    ax[3].legend()
    if count == 0:
        new_graph_name = "graph" + str(time.time()) + ".png"
        plt.savefig('static/images/' + new_graph_name)
        imgurl = 'static/images/' + new_graph_name
    else:
        new_graph_name = "graph1" + str(time.time()) + ".png"
        plt.savefig('static/images/' + new_graph_name)
        imgurl = 'static/images/' + new_graph_name
    return s, st, we, op, tt, qx, qy, imgurl


if __name__ == "__main__":
    app.run(debug=True)
