# Terminal based Strava API connection program with activity data analysis 
# author: chrisbrunet

import requests
import urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Introduction
print("\nWelcome to the Strava API Test App")
client_id = '111595'

# API access token generation
auth_url = "https://www.strava.com/oauth/token"
payload = {
    'client_id': client_id,
    'client_secret': '8e8f246270159ece4b0eb3c75e494241bad86027',
    'refresh_token': '8285947a1614c22ebf0a7308cafb267ed4d9426f',
    'grant_type': 'refresh_token',
    'f': 'json'
}
print("\nRequesting Access Token...")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print(f"\nAccess Token = {access_token}")

# Getting activity data
print("\nGetting Activity Data...")
activities_url = "https://www.strava.com/api/v3/athlete/activities"
header = {'Authorization': 'Bearer ' + access_token}
request_page_num = 1
all_activities = []
while True:
    param = {'per page': 200, 'page': request_page_num}
    get_activities = requests.get(activities_url, headers=header,params=param).json()
    if len(get_activities) == 0:
        break
    all_activities.extend(get_activities)
    request_page_num += 1
all_activities_df = pd.DataFrame(all_activities)

# Getting segment data
print("\nGetting Segment Data...")
bounds = [51.036047, -114.150184, 51.054738, -114.111313]
segments_url = "https://www.strava.com/api/v3/segments/explore"
header = {'Authorization': 'Bearer ' + access_token}
param = {'bounds': ','.join(str(coord) for coord in bounds)}
get_segments = requests.get(segments_url, headers=header, params=param).json()
all_segments = pd.DataFrame(get_segments)
normalized_data = pd.json_normalize(all_segments['segments'])
all_segments_df = pd.concat([all_segments, normalized_data], axis=1)
all_segments_df.drop(columns=['segments'], inplace=True)

# Most recent activity
print("\nMost Recent Activity:")
print(f"\tName: \t{all_activities_df['name'][0]}")
print(f"\tType: \t{all_activities_df['type'][0]}")
print(f"\tDist: \t{round(all_activities_df['distance'][0] / 1000, 2)}km")

# Bike Ride Analysis
all_rides = all_activities_df[all_activities_df['type'] == 'Ride']
all_bike_commutes = all_rides[all_rides['commute'] == True]
all_rides_exc_commutes = all_rides[all_rides['commute'] == False]
all_virtual_rides = all_activities_df[all_activities_df['type'] == 'VirtualRide']

print(f"\nBike Rides (excluding commutes):")
total_rides = len(all_rides_exc_commutes)
total_ride_distance = all_rides_exc_commutes['distance'].sum() / 1000
total_ride_elevation = all_rides_exc_commutes['total_elevation_gain'].sum()
avg_ride_speed = all_rides_exc_commutes['average_speed'].mean() * 3.6
avg_ride_power = all_rides_exc_commutes['average_watts'].mean()
avg_ride_distance = all_rides_exc_commutes['distance'].mean() / 1000
avg_ride_elevation = all_rides_exc_commutes['total_elevation_gain'].mean()

print(f"\n\tTotal Rides: {total_rides}")
print(f"\tTotal Distance: {round(total_ride_distance, 0)} km")
print(f"\tTotal Elevation: {round(total_ride_elevation, 0)} m")

print(f"\n\tAvg Speed: {round(avg_ride_speed, 1)} km/h")
print(f"\tAvg Power: {round(avg_ride_power, 1)} watts")
print(f"\tAvg Distance: {round(avg_ride_distance, 1)} km")
print(f"\tAvg Elevation: {round(avg_ride_elevation, 1)} m")

print(f"\nBike Commutes:")
total_commutes = len(all_bike_commutes)
total_commute_distance = all_bike_commutes['distance'].sum() / 1000
total_commute_elevation = all_bike_commutes['total_elevation_gain'].sum()
avg_commute_speed = all_bike_commutes['average_speed'].mean() * 3.6
avg_commute_power = all_bike_commutes['average_watts'].mean()
avg_commute_distance = all_bike_commutes['distance'].mean() / 1000
avg_commute_elevation = all_bike_commutes['total_elevation_gain'].mean()

print(f"\n\tTotal Rides: {total_commutes}")
print(f"\tTotal Distance: {round(total_commute_distance, 0)} km")
print(f"\tTotal Elevation: {round(total_commute_elevation, 0)} m")

print(f"\n\tAvg Speed: {round(avg_commute_speed, 1)} km/h")
print(f"\tAvg Power: {round(avg_commute_power, 1)} watts")
print(f"\tAvg Distance: {round(avg_commute_distance, 1)} km")
print(f"\tAvg Elevation: {round(avg_commute_elevation, 1)} m")

print(f"\nVitrual Bike Rides:")
total_virtual_rides = len(all_virtual_rides)
total_virtual_ride_distance = all_virtual_rides['distance'].sum() / 1000
total_virtual_ride_elevation = all_virtual_rides['total_elevation_gain'].sum()
avg_virtual_ride_speed = all_virtual_rides['average_speed'].mean() * 3.6
avg_virtual_ride_power = all_virtual_rides['average_watts'].mean()
avg_virtual_ride_distance = all_virtual_rides['distance'].mean() / 1000
avg_virtual_ride_elevation = all_virtual_rides['total_elevation_gain'].mean()

print(f"\n\tTotal Rides: {total_virtual_rides}")
print(f"\tTotal Distance: {round(total_virtual_ride_distance, 0)} km")
print(f"\tTotal Elevation: {round(total_virtual_ride_elevation, 0)} m")

print(f"\n\tAvg Speed: {round(avg_virtual_ride_speed, 1)} km/h")
print(f"\tAvg Power: {round(avg_virtual_ride_power, 1)} watts")
print(f"\tAvg Distance: {round(avg_virtual_ride_distance, 1)} km")
print(f"\tAvg Elevation: {round(avg_virtual_ride_elevation, 1)} m")

# Running Analysis

print(all_segments_df[['name', 'distance', 'avg_grade']])
