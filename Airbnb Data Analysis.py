"""
    CS051P Final Project

    Author: Aser Atawya

    Date:  12/08/2021

    The purpose  of this program is to analyze Airbnb data to look for any
     correlation between the price of a listing and the overall satisfaction, see if
     it is typical for hosts to have multiple listings at the same time, and analyze
     the change in the rental prices and the variations of prices in different neighborhoods.
"""
import matplotlib.pyplot as plt
from scipy.stats.stats import spearmanr


def price_satisfaction(filename):
    """ stores the price and the overall_satisfaction of each room in a sublist
    and returns all the sublists in the form of a list of lists.

    :param filename: (str) the name of the file containing the data
    :return: (list of lists of floats) list of sublists consisting of each room's price and overall_satisfaction
    """
    list_price_satisfaction = []
    with open(filename, "r", encoding="utf-8") as file_in:
        content = file_in.readlines()

        # figures out the order of the relevant columns since not all files have the same columns
        header = content[0].split(',')
        total_columns = len(header)
        for counter in range(total_columns):
            if header[counter] == "price":
                price = counter
            elif header[counter] == "reviews":
                reviews = counter
            elif header[counter] == "overall_satisfaction":
                satisfaction = counter

        # ignores the first line, which contains the title of the columns
        for i in range(1, len(content)):
            placeholder = []
            line = content[i].split(',')
            # ignores the line if the the price or the satisfaction is not an a number
            try:
                float(line[price])
                float(line[satisfaction])
            except:
                continue
            # ignores the line if it's empty in the price, reviews, or satisfaction columns
            # ignores the line if it has more commas than supposed to be to avoid inaccurate data reading
            # ignores the line if it the number of reviews is not a positive number
            if line[price] == "" or line[reviews] == "" or line[satisfaction] == "" or \
                    str(line).count(',') != total_columns or not (float(line[reviews]) > 0):
                continue
            placeholder.append(float(line[price]))
            placeholder.append(float(line[satisfaction]))
            list_price_satisfaction.append(placeholder)

    return list_price_satisfaction


def correlation(l):
    """  takes list_price_satisfaction, the output of the function price_satisfaction,
    and returns the correlation between the price and the overall satisfaction

    :param l: (list of lists of floats) list of sublists consisting of each room's price and overall_satisfaction
    :return: (tuple) the correlation between the price and the overall satisfaction.
    """
    price = []
    rating = []
    for element in l:
        price.append(element[0])
        rating.append(element[1])
    result = spearmanr(price, rating)
    correlation = result.correlation
    pvalue = result.pvalue
    return correlation, pvalue


def host_listings(filename):
    """ creates and returns a dictionary where the keys are host_ids (int)
     and the values are a list of room_ids (int) associated with that host.

    :param filename: (string) the name of the file containing the data
    :return: (dictionary) a dictionary mapping every host_id to the list of room_ids associated with that host
    """
    dictionary = {}
    with open(filename, "r", encoding="utf-8") as file_in:
        content = file_in.readlines()
        # figures out the order of the relevant columns since not all files have the same columns
        header = content[0].split(',')
        total_columns = len(header)
        for counter in range(total_columns):
            if header[counter] == "host_id":
                host_id = counter
            if header[counter] == "room_id":
                room_id = counter

        # ignores the first line, which contains the title of the columns
        for i in range(1, len(content)):
            line = content[i].split(',')
           # ignores the line if the host_id is not an integer
            try:
                int(line[host_id])
            except:
                continue
            # ignores the line if it's empty in the room_id or host_id columns
            # ignores the line if it has more commas than supposed to be to avoid inaccurate data reading
            if line[host_id] == "" or line[room_id] == "" or str(line).count(',') != total_columns:
                continue
            # if the host_id is already one of the keys of the dictionary, appends the new room_id to the existing list
            if int(line[host_id]) in dictionary.keys():
                dictionary[int(line[host_id])].append(int(line[room_id]))
            # If the host_id isn't a key, creates a new key and sets the value to be room-id associated with that host
            else:
                dictionary[int(line[host_id])] = [int(line[room_id])]

    return dictionary


def num_listings(d):
    """ takes as input the dictionary returned by host_listings and returns a list l
    where l[i] is the number of hosts having i number of rooms

    :param d: (dictionary) a dictionary mapping every host_id to the list of room_ids associated with that host
    :return: (list) a list l where l[i] is the number of hosts having i number of rooms
    """
    l = []
    # determines the largest number of rooms owned by the same host to put an endpoint to the list
    largest_num = 0
    for key in d.keys():
        if len(d[key]) > largest_num:
            largest_num = len(d[key])

    for i in range(largest_num + 1):
        counter = 0
        for key in d.keys():
            # counts the number of hosts having i listings
            if len(d[key]) == i:
                counter = counter + 1
        # adds the number of hosts to the list
        l.append(counter)

    return l


def room_prices(filename_list, roomtype):
    """ Reads a list of files and store all the prices of all the rooms in the files
     from the oldest data to the most recent in a dictionary.

    :param filename_list: (list of strings) list of filenames containing the data
    :param roomtype: (string) the type of the listing, which is â€œEntire home/aptâ€, â€œPrivate roomâ€ or â€œShared roomâ€
    :return: (dictionary) the keys are room_ids (int) and the values are a list of the prices over time (float)
    """
    # the roomtype can't be anything other than â€œEntire home/aptâ€, â€œPrivate roomâ€ or â€œShared roomâ€
    if roomtype != "Shared room" and roomtype != "Private room" and roomtype != "Entire home/apt":
        return "invalid call"

    room_price = {}
    date_filename = {}
    organized_date_filename = {}
    keys = []

    # stores the filenames as values in a dictionary whose keys are the dates
    for i in range(len(filename_list)):
        # extracts the dates from the filename
        date = filename_list[i][-14: -4]
        keys.append(date)
        date_filename[date] = filename_list[i]

    # orders the list keys in an ascending order from the earliest dates to the latest dates
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            # To order the list, we need to compare the dates with each other. I first compare years.
            # if the years are identical, I compare  months; if both months and years are identical, I compare days.
            if int(keys[i][0:4]) > int(keys[j][0:4]) or \
               (int(keys[i][0:4]) == int(keys[j][0:4]) and int(keys[i][5:7]) > int(keys[j][5:7])) or \
               (int(keys[i][0:4]) == int(keys[j][0:4]) and int(keys[i][5:7]) == int(keys[j][5:7]) \
                and int(keys[i][7:]) > int(keys[j][7:])):
                placeholder = keys[i]
                keys[i] = keys[j]
                keys[j] = placeholder

    # stores the filenames based on their dates ordered from earliest to latest
    for i in range(len(date_filename.keys())):
        organized_date_filename[keys[i]] = date_filename[keys[i]]

    for key in organized_date_filename.keys():
        with open(organized_date_filename[key], "r", encoding="utf-8") as file_in:
            content = file_in.readlines()
            # figures out the order of the relevant columns since not all files have the same columns
            header = content[0].split(',')
            total_columns = len(header)
            for counter in range(total_columns):
                if header[counter] == "price":
                    price = counter
                elif header[counter] == "room_id":
                    room_id = counter
                elif header[counter] == "room_type":
                    room_type = counter

            for i in range(1, len(content)):
                line = content[i].split(',')
                # ignores the line if the room_id is not an integer
                try:
                    int(line[room_id])
                except:
                    continue
                # ignores the line if it's empty in the room_id or price columns or doesn't match the given roomtype
                # ignores the line if it has more commas than supposed to be to avoid inaccurate data reading
                if line[price] == "" or line[room_id] == "" or str(line).count(',') != total_columns \
                        or line[room_type] != roomtype:
                    continue
                # if the room_id is already one of the dictionary's keys, appends the new price to the existing list
                if int(line[room_id]) in room_price.keys():
                    room_price[int(line[room_id])].append(float(line[price]))
                # If the room_id isn't a key, creates a new key and sets the value to be the room's price
                else:
                    room_price[int(line[room_id])] = [float(line[price])]

    return room_price


def price_change(d):
    """ takes as input the dictionary returned by the function room_prices and
    returns a tuple with 3 elements: maximum percentage change for the set
    of properties in the dictionary and the starting price and ending
    for the property that has the maximum percentage change

    :param d: (dictionary) dictionary in the format returned from room_prices
    :return: (tuple) tuple of 3 elements: the maximum percentage change and the associated starting and ending prices.
    """
    percent_change_dict = {}
    # stores the percentage change of each property in a dictionary whose keys are the room_ids
    for key in d.keys():
        initial_price = d[key][0]
        last_price = d[key][len(d[key]) - 1]
        percent_change = 100 * (last_price - initial_price) / initial_price
        percent_change_dict[key] = percent_change

    highest_percentage = 0
    key_maximum = 0
    # finds the largest percentage change regardless of the sign
    for key in percent_change_dict.keys():
        if abs(percent_change_dict[key]) > abs(highest_percentage):
            highest_percentage = percent_change_dict[key]
            # stores the key of the property that has the highest percentage change
            key_maximum = key

    # stores the starting and ending prices of the property that has the maximum percentage change
    starting = d[key_maximum][0]
    ending = d[key_maximum][len(d[key_maximum]) - 1]
    return highest_percentage, starting, ending


def price_by_neighborhood(filename):
    """ creates and returns a dictionary where each key is a neighborhood that appears in the file and
        the value for a key is the average price for an â€œEntire home/aptâ€ listing in that neighborhood.

    :param filename: (string) the name of the file containing the data
    :return: (dictionary) keys are neighborhoods & values are the avg prices of neighborhoods' â€œEntire home/aptâ€.
    """

    neighborhood_dict = {}
    with open(filename, "r", encoding="utf-8") as file_in:
        content = file_in.readlines()

        # figures out the order of the relevant columns since not all files have the same columns
        header = content[0].split(',')
        total_columns = len(header)
        for counter in range(total_columns):
            if header[counter] == "neighborhood":
                neighborhood = counter
            elif header[counter] == "room_type":
                room_type = counter
            elif header[counter] == "price":
                price = counter

        for i in range(1, len(content)):
            line = content[i].split(',')
            # ignores the line if the the price is not an a number
            try:
                float(line[price])
            except:
                continue
            # ignores the line if it's empty in the neighborhood or price columns or is not â€œEntire home/aptâ€
            # ignores the line if it has more commas than supposed to be to avoid inaccurate data reading
            if line[price] == "" or line[neighborhood] == "" or str(line).count(',') > total_columns \
                    or line[room_type] != "Entire home/apt":
                continue
            # collects all the prices of "Entire home/apt" listings of each neighborhood in a dictionary
            # if the neighborhood is already one of the dictionary's keys, appends the new price to the existing list
            if line[neighborhood] in neighborhood_dict.keys():
                neighborhood_dict[line[neighborhood]].append(float(line[price]))
            # If the neighborhood isn't a key, creates a new key and sets the value to be the room's price
            else:
                neighborhood_dict[line[neighborhood]] = [float(line[price])]

        # uses the data collected to calculate the average price of each neighborhood
        for key in neighborhood_dict.keys():
            total_price = 0
            for unit_price in neighborhood_dict[key]:
                total_price = unit_price + total_price
            average_price = total_price / len(neighborhood_dict[key])
            # replace the list of prices with the average price
            neighborhood_dict[key] = average_price

    return neighborhood_dict


def plot_data():
    """draws a plot between the i number of listings and number of hosts having i listings
    """
    host_dict = host_listings("tomslee_airbnb_new_york_1318_2017-06-12.csv")
    y_axis = num_listings(host_dict)
    x_axis = []
    # Stores all the numbers from 1 to the highest number of listings owned by the same host in a list
    for counter in range(1, len(y_axis)):
        x_axis.append(counter)
    # removes the 0 number of listings from the data because the number of owners of 0 listings is irrelevant
    y_axis.pop(0)
    plt.plot(x_axis, y_axis, label="linear")
    plt.xlabel("Number of Listings")
    plt.ylabel("Number of Hosts")
    plt.title("Listings - Hosts Plot")
    plt.legend()
    plt.show()


def main():
    plot_data()


if __name__ == '__main__':
    main()