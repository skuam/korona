import datetime

import pandas as pd

from . import models


def daily_report(date_string=None):
    # dating as far back to 01-22-2020
    # date formatting '%m-%d-%Y'
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else:
        file_date = date_string
    df = pd.read_csv(report_directory + file_date + '.csv')
    return df


# dailly updates
# add check to update only if there is not done so already
def Update_Day(Country_selected="Poland"):
    #chceck for last date in databse, assume
    d = models.Country.objects.latest("Date").Date
    today = datetime.date.today().strftime('%m-%d-%Y')
    for single_date in pd.date_range(d+datetime.timedelta(days=1) , today):
        try:
            Country_Data = daily_report(single_date.strftime("%m-%d-%Y"))
            Country_Data = pd.DataFrame(Country_Data)
            # old schema
            # Province / State, Country / Region, LastUpdate, Confirmed, Deaths, Recovered, Latitude, Longitude
            # new schema
            # FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key
            if 'Country/Region' in Country_Data:
                Country_Data = Country_Data.rename(columns={'Country/Region': 'Country_Region'})
            for country in Country_Data['Country_Region'].unique():
                saveToDB(country, single_date, Country_Data)
        except:
            print("No such date")

def saveToDB(country, single_date, Country_Data):
    Country_in = country
    Date_in = single_date.strftime("%Y-%m-%d")
    data = Country_Data.loc[Country_Data['Country_Region'] == country]
    Dead_in = data.groupby(["Country_Region"]).sum()['Deaths'].values[0]
    Infected_in = data.groupby(["Country_Region"]).sum()['Confirmed'].values[0]
    Recoverd_in = data.groupby(["Country_Region"]).sum()['Recovered'].values[0]

    # populate whit data
    try:
        country = models.Country(Country=Country_in, Date=Date_in, Dead=Dead_in, Infected=Infected_in, Recovered=Recoverd_in)
        country.save()
    except:
        print("there was a problem with date or country in data popultaion", single_date.strftime("%d-%m-%Y"))


def Last_Update_Date():
    return models.Country.objects.last().Date

# to be run in shell once
def Make_initail_Databese(Country_selected="Poland", Start_date='03-14-2020'):
    today = datetime.date.today().strftime('%m-%d-%Y')
    for single_date in pd.date_range(Start_date, today):
        try:
            Country_Data = daily_report(single_date.strftime("%m-%d-%Y"))
            Country_Data = pd.DataFrame(Country_Data)
            # old schema
            # Province / State, Country / Region, LastUpdate, Confirmed, Deaths, Recovered, Latitude, Longitude
            # new schema
            # FIPS, Admin2, Province_State, Country_Region, Last_Update, Lat, Long_, Confirmed, Deaths, Recovered, Active, Combined_Key
            if 'Country/Region' in Country_Data:
                Country_Data = Country_Data.rename(columns={'Country/Region': 'Country_Region'})

            Country_Data = Country_Data.loc[Country_Data['Country_Region'] == Country_selected]
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(Country_Data)
            Country_in = Country_Data.loc[Country_Data["Country_Region"] == Country_selected]["Country_Region"].values[
                0]
            Date_in = single_date.strftime("%Y-%m-%d")
            Dead_in = Country_Data.loc[Country_Data["Country_Region"] == Country_selected]["Deaths"].values[0]
            Infected_in = Country_Data.loc[Country_Data["Country_Region"] == Country_selected]["Confirmed"].values[0]
            Recoverd_in = Country_Data.loc[Country_Data["Country_Region"] == Country_selected]["Recovered"].values[0]

            # populate whit data
            try:
                country = models.Country(Country=Country_in, Date=Date_in, Dead=Dead_in, Infected=Infected_in,
                                         Recoverd=Recoverd_in)
                country.save()
            except:
                print("there was a problem with date or country in data popultaion", single_date.strftime("%d-%m-%Y"))
        except:
            print("Sth gone wrong")
