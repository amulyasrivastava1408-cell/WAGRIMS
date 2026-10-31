"""
WAGIRMS – Global Conflict Intelligence dashboard
Run:   python app.py      ->  http://127.0.0.1:8050/

Folder layout expected:
    WAGIRMS/
      dashboard/
        app.py
        assets/wagirms_dark.css
      data/processed/cleaned_conflict_data.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

# ----------------------------------------------------------------------
# 1. Data loading
# ----------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
CANDIDATES = [
    BASE.parent / "data" / "processed" / "cleaned_conflict_data.csv",
    BASE / "data" / "processed" / "cleaned_conflict_data.csv",
    BASE.parent / "data" / "cleaned_conflict_data.csv",
    BASE / "cleaned_conflict_data.csv",
]
DATA_PATH = next((p for p in CANDIDATES if p.exists()), None)
if DATA_PATH is None:
    raise FileNotFoundError(
        "cleaned_conflict_data.csv not found. Looked in:\n  "
        + "\n  ".join(str(p) for p in CANDIDATES)
    )

df = pd.read_csv(DATA_PATH)
df["WEEK"] = pd.to_datetime(df["WEEK"], format="%d-%B-%Y", errors="coerce")
if df["WEEK"].isna().all():  # fallback if the format ever differs
    df["WEEK"] = pd.to_datetime(df["WEEK"], errors="coerce")
for col in ["EVENTS", "FATALITIES", "POPULATION_EXPOSURE"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["WEEK", "COUNTRY", "EVENT_TYPE"]).copy()
df["YEAR"] = df["WEEK"].dt.year.astype(int)

ALL = "All"
REGIONS = sorted(df["REGION"].dropna().unique())
EVENT_TYPES = sorted(df["EVENT_TYPE"].dropna().unique())
YEAR_MIN, YEAR_MAX = int(df["YEAR"].min()), int(df["YEAR"].max())
TOTAL_RECORDS = len(df)

# ----------------------------------------------------------------------
# 2. Theme
# ----------------------------------------------------------------------
BG_TRANSPARENT = "rgba(0,0,0,0)"
TEXT = "#e6ecf8"
GRID = "#1d2d52"
PALETTE = ["#6c7bff", "#ff5c6c", "#2fd6a1", "#ffb44c", "#a56cff",
           "#35c4f0", "#ff8fd0", "#b6e880", "#f7e463", "#9aa7c7"]
HEAT = [[0, "#101c34"], [0.25, "#3a3f9e"], [0.55, "#a56cff"], [0.8, "#ff7a8a"], [1, "#ffd1a6"]]


def style(fig, height=420, legend=True):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        font=dict(family="Inter, Segoe UI, Arial", color=TEXT, size=12),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=legend,
        legend=dict(bgcolor=BG_TRANSPARENT, font=dict(size=11)),
        hoverlabel=dict(bgcolor="#101c34", bordercolor="#6c7bff", font_color=TEXT),
        colorway=PALETTE,
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    return fig


def empty_fig(msg="No data for the selected filters", height=420):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(size=15, color="#8fa1c4"))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return style(fig, height, legend=False)


# ----------------------------------------------------------------------
# 3. Layout helpers
# ----------------------------------------------------------------------
def kpi(card_id, label, color, sub_id):
    return html.Div(
        className="kpi",
        children=[
            html.Div(className="kpi-dot", style={"background": color, "boxShadow": f"0 0 12px {color}"}),
            html.Div(label, className="kpi-label"),
            html.Div(id=card_id, className="kpi-value", style={"color": color}),
            html.Div(id=sub_id, className="kpi-sub"),
        ],
    )


def chart_card(graph_id, title, note, wide=False, height=420):
    return html.Div(
        className="chart-card wide" if wide else "chart-card",
        children=[
            html.H3(title),
            html.P(note, className="note"),
            dcc.Graph(id=graph_id, config={"displaylogo": False}, style={"height": f"{height}px"}),
        ],
    )


def build_layout():
    return html.Div(
        className="app-shell",
        children=[
            html.Div(
                className="hero",
                children=[
                    html.Div([
                        html.H1("WAGIRMS"),
                        html.Div("Global Conflict Intelligence", className="tagline"),
                        html.P("Regional conflict patterns, event frequency and human impact",
                               className="desc"),
                    ]),
                    html.Div(className="hero-meta", children=[
                        html.Div("● ANALYTICS PLATFORM", className="live"),
                        html.Div(f"DATA PERIOD: {YEAR_MIN} – {YEAR_MAX}"),
                        html.Div(f"{TOTAL_RECORDS:,} RECORDS LOADED"),
                    ]),
                ],
            ),

            html.Div(
                className="panel",
                children=[
                    html.H2("Interactive Data Filters", className="panel-title"),
                    html.Div(className="filter-grid", children=[
                        html.Div([
                            html.Label("Region", className="filter-label"),
                            dcc.Dropdown(
                                id="region-filter",
                                options=[{"label": "All Regions", "value": ALL}]
                                        + [{"label": r, "value": r} for r in REGIONS],
                                value=ALL, clearable=False,
                            ),
                        ]),
                        html.Div([
                            html.Label("Countries", className="filter-label"),
                            dcc.Dropdown(id="country-filter", multi=True, placeholder="Select countries"),
                        ]),
                        html.Div([
                            html.Label("Event Category", className="filter-label"),
                            dcc.Dropdown(
                                id="event-filter",
                                options=[{"label": e, "value": e} for e in EVENT_TYPES],
                                value=EVENT_TYPES, multi=True, placeholder="Select categories",
                            ),
                        ]),
                    ]),
                    html.Div(style={"marginTop": "26px"}, children=[
                        html.Label("Year Range", className="filter-label"),
                        dcc.RangeSlider(
                            id="year-filter", min=YEAR_MIN, max=YEAR_MAX, step=1,
                            value=[YEAR_MIN, YEAR_MAX],
                            marks={y: str(y) for y in range(YEAR_MIN, YEAR_MAX + 1, 2)},
                            allowCross=False,
                        ),
                    ]),
                    html.Div(id="filter-status", className="filter-status"),
                ],
            ),

            html.Div(className="kpi-grid", children=[
                kpi("kpi-events", "Total Events", "#6c7bff", "kpi-events-sub"),
                kpi("kpi-fatal", "Total Fatalities", "#ff5c6c", "kpi-fatal-sub"),
                kpi("kpi-countries", "Countries Analysed", "#2fd6a1", "kpi-countries-sub"),
                kpi("kpi-cats", "Event Categories", "#a56cff", "kpi-cats-sub"),
                kpi("kpi-ratio", "Fatalities / Event", "#ffb44c", "kpi-ratio-sub"),
            ]),

            html.Div(className="chart-grid", children=[
                chart_card("fig-map", "Geographic Distribution",
                           "Admin-1 areas sized by fatalities, coloured by event count.", wide=True, height=520),
                chart_card("fig-top-countries", "Top Countries by Fatalities",
                           "Cumulative fatalities for the current selection."),
                chart_card("fig-event-type", "Fatalities by Event Type",
                           "Which categories cause the most human impact."),
                chart_card("fig-trend", "Yearly Fatality Trend",
                           "Top 5 countries in the current selection.", wide=True, height=440),
                chart_card("fig-events-year", "Yearly Events by Category",
                           "Frequency of events over time."),
                chart_card("fig-bubble", "Population Exposure vs Fatalities",
                           "Median record-level exposure; bubble size = total events."),
                chart_card("fig-heatmap", "Country × Event Type Heatmap",
                           "Darker/brighter cells = more fatalities."),
                chart_card("fig-treemap", "Event & Sub-Event Breakdown",
                           "Area is proportional to fatalities."),
            ]),

            html.Div(f"WAGIRMS Analytics • Source: {DATA_PATH.name} • Patterns describe the dataset and do not imply causation.",
                     className="footer"),
        ],
    )


# ----------------------------------------------------------------------
# 4. App
# ----------------------------------------------------------------------
app = Dash(__name__, title="WAGIRMS | Global Conflict Intelligence")
app.layout = build_layout()  # function-built so it never goes stale
server = app.server


def countries_for(region):
    sub = df if region in (None, ALL) else df[df["REGION"] == region]
    return sorted(sub["COUNTRY"].unique())


@app.callback(
    Output("country-filter", "options"),
    Output("country-filter", "value"),
    Input("region-filter", "value"),
)
def update_countries(region):
    c = countries_for(region)
    return [{"label": x, "value": x} for x in c], c


OUTPUTS = [
    Output("filter-status", "children"),
    Output("kpi-events", "children"), Output("kpi-events-sub", "children"),
    Output("kpi-fatal", "children"), Output("kpi-fatal-sub", "children"),
    Output("kpi-countries", "children"), Output("kpi-countries-sub", "children"),
    Output("kpi-cats", "children"), Output("kpi-cats-sub", "children"),
    Output("kpi-ratio", "children"), Output("kpi-ratio-sub", "children"),
    Output("fig-map", "figure"),
    Output("fig-top-countries", "figure"),
    Output("fig-event-type", "figure"),
    Output("fig-trend", "figure"),
    Output("fig-events-year", "figure"),
    Output("fig-bubble", "figure"),
    Output("fig-heatmap", "figure"),
    Output("fig-treemap", "figure"),
]


@app.callback(
    OUTPUTS,
    Input("region-filter", "value"),
    Input("country-filter", "value"),
    Input("event-filter", "value"),
    Input("year-filter", "value"),
)
def update_dashboard(region, countries, categories, years):
    y0, y1 = (years or [YEAR_MIN, YEAR_MAX])
    countries = countries or []
    categories = categories or []

    d = df[(df["YEAR"] >= y0) & (df["YEAR"] <= y1)
           & df["COUNTRY"].isin(countries) & df["EVENT_TYPE"].isin(categories)]
    if region not in (None, ALL):
        d = d[d["REGION"] == region]

    if d.empty:
        e = empty_fig()
        return (["No records match the current filters."]
                + ["0", "", "0", "", "0", "", "0", "", "0", ""] + [e] * 8)

    n_events = int(d["EVENTS"].sum())
    n_fatal = int(d["FATALITIES"].sum())
    n_countries = d["COUNTRY"].nunique()
    n_cats = d["EVENT_TYPE"].nunique()
    ratio = n_fatal / n_events if n_events else 0

    top_c = d.groupby("COUNTRY")["FATALITIES"].sum().idxmax()
    top_e = d.groupby("EVENT_TYPE")["FATALITIES"].sum().idxmax()
    peak_year = int(d.groupby("YEAR")["FATALITIES"].sum().idxmax())

    status = (f"Showing {len(d):,} records | {n_countries} countries | "
              f"{n_cats} event categories | Years {y0}–{y1}")

    # ---- Map -------------------------------------------------------
    geo = (d.groupby(["COUNTRY", "ADMIN1", "CENTROID_LATITUDE", "CENTROID_LONGITUDE"], as_index=False)
             .agg(EVENTS=("EVENTS", "sum"), FATALITIES=("FATALITIES", "sum")))
    geo = geo[(geo["EVENTS"] > 0)]
    fig_map = px.scatter_geo(
        geo, lat="CENTROID_LATITUDE", lon="CENTROID_LONGITUDE",
        size="FATALITIES", color="EVENTS", hover_name="ADMIN1",
        hover_data={"COUNTRY": True, "EVENTS": ":,", "FATALITIES": ":,",
                    "CENTROID_LATITUDE": False, "CENTROID_LONGITUDE": False},
        size_max=45, color_continuous_scale=HEAT, projection="natural earth",
    )
    fig_map.update_traces(marker=dict(line=dict(width=0.5, color="#0b1426"), opacity=0.82))
    fig_map.update_geos(
        bgcolor=BG_TRANSPARENT, showland=True, landcolor="#142347",
        showocean=True, oceancolor="#08101f", showcountries=True, countrycolor="#2c4175",
        showcoastlines=True, coastlinecolor="#2c4175", showframe=False, fitbounds="locations",
    )
    fig_map.update_layout(coloraxis_colorbar=dict(title="Events", thickness=12, len=0.7))
    style(fig_map, 520, legend=False)

    # ---- Top countries --------------------------------------------
    tc = (d.groupby("COUNTRY", as_index=False)["FATALITIES"].sum()
            .nlargest(10, "FATALITIES").sort_values("FATALITIES"))
    fig_tc = px.bar(tc, x="FATALITIES", y="COUNTRY", orientation="h", text="FATALITIES",
                    color="FATALITIES", color_continuous_scale=HEAT)
    fig_tc.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_tc.update_layout(coloraxis_showscale=False, xaxis_title="Total fatalities", yaxis_title=None)
    style(fig_tc, legend=False)

    # ---- Event type ------------------------------------------------
    et = (d.groupby("EVENT_TYPE", as_index=False)["FATALITIES"].sum().sort_values("FATALITIES"))
    fig_et = px.bar(et, x="FATALITIES", y="EVENT_TYPE", orientation="h", text="FATALITIES",
                    color="FATALITIES", color_continuous_scale=HEAT)
    fig_et.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    fig_et.update_layout(coloraxis_showscale=False, xaxis_title="Total fatalities", yaxis_title=None)
    style(fig_et, legend=False)

    # ---- Yearly trend (top 5 countries) ----------------------------
    top5 = d.groupby("COUNTRY")["FATALITIES"].sum().nlargest(5).index
    yt = (d[d["COUNTRY"].isin(top5)].groupby(["YEAR", "COUNTRY"], as_index=False)["FATALITIES"].sum())
    fig_tr = px.line(yt, x="YEAR", y="FATALITIES", color="COUNTRY", markers=True)
    fig_tr.update_traces(line=dict(width=3), marker=dict(size=7))
    fig_tr.update_layout(hovermode="x unified", xaxis_title=None, yaxis_title="Total fatalities",
                         xaxis=dict(dtick=1), legend_title_text="")
    style(fig_tr, 440)

    # ---- Events per year by category ------------------------------
    ey = d.groupby(["YEAR", "EVENT_TYPE"], as_index=False)["EVENTS"].sum()
    fig_ey = px.bar(ey, x="YEAR", y="EVENTS", color="EVENT_TYPE", barmode="stack")
    fig_ey.update_layout(xaxis_title=None, yaxis_title="Events", legend_title_text="",
                         legend=dict(orientation="h", y=-0.2), xaxis=dict(dtick=1))
    style(fig_ey)

    # ---- Bubble ----------------------------------------------------
    bub = (d.groupby("COUNTRY", as_index=False)
             .agg(EVENTS=("EVENTS", "sum"), FATALITIES=("FATALITIES", "sum"),
                  EXPOSURE=("POPULATION_EXPOSURE", "median")))
    bub = bub.nlargest(10, "FATALITIES")
    fig_b = px.scatter(bub, x="EXPOSURE", y="FATALITIES", size="EVENTS", color="COUNTRY",
                       text="COUNTRY", size_max=55,
                       labels={"EXPOSURE": "Median population exposure", "FATALITIES": "Total fatalities"})
    fig_b.update_traces(textposition="top center", marker=dict(opacity=0.85, line=dict(width=1, color="#0b1426")))
    style(fig_b, legend=False)

    # ---- Heatmap ---------------------------------------------------
    top10 = d.groupby("COUNTRY")["FATALITIES"].sum().nlargest(10).index
    hm = (d[d["COUNTRY"].isin(top10)].pivot_table(index="COUNTRY", columns="EVENT_TYPE",
                                                   values="FATALITIES", aggfunc="sum", fill_value=0)
            .loc[list(top10)])
    fig_h = px.imshow(hm, text_auto=".2s", aspect="auto", color_continuous_scale=HEAT)
    fig_h.update_layout(xaxis_title=None, yaxis_title=None, coloraxis_colorbar=dict(title="", thickness=10))
    fig_h.update_xaxes(tickangle=-30)
    style(fig_h, legend=False)

    # ---- Treemap ---------------------------------------------------
    tm = (d.groupby(["EVENT_TYPE", "SUB_EVENT_TYPE"], as_index=False)["FATALITIES"].sum())
    tm = tm[tm["FATALITIES"] > 0]
    if tm.empty:
        fig_t = empty_fig("No fatalities in selection")
    else:
        fig_t = px.treemap(tm, path=["EVENT_TYPE", "SUB_EVENT_TYPE"], values="FATALITIES",
                           color="FATALITIES", color_continuous_scale=HEAT)
        fig_t.update_traces(marker=dict(line=dict(color="#0b1426", width=2)),
                            textfont=dict(color="#fff"))
        fig_t.update_layout(coloraxis_showscale=False)
        style(fig_t, legend=False)

    return (
        status,
        f"{n_events:,}", f"Most affected: {top_c}",
        f"{n_fatal:,}", f"Deadliest category: {top_e}",
        f"{n_countries}", f"Years {y0}–{y1}",
        f"{n_cats}", f"Peak year: {peak_year}",
        f"{ratio:.2f}", "Average deaths per recorded event",
        fig_map, fig_tc, fig_et, fig_tr, fig_ey, fig_b, fig_h, fig_t,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8050)