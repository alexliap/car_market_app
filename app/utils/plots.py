import pandas as pd
import plotly.express as px


def brand_pie_chart(dataset):
    dummy = dataset["make"].value_counts()
    dummy = pd.DataFrame(
        pd.concat([pd.Series(dummy.index), pd.Series(dummy.values)], axis=1)
    )
    dummy.columns = ["make", "counts"]

    dummy.loc[dummy["counts"] <= 100, "make"] = "Other"

    fig = px.pie(dummy, values="counts", names="make", title="Brand Frequency")

    return fig
