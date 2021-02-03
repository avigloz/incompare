# incompare
Creates a plotly visualization for income comparison (relative to rent, savings, etc.)

Current state: **alpha** software, not ready for use; features (as described below) do not function fully. **Undergroing re-write.**

## Getting started

### Dependencies
- `plotly`
- `axios`
- TypeScript

### Building

`tcs ic.ts`
 
### Usage

This will display information as a parallel coordinates plot in your web browser, as well as a text-based summary in STDOUT.

`$ node ic.js [-s] [-z] [-i] [-r] [-d]`

- `-s` -> percentage of annual salary dedicated to savings (e.g 0.5)
- `-z` -> zipcode override
- `-i` -> comma-separated list of incomes to include
- `-r` -> annual rent (1 month's rent * 12)
- `-d` -> total (college) debt (adding estimated interest over time to this number in advance would be ideal)

Passing in these arguments is not *required*, but aside from fetching your income tax rates, incompare will default to hard-coded values, which may not reflect your own situation.

### Note

incompare does not take into account expenses such as non-incomes taxes, groceries, gas, childcare, gifts, vacation, or fancy dinners. Do keep these costs in mind when looking at numbers shown in graphs.

incompare will automatically get income tax rates using your approximate location (**guaranteed functionality within USA only**), so that it can display relevant information. Zipcode override can also be provided, to see the graph for a different place.

incompare does not store any information anywhere.

## Background

I'm a computer science new-grad, and I'm in debt ($100k+) thanks to exorbitant costs of tuition in the U.S.A.

I've written incompare ("income compare") to see an approximation of how various salaries will effect my quality of life and future planning going forward.

As of right now, I am still unemployed and accumulating more debt via interest.