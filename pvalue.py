from statsmodels.stats.proportion import proportions_ztest
from bokeh.models import Div, TabPanel, DataTable, ColumnDataSource, TableColumn
from bokeh.layouts import column, row
from clean_data import get_clean_data


def comparison(data):
    title = Div(
        text="<h2 style='margin: 5px 0 0 0;'>Comparison of the conversion rates between the new_page and old_page designs. </h2>"
    )
    title2 = Div(
        text="<h4 style='margin: 5px 0 0 0;'>As a first step, the average conversion rate for each design will be compared.</h4>"
    )

    data = get_clean_data(data)
    control_data = data.query("landing_page=='old_page'")
    control_mean = (control_data["converted"].mean()).round(4)
    tratment_data = data.query("landing_page=='new_page'")
    tratment_mean = (tratment_data["converted"].mean()).round(4)
    source = ColumnDataSource(
        data=dict(
            information=[
                "old_page conversion rate",
                "new_page conversion rate",
                "Conclusion",
            ],
            count=[
                f"{control_mean*100} %",
                f"{tratment_mean*100}%",
                "old page has bether conversion rate",
            ],
        )
    )
    columns = [
        TableColumn(field="information", title=""),
        TableColumn(field="count", title="count"),
    ]
    mean_compare_table = DataTable(
        source=source,
        columns=columns,
        width=600,
        height=200,
        index_position=None,
    )

    # pvalue with ztest
    title3 = Div(
        text="<h2 style='margin: 5px 0 0 0;'>In the second step, it must be examined whether this observed improvement is statistically significant or merely due to chance.</h2>"
    )
    count_control_one = len(control_data.query("converted == 1"))
    count_treatment_one = len(tratment_data.query("converted == 1"))

    stat, pvalue = proportions_ztest(
        [count_treatment_one, count_control_one],
        [len(tratment_data), len(control_data)],
        alternative="larger",
    )

    pvalue = (100 - (pvalue * 100)).round(2)

    if pvalue < 5:
        conclusion = "Since the p-value is below the 5% threshold, we can conclude that the new_page performed significantly better than the old_page."
    else:
        conclusion = "Since the p-value did not fall below the 5% threshold, we cannot confidently conclude that the old_page performed better than the new_page."

    source = ColumnDataSource(
        data=dict(
            information=["p-value", "Conclusion"],
            count=[f"{pvalue} %", conclusion],
        )
    )

    columns = [
        TableColumn(field="information", title="", width=100),
        TableColumn(field="count", title="Result", width=1200),
    ]

    ztest_table = DataTable(
        source=source,
        columns=columns,
        width=1000,
        height=200,
        index_position=None,
    )

    # output
    section1 = column(title, title2)
    section2 = row(mean_compare_table)
    section3 = column(title3, ztest_table)
    layout = column(section1, section2, section3)
    tab = TabPanel(child=layout, title="pvalue")
    return tab
