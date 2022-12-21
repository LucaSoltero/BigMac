import pandas as pd  # importing pandas for data manipulation/ aggregation
from datetime import datetime
from statistics import mean  # from statistics package importing mean to calc means
from Oooosecrets import load_creds

filename = load_creds.filename
def set_pd():
    """
    function: cleans csv file and creates new columns using pandas
    sets pandas df and returns new df
    :param filename:
    :return: updates pd dataframe
    """
    df = pd.read_csv(filename)
    df = df[df["dollar_price"].notnull()]  # getting rid of null values
    df = df[df["local_price"].notnull()]  # getting rid of null values
    df = df[df["date"].notnull()]  # getting rid of null dates
    df["YEAR"] = df["date"].str[0:4]  # adding date column
    df["MONTH_DAY"] = df["date"].str[-5:]  # creating month_day column
    df["date"] = df["date"].apply((lambda x: (datetime.strptime(x, '%Y-%m-%d') - datetime(2000, 1, 1)).days))
    df.sort_values(inplace=True, by='date')  # sorting by date
    return df  # return set df


def calc_means(df, date):
    """
    function: calculates the mean price at a specific date measured across all countries
    :param df: pandas dataframe
    :param date: date at which mean price is to be calculated across for all countries
    :return: the mean price measured in USD across all countries at that specific date of measuring
    """
    grouped_dates = df.groupby("date")  # groups data by month day
    date_prices = grouped_dates["dollar_price"]  # getting dollar price column
    spec_date_prices = date_prices.get_group(date)  # getting dates of each price
    data_per_date_list = [d for d in spec_date_prices]  # getting data per every date
    return mean(data_per_date_list)  # obtaining the mean usd price for a big mac at each data across all countries


def get_means(df):
    """
    function: iterates through unique dates, calculates averages at each date and adds it to a list
    :param df: pandas dataframe
    :return: returns a list of the mean prices measured in USD across all countries at that specific date of measuring
    """

    unique_dates = df["date"].unique()  # getting unique month day dates
    avg_prices = []  # instantiating empty list to hold avg temperature for all years
    for date in unique_dates:  # iterating through unique dates
        avg_prices.append(calc_means(df, date))  # appending prices to list
    return avg_prices  # returning avg price list


def get_lr_countries():
    df = set_pd()
    c = df.groupby("name")
    dates = c["date"]
    countries = df["name"].unique()
    countries.sort()

    lr_countries = []
    for i in countries:
        # print(i)
        xd = dates.get_group(i)
        if len(xd) == 37:
            lr_countries.append(i)
    return lr_countries


def get_pairs(locale):
    df = set_pd()
    c = df.groupby("name")
    dollar_price = c["dollar_price"]
    dates = c["date"]
    local_price = c["local_price"]
    currency_code = c["currency_code"]
    dollar_ex = c["dollar_ex"]

    x_dates = dates.get_group(locale)
    y_prices = dollar_price.get_group(locale)
    local_p = local_price.get_group(locale)
    curr_code = currency_code.get_group(locale)
    mac_index = dollar_ex.get_group(locale)

    xd = [i for i in x_dates]
    yp = [p for p in y_prices]
    lp = [l for l in local_p]
    cc = [c for c in curr_code]
    return xd, yp, lp, cc[0]


def get_np_pairs(locale):
    df = set_pd()
    c = df.groupby("name")
    dollar_price = c["dollar_price"]
    dates = c["date"]
    xd = dates.get_group(locale)
    yp = dollar_price.get_group(locale)
    return xd, yp




def main():
    pass


if __name__ == '__main__':
    pass
