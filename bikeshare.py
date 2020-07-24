import time
import numpy as np
import pandas as pd
import pdb

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def check_input(input_str,input_type):
    while True:
        input_read=input(input_str).title()
        try:
            if input_read in ['new york city','chicago','washington'] and input_type==1:
                break
            elif input_read in ['january','february','march','april','may','june','all'] and input_type==2:
                break
            elif input_read in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'] and input_type==3:
                break
            else:
                if input_type==1:
                    print('wrong city')
                if input_type==2:
                    print('invalid month')
                if input_type==3:
                    print('invalid day')
        except valueError:
            print('wrong input')
    return(input_read)

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city=check_input('Please enter New york,Chicago or Washington: ',1)
    month=check_input('please enter month: ',2)
    day=check_input('Please enter day of week: ',3)
    print('-'*40)
    return city,month,day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour']=df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    start_time=time.time()
    print(df['month'].mode()[0])
    print(df['day_of_week'].mode()[0])
    print(df['hour'].mode()[0])
    print('elapsed time is: ',(time.time()-start_time))

def Station_stats(df):
    start_time=time.time()
    popular_start_station =df['Start Station'].mode()[0]
    print('most popular  start station is',popular_start_station)
    popular_end_station =df['End Station'].mode()[0]
    print('most popular  end station is',popular_end_station)
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station=group_field.size().sort_values(ascending=False).head(1)
    print('most popular combination is :',popular_combination_station)
    print('This took this time: ',(time.time()-start_time))
    print('-'*40)


def trip_stats(df):
    start_time=time.time()
    print('Total travel time is ',df['Trip Duration'].sum())
    print('Mean travel timeis ',df['Trip Duration'].max())
    print('This took this time: ',(time.time()-start_time))
    print('-'*40)


def User_stats(df,city):
    start_time=time.time()
    print(df['User Type'].value_counts())
    if city != 'washington':
        print(df['Gender'].value_counts())
        print(df['Birth Year'].mode()[0])
        print(df['Birth Year'].max())
        print(df['Birth Year'].min())
    print('\nThis took %s seconds.: ',(time.time()-start_time))
    print('-'*40)

def main():
    while True:
        city,month,day=get_filters()
        df=load_data(city,month,day)
        time_stats(df)
        Station_stats(df)
        trip_stats(df)
        User_stats(df,city)
        print(df.head())
        restart=input(' would you like to try again? ')
        if restart == 'no':
            break

if __name__ == "__main__":
	main()
