from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pd_manipulation as pm
import numpy as np


def get_xy(country):
    """
    querys db returns x int date values and corresponding dollar price y values from
    desired country and the local price values and corresponding currency code
    :return: three lists xd:  x int dates, yp: y dollar prices , zp: z local prices,and c country code
    """

    data = pm.get_pairs(country)
    xd = data[0]
    yp = data[1]
    zp = data[2]
    cc = data[3]
    return xd, yp, zp, cc  # returning x dates, y usd prices, z local prices, and c currency code to be graphed


def get_avgxy():
    """
    querys db returns x int date values and corresponding average dollar price y values from
    each date
    :return: two lists xd:  x int dates, yp: y dollar prices
    """
    df = pm.set_pd()  # using pandas manipulationt to set pd
    avgp = pm.get_means(df)
    unique_dates = df["date"].unique()
    xd = [i for i in unique_dates]
    return xd, avgp


def graph_avg(x, y):
    """
    :param x: int date values (list)
    :param y: avg dollar prices (list)
    :return: plots a scatter plot of average world Big Mac Prices over time
    """
    fig = Figure()  # instantiating fig obj
    years = [i for i in range(23)]  # list of years on x axis
    xtick = list(range(0, 8395, 365))  # xtick will cordinate where x values are placed
    ax = fig.add_subplot(1, 1, 1)  # adding subplots

    ax.plot(x, y, color="orange", label="Average Big Mac Prices over time", alpha=.5)  # plotting line
    ax.scatter(x, y, color="orange", alpha=.5)  # plotting individual points
    ax.set(title="World Average Big Mac Prices (USD) since 2000", xlabel="Years Since 2000",
           ylabel="Price(Dollars)")  # setting title and x and yaxis labels
    ax.xaxis.set_ticks(xtick)  # setting x ticks
    ax.xaxis.set_ticklabels(years)  # setting months labels
    ax.legend()  # creating legend allowing user to understand graph better

    # showing graphs

    fig.tight_layout()  # reformatting layout to add space between two graphs
    # plt.show()   showing graphs
    return fig  # returning fig obj will be saved and rendered in html template


def graph_data(x, y, z, country, currency_code):
    """
    :param currency_code : str currency code for country (str)
    :param x: int date values (list)
    :param y: dollar prices (list)
    :param z: local prices (list)
    :param country: country name(str)
    :param country_code: str
    :return: plots a scatter plot showing change in price of big macs over time

    """
    fig = Figure()  # instantiating figure object
    years = [i for i in range(23)]  # years list for x axis
    xtick = list(range(0, 8395, 365))  # xtick will cordinate where x values are placed
    ax = fig.add_subplot(2, 1, 1)  # adding subplots we are plotting this one on top
    # creating 2 plots, 2 rows 1 column

    ax.plot(x, y, color="blue", label="Big Mac Prices over time", alpha=.5)  # plotting line for locale
    ax.scatter(x, y, color="blue", alpha=.5)  # plotting specific points on the line

    ax.set(title=str(country) + " Big Mac Prices (USD) since 2000", xlabel="Years Since 2000",
           ylabel="Price(USD)")  # setting title and x and yaxis labels
    ax.xaxis.set_ticks(xtick)  # setting x ticks
    ax.xaxis.set_ticklabels(years)  # setting months labels
    ax.legend()  # creating legend allowing user to understand graph better

    # showing graphs
    ax = fig.add_subplot(2, 1, 2)  # adding subplots we are plotting this one below the USD prices graph
    ax.plot(x, z, color="red", label="Big Mac Prices over time", alpha=.5)  # plotting line for locale
    ax.scatter(x, z, color="red", alpha=.5)  # plotting specific points on the line

    ax.set(title=str(country) + " Big Mac Prices (" + str(currency_code) + ") since 2000", xlabel="Years since 2000",
           ylabel="Price(" + str(currency_code) + ")")  # setting labels
    # ax.set(title=str(country) + " local Big Mac Prices since 2000", xlabel="Years since 2000", ylabel="local price")
    ax.xaxis.set_ticks(xtick)  # setting x ticks
    ax.xaxis.set_ticklabels(years)  # setting months labels
    ax.legend()  # creating legend allowing user to understand graph better

    fig.tight_layout()  # reformatting layout to add space between two graphs
    # showing graphs
    return fig  # returning fig obj will be saved and rendered in html template


def graph_LR(country, xd, yp):
    x_train, x_test, y_train, y_test = train_test_split(xd, yp)
    fig = Figure()
    years = [i for i in range(23)]  # list of years on x axis
    xtick = list(range(0, 8395, 365))  # xtick will cordinate where x values are placed
    ax = fig.add_subplot(1, 1, 1)  # adding subplots

    ax.scatter(xd, yp, color="red", label="Train Data", alpha=.7)  # plotting line
    # ax.scatter(x_test, y_test, color="red", alpha=.7)  # plotting individual points
    ax.set(title="Regressed " + country + " Big Mac Prices(USD) Since 2000", xlabel="Years Since 2000",
           ylabel="Price(USD)", label="test data")  # setting title and x and yaxis labels

    ax.xaxis.set_ticks(xtick)  # setting x ticks
    ax.xaxis.set_ticklabels(years)  # setting months labels

    LR = LinearRegression()
    LR.fit(x_train.values.reshape(-1, 1), y_train.values)
    prediction = LR.predict(x_test.values.reshape(-1, 1))
    ax.scatter(x_test, prediction, label="Actual Test Data", color='g', alpha=.7)
    ax.plot(x_test, prediction, label="Linear Regression", color='b')
    ax.legend()
    return fig


def predict_price(xd, yp, prediction):
    x_train, x_test, y_train, y_test = train_test_split(xd, yp)
    LR = LinearRegression()
    LR.fit(x_train.values.reshape(-1, 1), y_train.values)
    predict_val = LR.predict(np.array([[prediction]]))
    return predict_val


def get_score(xd, yp):
    x_train, x_test, y_train, y_test = train_test_split(xd, yp)
    LR = LinearRegression()
    LR.fit(x_train.values.reshape(-1, 1), y_train.values)
    score = LR.score(x_test.values.reshape(-1, 1), y_test.values)
    return score


def main():  # main
    pass
    #get_avgxy()
    # ['Argentina', 'Australia', 'Brazil', 'Britain', 'Canada', 'Chile', 'China',
    # 'Czech Republic', 'Euro area', 'Hong Kong', 'Hungary', 'Indonesia', 'Japan',
    # 'Malaysia', 'Mexico', 'New Zealand', 'Poland', 'Singapore', 'South Africa',
    # 'South Korea', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'United States
    # print(pm.get_lr_countries())
    # data = pm.get_lr_pairs("United States")
    # x, y = data[0], data[1]
    ##graph_LR("US", x, y)
    # z = predict_price(x, y,2800)
    # print(z[1])

    # --UNIT TEST--
    # data = get_xy("United States")
    # x, y, z , c = data[0], data[1], data[2], data[3]
    # print(x)
    # print(y)
    # print(c)
    # print(graph_data(x, y, z, "peen", c))

    # data_avg = get_avgxy()
    # x, y = data_avg[0], data_avg[1]
    # print(graph_avg(x, y))


if __name__ == '__main__':  # if name main calling main function
    pass  # main
