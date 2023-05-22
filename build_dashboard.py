import streamlit as st
import pandas as pd
import numpy as np
from streamlit import session_state as ss
import streamlit_toggle as tog
import plotly.express as px


st.set_page_config(page_title="Sydney Sold Properties Analysis", layout="wide")


@st.cache_data
def read_data(file_path):
    df = pd.read_csv(file_path, compression='zip')
    df = df.iloc[:3000]
    for i in ["bedrooms", "bathrooms", "parking_spaces"]:
        df[i] = df[i].replace(np.nan, -1, regex=True)
    df["sold_date"] = pd.to_datetime(df["sold_date"])
    return df


all_filters = ["suburb", "postcode", "property_type", "property_type_detail", "bedrooms", "bathrooms", "parking_spaces"]
data_path = r"C:\Users\raymo\PycharmProjects\PropertyPriceScraper\ALL_SOLD.zip"
data = read_data(data_path)
# st.dataframe(data)


def on_filter_change(user_filter, all_filters, data):
    ss["most_recently_changed"] = user_filter
    remaining_filters = [i for i in all_filters if len(ss[i]) != 0]
    # Configure default selections (want to filter to relevant values only)
    selected = dict()
    available = dict()
    for i in all_filters:
        ss[f"{i}_default_selections"] = None
    for i in remaining_filters:
        selected[i] = ss[i]
        # if np.isnan(ss[user_filter]).any():
        #     available[i] = data.loc[data[user_filter].isin(ss[user_filter]) | data[user_filter].isnull(), i].unique()
        # else:
        #     available[i] = data.loc[data[user_filter].isin(ss[user_filter]), i].unique() # Think i need to fix this
        available[i] = data.loc[data[user_filter].isin(ss[user_filter]), i].unique()

        if len(ss[user_filter]) == 0:
            ss[f"{i}_default_selections"] = ss[i]
        else:

            ss[f"{i}_default_selections"] = [k for k in selected[i] if k in available[i]]
            # st.write(f"{selected[i]}")
            # st.write(f"{available[i]}")
            # if (np.isnan(selected[i]).any()) and (np.isnan(available[i]).any()):
            #     ss[f"{i}_default_selections"].append(np.nan)


    # Configure dropdown options (for dynamic filtering)
    for i in all_filters:
        other_active_filters = [j for j in all_filters if (i != j) and (len(ss[j]) != 0)]
        filtered_data_temp = data.copy()
        for k in other_active_filters:
            # if np.isnan(ss[f"{k}_default_selections"]).any():
            #     filtered_data_temp = filtered_data_temp.loc[filtered_data_temp[k].isin(ss[f"{k}_default_selections"]) | filtered_data_temp[k].isnull()]
            # else:
            #     filtered_data_temp = filtered_data_temp.loc[filtered_data_temp[k].isin(ss[f"{k}_default_selections"])]
            filtered_data_temp = filtered_data_temp.loc[filtered_data_temp[k].isin(ss[f"{k}_default_selections"])]

        ss[f"{i}_options"] = np.sort(filtered_data_temp[i].unique())



# ----SIDEBAR---
st.sidebar.caption("Select nothing to apply no filter. For numeric filters, a value of -1 implies an NA entry for that property.")
with st.sidebar:
    col1, col2 = st.columns([4.8,1])
    with col1:
        st.caption("**Dynamic Filtering** - Switch on (recommended) for only relevant options to be displayed for each filter based on other selected filters")
    with col2:
        dynamic_filter_toggle = tog.st_toggle_switch(default_value=True, key="dynamic_filter_toggle", inactive_color='#D3D3D3', active_color="#11567f", track_color="#29B5E8")
st.sidebar.header("Global Filters:")

for i in all_filters:
    if f"{i}_options" not in ss:
        ss[f"{i}_options"] = np.sort(data[i].unique())
    # if i not in ss:
    #     ss[i] = ss[f"{i}_options"].copy()
    if f"{i}_default_selections" not in ss:
        ss[f"{i}_default_selections"] = None

if "most_recently_changed" not in ss:
    ss["most_recently_changed"] = None
if "dynamic_filter_tracker" not in ss:
    ss["dynamic_filter_tracker"] = [True, True]

filter_buttons = st.sidebar.columns(2, gap="small")
with filter_buttons[0]:
    clear_filters = st.button(label="Reset filters",
                              help="Clear all filters (return to no selection)")
with filter_buttons[-1]:
    fill_filters = st.button(label="Fill all filters",
                              help="Fill all filters.\n\n Based on most recent selection of filters.\n\n The most recent filter is left unchanged.")

ss["dynamic_filter_tracker"] = (ss["dynamic_filter_tracker"] + [dynamic_filter_toggle])[-2:]
if clear_filters or (not(ss["dynamic_filter_tracker"][-2]) and ss["dynamic_filter_tracker"][-1]):
    for i in all_filters:
        ss[f"{i}_options"] = np.sort(data[i].unique())
        ss[f"{i}_default_selections"] = None
    if not(ss["dynamic_filter_toggle"] or ss["dynamic_filter_toggle"] is None):
        for i in all_filters:
            ss[i] = []

if fill_filters:
    for i in all_filters:
        if i != ss["most_recently_changed"]:
            ss[f"{i}_default_selections"] = ss[f"{i}_options"]
        else:
            ss[f"{i}_options"] = ss[i]

if ss["dynamic_filter_toggle"] or ss["dynamic_filter_toggle"] is None:
    on_change_function = on_filter_change
else:
    on_change_function = None
    for i in all_filters:
        ss[f"{i}_options"] = np.sort(data[i].unique())

suburb_select = st.sidebar.multiselect(label="Select the Suburb(s):",
                                       options=ss["suburb_options"],
                                       on_change=on_change_function,
                                       args=("suburb", all_filters, data),
                                       default=ss["suburb_default_selections"],
                                       key="suburb")

postcode_select = st.sidebar.multiselect(label="Select the Postcode(s):",
                                         options=ss["postcode_options"],
                                         on_change=on_change_function,
                                         args=("postcode", all_filters, data),
                                         default=ss["postcode_default_selections"],
                                         key="postcode")
property_type_select = st.sidebar.multiselect(label="Select the Property Type(s):",
                                              options=ss["property_type_options"],
                                              on_change=on_change_function,
                                              args=("property_type", all_filters, data),
                                              default=ss["property_type_default_selections"],
                                              key="property_type",
                                              help="This is a more general filter for Property Type")
property_type_detail_select = st.sidebar.multiselect(label="Select the Property Type(s) (Detailed):",
                                              options=ss["property_type_detail_options"],
                                              on_change=on_change_function,
                                              args=("property_type_detail", all_filters, data),
                                              default=ss["property_type_detail_default_selections"],
                                              key="property_type_detail",
                                              help="This is a detailed filter for Property Type. For example, Property Type=House can be further classified as house or duplex")
bedrooms_select = st.sidebar.multiselect(label="Select the Number of Bedroom(s):",
                                              options=ss["bedrooms_options"],
                                              on_change=on_change_function,
                                              args=("bedrooms", all_filters, data),
                                              default=ss["bedrooms_default_selections"],
                                              key="bedrooms")
bathrooms_select = st.sidebar.multiselect(label="Select the Number of Bathroom(s):",
                                              options=ss["bathrooms_options"],
                                              on_change=on_change_function,
                                              args=("bathrooms", all_filters, data),
                                              default=ss["bathrooms_default_selections"],
                                              key="bathrooms")
parking_spaces_select = st.sidebar.multiselect(label="Select the Number of Parking Space(s):",
                                              options=ss["parking_spaces_options"],
                                              on_change=on_change_function,
                                              args=("parking_spaces", all_filters, data),
                                              default=ss["parking_spaces_default_selections"],
                                              key="parking_spaces")


# st.write(st.session_state)


active_filters = [i for i in all_filters if len(ss[i]) != 0]
query_string = ""
for i in range(len(active_filters)):
    if i == 0:
        query_string = query_string + f"{active_filters[i]} == @{active_filters[i]}_select"
    else:
        query_string = query_string + " & " + f"{active_filters[i]} == @{active_filters[i]}_select"

if query_string == "":
    df_selection = data
else:
    df_selection = data.query(query_string)
# st.dataframe(df_selection)

aggregate_option_selection = st.columns(2, gap="medium")
with aggregate_option_selection[0]:
    aggregate_option_level = st.selectbox("Select the level of Aggregation for Time Distribution Plots",
                                    ("Daily", "Monthly", "Quarterly", "Half-Yearly", "Annually"))
with aggregate_option_selection[-1]:
    aggregate_option_type = st.selectbox("Select the type of Aggregation for Time Distribution Plots",
                                    ("Mean", "Median", "Mode", "Min", "Max"))
import datetime as dt
factor_option_level = st.selectbox("Select the factor to compare by in Time Distribution Plots (Factor Views)", all_filters)
time_select = st.slider(label="Select time range for Time Distribution Plots", min_value=dt.date(year=2021,month=1,day=1), max_value=dt.datetime.now().date(), value=[dt.date(year=2021,month=1,day=1), dt.datetime.now().date()], format='MMM DD, YYYY')

st.divider()

if aggregate_option_level == "Monthly":
    df_selection["sold_month"] = df_selection["sold_date"].dt.strftime('%Y') + df_selection["sold_date"].dt.strftime('%m')
elif aggregate_option_level == "Quarterly":
    df_selection["sold_quarter"] = pd.PeriodIndex(df_selection["sold_date"], freq='Q').astype(str)
elif aggregate_option_level == "Half-Yearly":
    df_selection["sold_half_year"] = df_selection["sold_date"].dt.strftime('%Y') + np.where(df_selection["sold_date"].dt.month.le(6), 'H1', 'H2').astype(str)
elif aggregate_option_level == "Annually":
    df_selection["sold_year"] = df_selection["sold_date"].dt.strftime('%Y')

aggregate_level_map = {"Daily": "sold_date", "Monthly": "sold_month", "Quarterly": "sold_quarter", "Half-Yearly": "sold_half_year", "Annually": "sold_year"}
aggregate_option_map = {"Mean": "mean_price", "Median": "median_price", "Mode": "mode_price", "Min": "min_price", "Max": "max_price"}

def aggregate_type_map(df, type):
    df = df.reset_index(drop=True)
    if type == "Mean":
        return pd.DataFrame({"mean_price": [df["price"].mean()], "count": [df["price"].count()]})
    elif type == "Median":
        return pd.DataFrame({aggregate_level_map[aggregate_option_level]: df[aggregate_level_map[aggregate_option_level]][[0]], "median_price":  df["price"].median(), "count": df["price"].count()})
    elif type == "Mode":
        return pd.DataFrame({aggregate_level_map[aggregate_option_level]: df[aggregate_level_map[aggregate_option_level]][[0]], "mode_price":  df["price"].mode(), "count": df["price"].count()})
    elif type == "Min":
        return pd.DataFrame({aggregate_level_map[aggregate_option_level]: df[aggregate_level_map[aggregate_option_level]][[0]], "min_price":  df["price"].min(), "count": df["price"].count()})
    elif type == "Max":
        return pd.DataFrame({aggregate_level_map[aggregate_option_level]: df[aggregate_level_map[aggregate_option_level]][[0]], "max_price":  df["price"].max(), "count": df["price"].count()})

# def comparison_assist(chosen_factor):

# aggregate_by_date = df_selection.groupby(by=[aggregate_level_map[aggregate_option_level]] + active_filters)["price"].apply(aggregate_type_map, aggregate_option_type).reset_index(drop=False)
aggregate_by_date = df_selection[[aggregate_level_map[aggregate_option_level], "price"]].groupby(by=[aggregate_level_map[aggregate_option_level]]).apply(aggregate_type_map, aggregate_option_type).reset_index(drop=False)
aggregate_fig = px.line(aggregate_by_date, x=aggregate_level_map[aggregate_option_level], y=aggregate_option_map[aggregate_option_type], title=f"<span style='color:#8A3CC4'>{aggregate_option_level}</span> Sales Price Time Distribution (<span style='color:#8A3CC4'>{aggregate_option_type}</span>) - Aggregate View", template="plotly_white")
st.plotly_chart(aggregate_fig, use_container_width=True)

# st.divider()

factor_by_date = df_selection[[aggregate_level_map[aggregate_option_level], "price"] + [factor_option_level]].groupby(by=[aggregate_level_map[aggregate_option_level]] + [factor_option_level]).apply(aggregate_type_map, aggregate_option_type).reset_index(drop=False)
if aggregate_level_map[aggregate_option_level] in ["sold_date", "sold_month", "sold_year"]:
    factor_by_date["sort_date"] = pd.to_numeric(factor_by_date[aggregate_level_map[aggregate_option_level]], errors="coerce")
elif aggregate_level_map[aggregate_option_level] == "sold_half_year":
    factor_by_date["year"] = factor_by_date["sold_half_year"].str[:4]
    factor_by_date["half_year"] = factor_by_date["sold_half_year"].str[-1]
    factor_by_date["sort_date"] = pd.to_numeric(factor_by_date["year"] + factor_by_date["half_year"], errors="coerce")
elif aggregate_level_map[aggregate_option_level] == "sold_quarter":
    factor_by_date["year"] = factor_by_date["sold_quarter"].str[:4]
    factor_by_date["quarter"] = factor_by_date["sold_quarter"].str[-1]
    factor_by_date["sort_date"] = pd.to_numeric(factor_by_date["year"] + factor_by_date["quarter"], errors="coerce")
factor_by_date = factor_by_date.sort_values(by=[factor_option_level, "sort_date"]).reset_index(drop=True)

factor_fig = px.line(factor_by_date, x=aggregate_level_map[aggregate_option_level], y=aggregate_option_map[aggregate_option_type],
                     color=factor_option_level, category_orders={aggregate_level_map[aggregate_option_level]: factor_by_date.sort_values(by=["sort_date"])[aggregate_level_map[aggregate_option_level]].unique()},
                     title=f"<span style='color:#8A3CC4'>{aggregate_option_level}</span> Sales Price Time Distribution (<span style='color:#8A3CC4'>{aggregate_option_type}</span>) - Factor View",
                     template="plotly_white")

factor_fig.update_layout(legend=dict(orientation="h", y=-0.22))
st.plotly_chart(factor_fig, use_container_width=True)
st.divider()

aggregate_fig_bar = px.bar(aggregate_by_date, x=aggregate_level_map[aggregate_option_level], y="count", category_orders={aggregate_level_map[aggregate_option_level]: factor_by_date.sort_values(by=["sort_date"])[aggregate_level_map[aggregate_option_level]].unique()},
                     title=f"<span style='color:#8A3CC4'>{aggregate_option_level}</span> Sales Volume Time Distribution - Aggregate View",
                     template="plotly_white")
aggregate_fig_bar.update_layout(legend=dict(orientation="h", y=-0.22))
st.plotly_chart(aggregate_fig_bar, use_container_width=True)
st.caption("Zoom in, or set aggregation level to a more broad selection to see bar chart better.")

factor_fig_bar = px.bar(factor_by_date, x=aggregate_level_map[aggregate_option_level], y="count", color=factor_option_level, category_orders={aggregate_level_map[aggregate_option_level]: factor_by_date.sort_values(by=["sort_date"])[aggregate_level_map[aggregate_option_level]].unique()},
                     title=f"<span style='color:#8A3CC4'>{aggregate_option_level}</span> Sales Volume Time Distribution - Factor View",
                     template="plotly_white")
factor_fig_bar.update_layout(legend=dict(orientation="h", y=-0.22))
st.plotly_chart(factor_fig_bar, use_container_width=True)
st.caption("Zoom in, or set aggregation level to a more broad selection to see bar chart better.")
st.divider()

