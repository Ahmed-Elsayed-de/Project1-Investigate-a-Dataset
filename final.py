from cmath import nan
import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv' , 'new york city': 'new_york_city.csv','washington': 'washington.csv'  }
#===================================================================================================================
#Function to figure out the filtering requirements of the user
def get_filters():
    print("=============================================================================================================")
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities= ['washington','chicago','new york city']
    while True:
        cities= ['washington','chicago','new york city']
        city= input("\n Would you like to see data for Chicago, New York, or Washington? \n").lower()
        if city in cities:
            break
        else:
            print("\n it's not a one of the three cities Please try again") 
    #display data by month, day, both, or not at all
    Data_filter= input("\n Would you like to filter the data by month, day, both, or not at all? Type none for no time filter \n").lower()
    months= ['january','february','march','april','may','june','all']
    days= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    
    if Data_filter == "none":
        month="all"
        day="all"
    elif Data_filter == "both":
        while True:
            month = input("\n Which month would you like to filter by from January to June? Type 'all' for no filter\n").lower()
            if month in months:
                break
            else:
                print("\n Please month has to be from January to June Please try againchicago ")
        while True:
            day = input("\n Which day of the week would you like to filter by from Monday to Sunday)? Type 'all' for no filter \n").lower()
            if day in days:
                break
            else:
                print("\n it's not a one of the weekdays Please try again") 
    elif Data_filter == "month":
        while True:
            month = input("\n Which month would you like to filter by from January to June? Type 'all' for no filter\n").lower()
            if month in months:
                break
            else:
                print("\n Please month has to be from January to June Please try againchicago ")
        day="all"
    elif Data_filter == "day":
        while True:
            day = input("\n Which day of the week would you like to filter by from Monday to Sunday)? Type 'all' for no filter \n").lower()
            if day in days:
                break
            else:
                print("\n it's not a one of the weekdays Please try again")
        month="all"
     
    print(("\nYou have chosen to filter data by city: {} , month: {} and day: {} .").format(city, month, day))
    print('-'*70)
    #Returning the city, month and day selections
    return city, month, day
#===================================================================================================================
#Function to load data from .csv files
def load_data(city, month, day):
    print("=============================================================================================================")
    
    #Load data for city
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    input_list = ['all', 'none']
    #Filter by month if applicable
    if month not in input_list:
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day not in input_list:
        df = df[df['day_of_week'] == day.title()]

    return df
#===================================================================================================================
#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    print("=============================================================================================================")

    print("1 common times of travel (occurs most often in the start time)")
    start_time = time.time()
    # the most common month
    Common_month = df['month'].mode()[0]
    # the most common day of week    
    common_day = df['day_of_week'].mode()[0]
    # the most common start hour    
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    
    print("------------------------------------------------------------")
    print(f"Common Month: ({Common_month})\nCommon Day: ({common_day})\nCommon Start Hour: ({common_hour})")
    print("------------------------------------------------------------")

    #Prints the time taken to perform the calculation
    print(f"This took {(time.time() - start_time)} seconds.")
    print("------------------------------------------------------------")
   
#==================================================================================================================
#Function to calculate station related statistics
def station_stats(df):
    print("=============================================================================================================")
    
    print("2 Popular stations and trip")
    start_time = time.time()

    #the most common start station
    common_start_station = df['Start Station'].mode()[0]
    
    #the most common end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    period = df['Start To End'].mode()[0]

    print("------------------------------------------------------------")
    print(f"Common used start station: ({common_start_station})\nCommon used end station: ({common_end_station})\nCommon combination of trips are from: ({period})")
    print("------------------------------------------------------------")

    #Prints the time taken to perform the calculation
    print(f"This took {(time.time() - start_time)} seconds.")
    print("------------------------------------------------------------")
#==================================================================================================================
#Function for trip duration related statistics
def trip_duration_stats(df):
    print("=============================================================================================================")
    print("3 Trip duration")
    start_time = time.time()

    #total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("------------------------------------------------------------")
    print("The total trip duration")
    print(f"hours: ({hour})\nminutes: ({minute})\nseconds: ({second})")
    print("------------------------------------------------------------")

    #average travel time
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hours, mins = divmod(mins, 60)
        print("------------------------------------------------------------")
        print("The average trip duration")
        print(f"hours: ({hours})\nminutes: ({mins})\nseconds: ({sec})")
        print("------------------------------------------------------------")
    else:
        print("------------------------------------------------------------")
        print("The average trip duration")
        print(f"--minutes: ({mins})\nseconds: ({sec})")
        print("------------------------------------------------------------")

    print(f"This took {(time.time() - start_time)} seconds.")
    print("------------------------------------------------------------")
#==================================================================================================================
#Function to calculate user statistics
def user_stats(df,city):
    print("=============================================================================================================")
    
    print("4 User info")
    start_time = time.time()
    print("------------------------------------------------------------")
    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"The types of users :\n{user_type}")
    print("------------------------------------------------------------")
    
    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender = df['Gender'].value_counts()
    else:
        gender = "none"
    print(f"The counts of users by gender:\n{gender}")
    print("------------------------------------------------------------")
    
    # Display earliest, most recent, and most common year of birth
    earliest = int(df['Birth Year'].min())
    recent = int(df['Birth Year'].max())
    common_year = int(df['Birth Year'].mode()[0])
    print("------------------------------------------------------------")
    print(f"The oldest user: ({earliest})\nThe youngest user: ({recent})\nmost common year of birth: ({common_year})")
    print("------------------------------------------------------------")

    print(f"This took {(time.time() - start_time)} seconds.")
    print("------------------------------------------------------------")
#==================================================================================================================
#display data
def display_data(df):
    print("=============================================================================================================")
    input_list = ['yes', 'no']
    counter = 0
    #display first 5 rows of data
    while True:
        entry_choice= input("would like want to see the raw data (5 rows)? Type 'yes' or 'no'\n").lower()
        if entry_choice in input_list:        
            if entry_choice=='yes':
                    print(df.head())
                    break
            else:    
                    break
        else:
            print("Please enter a valid input_list")
    #display next 5 rows of data
    if  entry_choice=='yes':       
            while True:
                entry_choice_2= input("would like to see 5 more rows of the data? Type 'yes' or 'no'\n").lower()
                if entry_choice_2 in input_list:
                    if entry_choice_2=='yes':
                        counter += 5
                        print(df[counter:counter+5])
                    else:    
                        break  
                else:
                    print("Please enter a valid input_list")       
#==================================================================================================================
#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()