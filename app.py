import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load the processed sales data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort data by date
df = df.sort_values(by="date")

# Create the Dash app
app = dash.Dash(__name__)

# Create a line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Sales"
    }
)

# Add vertical line for price increase
fig.add_shape(
    dict(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=df["sales"].min(),
        y1=df["sales"].max(),
        line=dict(color="red", dash="dash"),
    )
)

# Add annotation
fig.add_annotation(
    dict(
        x="2021-01-15",
        y=df["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=3
    )
)

# App layout
app.layout = html.Div(children=[
    html.H1(
        children="Soul Foods Pink Morsel Sales Visualiser",
        style={"textAlign": "center", "marginBottom": "20px"}
    ),
    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)