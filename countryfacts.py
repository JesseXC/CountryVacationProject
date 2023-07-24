from countryinfo import CountryInfo
import difflib
import sqlite3
import pandas as pd
from seoproject import added_to_database

list_of_names = []
list_of_langs = []
countryname = CountryInfo("nigeria")
acc = 1

for name in countryname.all():
    list_of_names.append(name)
    acc += 1

def search_by_country_name(nameeofcount):
    try:
        countryAPI = CountryInfo(nameeofcount)
    except KeyError:
        return None

    results = []

    x = {
        'Name': [],
        'Region': [],
        'Subregion': [],
        'Capital': [],
        'Currency': [],
        'Languages': [],
        'Provinces': [],
        'Timezones': []
    }

    results.append(("Name:", nameeofcount))
    x['Name'].append(nameeofcount)
    results.append(("Alt Spellings:", countryAPI.alt_spellings()))
    results.append(("Region:", countryAPI.region()))
    x['Region'].append(countryAPI.region())
    results.append(("Subregion:", countryAPI.subregion()))
    x['Subregion'].append(countryAPI.subregion())
    results.append(("Capital:", countryAPI.capital()))
    x['Capital'].append(countryAPI.capital())

    if len(countryAPI.currencies()) == 1:
        results.append(("Currency:", countryAPI.currencies()[0]))
    else:
        results.append(("Currencies:", countryAPI.currencies()))

    results.append(("Languages:", countryAPI.languages()))
    results.append(("Provinces:", countryAPI.provinces()))
    results.append(("Timezones:", countryAPI.timezones()))

    return results


def search_country(search_option, list_of_names):
    search_option = search_option.lower()

    if search_option in list_of_names:
        country_info = search_by_country_name(search_option)
        return country_info
    else:
        similar_matches = difflib.get_close_matches(search_option, list_of_names)
        if len(similar_matches) > 0:
            print("Country not found. Did you mean one of these?")
            for idx, match in enumerate(similar_matches, 1):
                print(f"{idx}. {match}")

            choice = input("Choose the number corresponding to the correct country or 'q' to quit: ")
            if choice == 'q':
                return None
            elif choice.isdigit() and 1 <= int(choice) <= len(similar_matches):
                search_option = similar_matches[int(choice) - 1]
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Country does not exist, I'm sorry")
            return None


        return search_country(search_option, list_of_names)

''' So what the program does is that it uses a try and except block to catch the KeyError when attempting to retrieve information for a non-existent country. 
The function search_by_country_name returns None if the country does not exist. In the search_country function, 
if the country doesn't exist, it prints a message and returns None, effectively terminating the search. Additionally, 
when similar matches are presented, the function calls itself recursively to allow the user to try again with the new search_option. 
This way, the user can retry their search without having to restart the entire program.'''
