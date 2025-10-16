from bokeh.models import ColumnDataSource, TabPanel, TableColumn, DataTable, Div, Spacer
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column, row
import matplotlib.pyplot as plt
from bokeh.transform import cumsum
from math import pi
import io
import base64


def table_tab(data):

    # table1:shape
    title = Div(text=" <h2 style='margin: 5px 0 0 0;'>Pure Data Shape</h2>")
    count_data_rows, count_data_columns = data.shape
    source = ColumnDataSource(
        data=dict(
            feature=["number of columns", "number of rows"],
            value=[count_data_columns, count_data_rows],
        )
    )
    columns = [
        TableColumn(field="feature", title="feature", width=50),
        TableColumn(field="value", title="value"),
    ]
    shape_table = DataTable(
        source=source,
        columns=columns,
        sizing_mode="stretch_width",
        height=200,
        index_position=None,
    )

    # table2:info
    title2 = Div(text="<h2 style='margin: 5px 0 0 0;'>columns describes</h2>")

    column_names = data.columns.tolist()
    non_null_counts = data.notnull().sum().tolist()
    dtypes = data.dtypes.astype(str).tolist()
    unique_counts = data.nunique().tolist()

    row_numbers = list(range(1, len(column_names) + 1))

    source2 = ColumnDataSource(
        data=dict(
            Row=row_numbers,
            Column=column_names,
            count=non_null_counts,
            Dtype=dtypes,
            Uniques=unique_counts,
        )
    )
    columns2 = [
        TableColumn(field="Row", title="", width=20),
        TableColumn(field="Column", title="column name"),
        TableColumn(field="count", title="Non-Null Count"),
        TableColumn(field="Dtype", title="type"),
        TableColumn(field="Uniques", title="unique values"),
    ]
    info_table = DataTable(
        source=source2,
        columns=columns2,
        sizing_mode="stretch_width",
        height=200,
        index_position=None,
    )

    # cahrts
    def create_conversion_pie_charts(data):
        control = data.query("group == 'control'")
        treatment = data.query("group == 'treatment'")

        count_control = len(control)
        count_treatment = len(treatment)
        count_control_zero = (control["converted"] == 0).sum()
        count_control_one = (control["converted"] == 1).sum()
        count_treatment_zero = (treatment["converted"] == 0).sum()
        count_treatment_one = (treatment["converted"] == 1).sum()

        count_control_old = (control["landing_page"] == "old_page").sum()
        count_control_new = (control["landing_page"] == "new_page").sum()

        count_treatment_old = (treatment["landing_page"] == "old_page").sum()
        count_treatment_new = (treatment["landing_page"] == "new_page").sum()

        fig, axes = plt.subplots(2, 3, figsize=(12, 6))
        axes = axes.flatten()

        pie_data = [
            ([count_control, count_treatment], ["control", "treatment"], "Group Counts"),
            ([count_treatment_zero, count_treatment_one], ["Not Converted", "Converted"], "Treatment Conversion"),
            ([count_control_zero, count_control_one], ["Not Converted", "Converted"], "Control Conversion"),
            ([count_control_old, count_control_new], ["old page", "new page"], "Control Page Type"),
            ([count_treatment_old, count_treatment_new], ["old page", "new page"], "Treatment Page Type"),
        ]

        for i, (values, labels, title) in enumerate(pie_data):
            wedges, texts, autotexts = axes[i].pie(
                values, labels=labels, autopct="%1.2f%%", startangle=90, colors=["green", "red"]
            )
            axes[i].set_title(title)

            if i == 0:
                for t in texts:
                    t.set_rotation(90)
                for spine in axes[i].spines.values():
                    spine.set_visible(True)
                    spine.set_color("black")
                    spine.set_linewidth(1)

        fig.delaxes(axes[5])

        plt.subplots_adjust(hspace=0.5, wspace=0.3)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close(fig)

        from bokeh.models import Div

        div_charts = Div(
            text=f"<h2 style='text-align:center; margin: 0 0 0 0;'>Conversion Comparison</h2>"
            f"<img src='data:image/png;base64,{image_base64}' "
            f"style='display:block;margin:auto;width:100%;'/>",
            sizing_mode="stretch_width",
        )
        return div_charts

    # main layout
    left_section1 = column(title, shape_table, sizing_mode="stretch_width")
    gap = Spacer(width=50)
    right_section1 = column(title2, info_table, sizing_mode="stretch_width")
    section_1 = row(left_section1, gap, right_section1, sizing_mode="stretch_width")
    section_2 = create_conversion_pie_charts(data)

    layout = column(section_1, section_2)
    tab = TabPanel(child=layout, title="pure data")

    return tab
