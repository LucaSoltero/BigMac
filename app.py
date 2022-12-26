import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import graph as gd
import pd_manipulation as pm
import io
import json
from datetime import datetime


def get_locales():
    """
    obtains unique countries from pandas df
    :return: a list of countries that users can obtain data about
    """
    df = pm.set_pd()
    countries = df["name"].unique()
    countries.sort()
    countries_list = [i for i in countries]
    countries_list.remove(
        "United Arab Emirates")  # removing United Arab Emirates because there is already data on it via UAE (it is redundant)
    return countries_list


def create_spec_figure(locale):
    """
    gets date, dollar p, local p , and currency code of locale
    :param locale: country user would like to visualize data on
    :return: image fig object
    """
    # gd.getxy() returns 4 lists containing int data values (x) for that country
    # y list of USD prices of Big Macs
    # z list of prices in local currency
    # c string currency code for that specific country
    data = gd.get_xy(locale)
    x, y, z, cc = data[0], data[1], data[2], data[3]  # getting list values
    return gd.graph_data(x, y, z, locale, cc)  # return gd.graph data to vizualize the data requested by the user


def create_avg_figure():
    """
    visualzes data on average big mac prices across all countries over the last 22 years
    :return: image fig object
    """
    # gd.get_avgxy() returns 2 lists containing int data values (x) for that country
    # y list of average big mac prices across all countries in USD
    data_avg = gd.get_avgxy()
    x, y = data_avg[0], data_avg[1]
    return gd.graph_avg(x, y)  # return gd.graph data to visualize the data requested by the user


def create_regr_figure(locale):
    data = pm.get_np_pairs(locale)
    x, y = data[0], data[1]
    return gd.graph_LR(locale, x, y)


def predict_price(locale, prediction):
    data = pm.get_np_pairs(locale)
    x, y = data[0], data[1]
    return gd.predict_price(x, y, prediction)


def score(locale):
    data = pm.get_np_pairs(locale)
    x, y = data[0], data[1]
    return gd.get_score(x, y)


def fig(locale):
    """
    :param locale: str locale of data requested ( a country )
    :param data_request: dictionary key of data type requested either average data or data by country
    :return: Either visualized data png on the selected locale or visualised data png on average price data across all contries
    """
    # if data request is DBC then return a png image of the data for the selected locale

    # print("here")
    fig = create_spec_figure(locale)  # calls create spec figure to return the vizualzed data image for that locale
    img = io.BytesIO()  # instantiating image object
    fig.savefig(img, format='png')  # saving image in png format
    img.seek(0)  # obtaining the 0th index to return img type
    return img


def avg_fig():
    fig = create_avg_figure()  # calls create avg figure to return the vizualzed data image
    img = io.BytesIO()  # instantiating image object
    fig.savefig(img, format='png')  # saving image in png format
    img.seek(0)  # obtaining the 0th index to return img type
    return img


def regress_fig(locale):
    fig = create_regr_figure(locale)  # calls create spec figure to return the vizualzed data image for that locale
    img = io.BytesIO()  # instantiating image object
    fig.savefig(img, format='png')  # saving image in png format
    img.seek(0)  # obtaining the 0th index to return img type
    return img


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# CONFIGS
page_title = "Big Mac Price Data"
page_icon = ":hamburger:"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")
data_selected = ["DBC", "PREDICT"]

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

# NAV BAR (Temp)
with st.sidebar:
    selected = option_menu(menu_title="Menu",
                           options=["Welcome", "Data by Country", "Average Price Data", "Regression Model"])

if selected == "Welcome":
    st.markdown("<h1 style='text-align: center; color: black;'>Big Mac Price Data &#x1F354;</h1>",
                unsafe_allow_html=True)
    anime = load_lottiefile("burger.json")
    st_lottie(anime, height=300, loop=False)
    st.markdown(
        '<p style="text-align: center;">The comparison in cost of Big Macs between nations has been used in the past to measure '
        'whether market exchange rates for different countries currencies are either over or undervalued. '
        'In 1986 The Economist coined the term "Big Mac Price Index" as a simple guide to examine the state of a nations '
        'currency, basing itself on the Macroeconomic Theory of Purchasing Power Parity. This web app visualizes data about '
        'Big Mac Prices from 73 countries worldwide and shows international economic trends like inflation and disparities '
        'in consumer purchasing power between nations.'
        '</p>', unsafe_allow_html=True)

if selected == "Data by Country":
    st.header("Data By Country " + page_icon)
    with st.form(data_selected[0]):
        country = st.selectbox("Select a Country", get_locales())
        submit_dbc = st.form_submit_button("Visualize Data")
        if submit_dbc:
            st.image(fig(country))

if selected == "Average Price Data":
    st.header("Worldwide Average Big Mac Price Data :hamburger:")
    st.image(avg_fig())


if selected == "Regression Model":
    st.header("Simple Linear Regression Model :hamburger:")
    with st.form(data_selected[1], clear_on_submit=False):
        lr_country = st.selectbox("Select a Country", pm.get_lr_countries())
        submit_lr = st.form_submit_button("Visualize Regressed Data")
        if submit_lr:
            st.image(regress_fig(lr_country))
            Rsqr = str(score(lr_country))
            st.write("This regression has a coefficient of determination equal to " + Rsqr)

        p_prediction = st.text_input("Submit prediction in year-month-date format ex: \'2023-01-01\'", "2023-01-01",
                                     key="PREDICTION")
        submit_prediction = st.form_submit_button("Get Prediction")
        if submit_prediction:
            prediction = str(st.session_state["PREDICTION"]).strip()
            cn = []
            for i in prediction:
                if i.isnumeric():
                    cn.append(1)
                elif i == '-':
                    cn.append(0)
                else:
                    pass
            if cn == [1, 1, 1, 1, 0, 1, 1, 0, 1, 1]:
                int_date = (datetime.strptime(prediction, '%Y-%m-%d') - datetime(2000, 1, 1)).days
                predicted_value = str(predict_price(lr_country, int_date))
                c = predicted_value.replace("[", "")
                d = c.replace("]", "")
                st.write("The predicted price for this date is  ", d, "USD !")
            else:
                st.write("Please enter a date in the valid format")