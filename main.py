from bokeh.io import curdoc
import pandas as pd
from bokeh.models import Tabs
from pure_data import table_tab
from clean_data import cleaned_data
from pvalue import comparison

data = pd.read_csv("ab_data.csv")
tab_table = table_tab(data)
cleaned_data_tab = cleaned_data(data)
tab_comp = comparison(data)

finall = Tabs(tabs=[tab_table, cleaned_data_tab, tab_comp])
curdoc().add_root(finall)
