import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the processed sales data (from Task 2)
df = pd.read_csv("formatted_sales_data.csv")

# Normalize and prepare fields
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
df["region_norm"] = df["region"].astype(str).str.strip().str.lower()

# Helper to build the figure from a filtered dataframe
def create_figure(filtered_df):
    # If there's no data for this selection, return an empty/informative chart
    if filtered_df.empty:
        fig = px.line(title="No data for selected region")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Sales",
        )
        return fig

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Sales"},
    )

    # Add a vertical line marking the price increase date (using string date on time axis)
    y_min = filtered_df["sales"].min()
    y_max = filtered_df["sales"].max()
    padding = (y_max - y_min) * 0.05 if (y_max > y_min) else max(y_max * 0.05, 1)

    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=y_min - padding,
        y1=y_max + padding,
        line=dict(color="red", dash="dash"),
    )

    fig.add_annotation(
        x="2021-01-15",
        y=y_max + padding,
        text="Price Increase",
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=-40,
    )

    fig.update_layout(transition_duration=400, margin=dict(t=80, l=40, r=40, b=40))
    return fig

# Create the Dash app
app = Dash(__name__, suppress_callback_exceptions=False)

# Layout
app.layout = html.Div(
    className="container",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Soul Foods — Pink Morsel Sales Visualiser"),
                html.P("Use the radio buttons to filter sales by region.", className="subtitle"),
            ],
        ),

        # Controls: radio buttons
        html.Div(
            id="radio-container",
            className="controls",
            children=[
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    labelStyle={"display": "inline-block", "marginRight": "18px"},
                    inputStyle={"marginRight": "8px"},
                    persistence=True,
                    persistence_type="session",
                )
            ],
        ),

        # Chart
        dcc.Graph(id="sales-line-chart", figure=create_figure(df)),

        html.Div(
            className="footer",
            children="Tip: The red dashed line marks the price increase (15 Jan 2021).",
        ),
    ],
)

# Callback to update the figure based on radio selection
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(selected_region):
    if not selected_region or selected_region == "all":
        filtered = df
    else:
        filtered = df[df["region_norm"] == selected_region]

    return create_figure(filtered)


if __name__ == "__main__":
    # Newer Dash uses app.run(...)
    app.run(debug=True)
