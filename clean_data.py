import pandas as pd
from bokeh.models import TabPanel, TableColumn, DataTable, Div, Spacer, ColumnDataSource
from pure_data import table_tab
from bokeh.layouts import column, row


def cleaned_data(data):

    mistake_control = data.query("group == 'control' and landing_page == 'new_page'")
    mistake_treatment = data.query("group == 'treatment' and landing_page == 'old_page'")
    clean_data = data.drop(mistake_control.index).drop(mistake_treatment.index)

    duplicated_data = clean_data["user_id"].duplicated()
    number_of_duplicated_data = sum(duplicated_data)
    exact_users_with_duplicate = clean_data[duplicated_data]["user_id"]
    clean_data = clean_data[~clean_data["user_id"].duplicated(keep="first")]

    # diffrence table
    title = Div(text=" <h2 style='margin: 5px 0 0 0;'>dfiffrence beetween pure data & clean data </h2>")

    source = ColumnDataSource(
        data=dict(
            information=[
                "deleted rows(by mistake of group and land page)",
                "deleted rows(by duplicated user)",
                "exact remover dublicat user(by user_id)",
            ],
            count=[
                len(mistake_control) + len(mistake_treatment),
                number_of_duplicated_data,
                exact_users_with_duplicate,
            ],
        )
    )

    columns = [
        TableColumn(field="information", title=""),
        TableColumn(field="count", title="count"),
    ]
    diffrence_table = DataTable(
        source=source,
        columns=columns,
        width=600,
        height=200,
        index_position=None,
    )

    section1 = row(table_tab(clean_data).child)
    section2 = column(title, diffrence_table)

    tab = column(section1, section2)
    tab_panel = TabPanel(child=tab, title="clean data")
    return tab_panel


def get_clean_data(data):
    mistake_control = data.query("group == 'control' and landing_page == 'new_page'")
    mistake_treatment = data.query("group == 'treatment' and landing_page == 'old_page'")
    clean_data = data.drop(mistake_control.index).drop(mistake_treatment.index)
    clean_data = clean_data[~clean_data["user_id"].duplicated(keep="first")]
    return clean_data
