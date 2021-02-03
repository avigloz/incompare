#!/bin/python
# (C) Avi Glozman, 2021. The following code is licensed under the MIT license.
############################################
#external dep
import plotly.graph_objects as go
import requests
#std
import sys
dim = list([ # table for plotly
    dict(range = [70000, 120000],
        ticktext = [],
        tickvals = [],
        label = 'Gross Annual Income', values = []),
    dict(range = [15000, 40000],
        ticktext = [],
        tickvals = [],
        label = 'Annual Tax', values = []),
    dict(range = [30000, 60000],
        ticktext = [],
        tickvals = [],
        label = 'Annual Savings', values = []),
    dict(range = [8000,15000],
        ticktext = [],
        tickvals = [],
        label = 'Annual Spending Money', values = []),
    dict(range = [600,1500],
        ticktext = [],
        tickvals = [],
        label = 'Monthly Spending Money', values = []),
    dict(range = [1.5,3.5],
        ticktext = [],
        tickvals = [],
        label = 'Years Until Debt-Free', values = [])
])

def main():
    getTaxRates()
    data = argParse()
    output(data)

#TODO get taxes by location
def getTaxRates(incomes: list = [120000], zip: str = None) -> list:
    if (zip == None):
        zip = getZip()
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    url = "https://smartasset.com/taxes/income-taxes"
    params = {"render": "json"}

    for inc in incomes:
        print(inc)
        data = {
            "ud-it-household-income" : inc,
            "ud-current-location" : "ZIP|14205" + zip
        }
        # There's some issue with the "requests" module, which inhibts this code from functioning properly.
        data_enc = f'ud-it-household-income={inc}&ud-current-location=ZIP|{zip}'
        res = requests.post(url=url, data=data, headers=headers, params=params, allow_redirects=False)
        print(res.json()['user_data']['ud-it-household-income']['value'])
        print(res.json()['page_data']['2020']['totalEffectiveTaxRate'])
    exit(0)
    return tax

def argParse() -> list:
    args = sys.argv[1:]
    data = [0.8, None, 10800, 112000.0, [70000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 120000]]
    for i, a in enumerate(args):
        if (a == "-h" or a == "--help"):
            print("Usage:\n" + 
                "$ python3 ic.py [-s] [-z] [-i] [-r] [-d]\n\n" + 
                "-s -> percentage of annual salary dedicated to savings\n" + 
                "-z -> zipcode override\n" + 
                "-i -> comma-separated list of incomes to include\n" + 
                "-r -> annual rent (1 month's rent * 12)\n" + 
                "-d -> total (college) debt (adding estimated interest over time to this number in advance would be ideal)\n\n" +
                "-r FORMAT: 1,2,3,4 (comma-separated, no spaces, just integers)\n" +
                "-s FORMAT: 0.5 or 0.75 (any decimal %)"
            )
            exit(0)
        elif (a == "-s"):
            data[0] = float(args[i + 1])
        elif (a == "-z"):
            data[1] = args[i + 1]
        elif (a == "-r"):
            data[2] = int(args[i + 1])
        elif (a == "-d"):
            data[3] = float(args[i + 1])
        elif (a == "-i"):
            data[4] = [int(i) for i in args[i+1].split(',')]
            data[4].sort()

    tax = [0.2476, 0.2613, 0.267, 0.2720, 0.2767, 0.2813, 0.286, 0.2903, 0.2979] # 2020 tax rates for NY-employed NJ residents
    # if (data[1] is None):
    #     tax = getTaxRates()
    data.append(tax)
    setRanges(data)
    return data

def output(data: list):
    #   data = [0.8, None, 10800, 112000.0, [70000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 120000]]
    for c, i in enumerate(data[4]):
        tp = i * data[5][c] # taxes paid
        ptpr = (i * (1 - data[5][c])) - data[2] # post-tax and rent
        s = ptpr * data[0] # annual savings (after taxes and rent)
        pt_disp = ptpr - s # post-tax annual disposable (after savings, taxes, and rent)
        m_disp = pt_disp / 12 # monthly disposable
        
        i_txt = prettyDollars(i)
        dim[0]['ticktext'].append(i_txt)
        dim[0]['tickvals'].append(i)
        dim[0]['values'].append(i)

        vals = [tp, s, pt_disp, m_disp, data[3]/s]
        vals_txt = [prettyDollars(tp), prettyDollars(s), prettyDollars(pt_disp), prettyDollars(m_disp)]
        for c in range(len(dim) - 1):
            dim[c + 1]['values'].append(vals[c])
            dim[c + 1]['tickvals'].append(vals[c])
            if (dim[c + 1]['label'] != 'Years Until Debt-Free'):
                dim[c + 1]['ticktext'].append(prettyDollars(vals[c]))
            else:
                dim[c + 1]['ticktext'].append(shortYears(vals[c]))

        #print("Gross salary: $%.2f (pre-tax)\nActual salary: $%.2f (post-tax, post-rent)\nTaxes: $%.2f\nAnnual savings: $%.2f\nAnnual disposable: $%.2f\nMonthly disposable income: $%.2f\nYears to pay debts: ~%.2f\n---------------" %(i, ptpr, tp, s, pt_disp, m_disp, 112000.0/s))

    fig = go.Figure(data=
        go.Parcoords(
            line = dict(
                color = data[4],
                colorscale = 'rainbow',
            ),
            dimensions = dim
        )
    )
    fig.update_layout(
        title="Income Comparison",
        title_x = 0.02,
        title_y = 0.98,
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
        showlegend=False
    )
    fig.show()

def setRanges(data: list):
    # calculate range for gross annual income
    income = data[4] # sorted income list
    inc_top = income[len(income) - 1]
    inc_bot = income[0]
    dim[0]['range'] = [inc_bot - 500, inc_top]

    # calculate range for annual taxes paid
    tax = data[5]
    tax_top = tax[len(tax) - 1] * inc_top
    tax_bot = tax[0] * inc_bot
    dim[1]['range'] = [round(tax_bot, -3) - 2000, round(tax_top, -3) + 4000]

    # calculate range for annual savings
    sav_bot = dim[1]['range'][0]*1.75
    sav_top = dim[1]['range'][1]*1.5
    dim[2]['range'] = [sav_bot, sav_top] # shitty approximation. it doesn't need to be perfect though

    # calculate range for annual spending money/raw disposable income
    ansp_bot = round((inc_bot - tax_bot - sav_bot)/3, -3) - 1000
    ansp_top = round((inc_top - tax_top - sav_top)/1.5, -3)
    dim[3]['range'] = [ansp_bot, ansp_top]

    # calculate range for monthly spending money
    dim[4]['range'] = [round(ansp_bot/12, -2) - 100, round(ansp_top/12, -2) + 100]

    # calculate range for years until debt free
    dim[5]['range'] = [round(data[3]/sav_top) - 0.5, round(data[3]/sav_bot) - 0.5]  

    # for debugging
    for i in range(6):
        print(dim[i]['label'] + " " + str(dim[i]['range']))

def getZip() -> str:
    res = requests.get("https://ifconfig.co/json")
    return res.json()['zip_code']

def prettyDollars(val) -> str:
    return "${:,.0f}".format(val) # monetary value as text
def shortYears(years) -> float:
    return float("{:.2f}".format(years))

if __name__ == "__main__":
    main()