from countryinfo import CountryInfo
import difflib
import sqlite3
import pandas as pd 
from seoproject import added_to_database



list_of_names = []
list_of_langs=[]
countryname = CountryInfo("nigeria")
acc = 1

for name in countryname.all():
    list_of_names.append(name)
    acc += 1

def search_by_country_name(nameeofcount):
        countryAPI = CountryInfo(nameeofcount)
        results = [] 

        # Create object
        x = {
            'Name': [],
            #'Alt Spellings': [],
            'Region': [],
            'Subregion': [],
            'Capital': [],
            #'Currency': [],
            #'Languages': [],
            #'Provinces': [],
            #'Timezones': []
        }
        # Fill object

        results.append(("Name:", nameeofcount))
        x['Name'].append(nameeofcount)
        results.append(("Alt Spellings:", countryAPI.alt_spellings()))
        #x['Alt Spellings'].append(countryAPI.alt_spellings())
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
        #x['Currency'].append(countryAPI.currencies())

        results.append(("Languages:", countryAPI.languages()))
        #x['Languages'].append(countryAPI.languages())
        results.append(("Provinces:", countryAPI.provinces()))
        #x['Provinces'].append(countryAPI.provinces())
        results.append(("Timezones:", countryAPI.timezones()))
        #x['Timezones'].append(countryAPI.timezones())
        # result_string = "\n".join([f"{key} {value}" for key, value in results])

        #print(pd.DataFrame(results))

        # Send object to database
        #df = pd.DataFrame.from_dict(x)
        # print(df)
        
        # added_to_database(pd.DataFrame.from_dict(x))
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
            for match in similar_matches:
                print(match)
        else:
            print("Country does not exist, I'm sorry")

print(search_country(search_option, list_of_names))

# printhistory=input("Would you like to see previous Countries Searched?(Y or N): ")
# def history(printhistory):
#     if printhistory.lower() == "yes" or printhistory.lower() == "y":
#         added_to_database(data_frame)
#         print("Have a nice day!")
#     else:
#         print("Ok, Have a nice day!")
# history(printhistory)
