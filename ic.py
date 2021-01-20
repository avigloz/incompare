#!/bin/python
import plotly.graph_objects as go

incomes = [70000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 120000]
stats = ["net annual income", "annual tax", "annual savings", "annual spending money", "monthly spending money", "years until no debt"]
tax = [0.2476, 0.2613, 0.267, 0.2720, 0.2767, 0.2813, 0.286, 0.2903, 0.2979] # 2020 tax rates for NY-employed non-residents
annual_savings = 0.8 # savings percentage
rent = 10800 # annual rent

dim = list([
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

def prettyDollars(val):
    return "${:,.0f}".format(val) # gross income as text
def shortYears(years):
    return float("{:.2f}".format(years))

for c, i in enumerate(incomes):
    tp = i * tax[c] # taxes paid
    ptpr = (i * (1 - tax[c])) - rent # post-tax and rent
    s = ptpr * annual_savings # annual savings (after taxes and rent)
    pt_disp = ptpr - s # post-tax annual disposable (after savings, taxes, and rent)
    m_disp = pt_disp / 12 # monthly disposable
    
    i_txt = prettyDollars(i)
    dim[0]['ticktext'].append(i_txt)
    dim[0]['tickvals'].append(i)
    dim[0]['values'].append(i)

    vals = [tp, s, pt_disp, m_disp, 112000.0/s]
    vals_txt = [prettyDollars(tp), prettyDollars(s), prettyDollars(pt_disp), prettyDollars(m_disp)]
    for c in range(len(dim) - 1):
        dim[c + 1]['values'].append(vals[c])
        dim[c + 1]['tickvals'].append(vals[c])
        if (dim[c + 1]['label'] != 'Years Until Debt-Free'):
            dim[c + 1]['ticktext'].append(prettyDollars(vals[c]))
        else:
            dim[c + 1]['ticktext'].append(shortYears(vals[c]))

    print("Gross salary: $%.2f (pre-tax)\nActual salary: $%.2f (post-tax, post-rent)\nTaxes: $%.2f\nAnnual savings: $%.2f\nAnnual disposable: $%.2f\nMonthly disposable income: $%.2f\nYears to pay debts: ~%.2f\n---------------" %(i, ptpr, tp, s, pt_disp, m_disp, 112000.0/s))

fig = go.Figure(data=
    go.Parcoords(
        line = dict(
            color = incomes,
            colorscale = 'rainbow',
        ),
        dimensions = dim
    )
)
fig.update_layout(
    title="Income Comparison (living in Jersey City, working in NYC)",
    title_x = 0.02,
    title_y = 0.98,
    plot_bgcolor = 'white',
    paper_bgcolor = 'white',
    showlegend=False
)

fig.show()