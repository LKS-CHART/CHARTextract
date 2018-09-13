from datahandler import data_import as di
import os
import pycountry
from util import country_lists
import time
# Overview:
# Look for denonym, country, subdivision or city
# Save these statements and perform regexes
# Score country higher or lower based on regexes
# Respond with country with highest score
'''
## Overall Statistics
##                                          
##                Accuracy : 0.9184         
##                  95% CI : (0.804, 0.9773)
##     No Information Rate : 0.2653         
##     P-Value [Acc > NIR] : < 2.2e-16   
'''

country_list = []
common_names = {}
for each in pycountry.countries:
    country_list.append(each.name)
    if each.name.find(",") >= 0:
        common_name = each.name.split(",")[0]

        if common_name not in common_names:
            common_names[common_name] = each.name
    try:
        if each.common_name not in common_names:
            common_names[each.common_name] = each.name
    except AttributeError:
        pass

subdivisions = {}
for country_code in country_lists.subdivision_list:
    subdivs = pycountry.subdivisions.get(country_code=country_code)

    for subdiv in subdivs:
        subdivisions[subdiv.code] = pycountry.countries.get(alpha_2=country_code).name
        subdivisions[subdiv.name] = pycountry.countries.get(alpha_2=country_code).name

        if subdiv.name.find("(") >= 0:
            temp = subdiv.name.split("(")[1].split(")")[0].replace("-"," ")
            subdivisions[temp] = pycountry.countries.get(alpha_2=country_code).name

def get_cntr_list():
    cntr_list = []
    for c in pycountry.countries:
        print(c.name.lower())
        s = input()
        if s.strip() == "":
            cntr_list.append(c.name.lower())
        else:
            cntr_list.append(s.strip())

    return cntr_list


def preprocess(text, *args):
    start = time.time()
    text = text.replace(",", "").replace("-", " ").replace(";", "").replace(":", "")

    keep_data = False
    countries_found = []
    i = 0
    new_text = ""

    while text[i:] != "":
        word_checked = False

        # Check for major cities
        offset = 0
        for country in country_lists.major_city_list:
            for city in country_lists.major_city_list[country]:
                if text[i:].startswith(city + " "):
                    new_text += country
                    offset = len(city)
                    keep_data = True
                    word_checked = True
                    countries_found.append(country)
                    break
            if word_checked:
                break

        '''
        # Check cities near origin
        for country in country_lists.cities_near_orig:
            for city in country_lists.cities_near_orig[country]:
                if word == city:
                    text = text.replace(" {} ".format(word), " {} ".format(country))
                    keep = True
        '''

        # Look up full country names
        if not word_checked:
            for country_name in sorted(country_list, key=len, reverse=True):
                if text[i:].startswith(country_name + " "):
                    new_text += country_name
                    offset = len(country_name)
                    keep_data = True
                    word_checked = True
                    countries_found.append(country_name)
                    break

        # Look up common names for countries
        if not word_checked:
            for common_name in sorted(common_names, key=len, reverse=True):
                if text[i:].startswith(common_name + " "):
                    new_text += common_names[common_name]
                    offset = len(common_name)
                    keep_data = True
                    word_checked = True
                    print(common_name)
                    print(common_names[common_name])
                    countries_found.append(common_names[common_name])
                    break

        # Look up local subdivisions
        if not word_checked:
            for subdiv in country_lists.subdivision_conversion:
                if text[i:].startswith(subdiv + " "):
                    offset = len(subdiv)
                    temp_subdiv = country_lists.subdivision_conversion[subdiv]
                    keep_data = True
                    word_checked = True
                    new_text += subdivisions[temp_subdiv]
                    countries_found.append(subdivisions[temp_subdiv])
                    break

        # Look up subdivisions for specific countries
        if not word_checked:
            for subdiv_name in sorted(subdivisions, key=len, reverse=True):
                if text[i:].startswith(subdiv_name + " "):
                    offset = len(subdiv_name)
                    keep_data = True
                    word_checked = True
                    new_text += subdivisions[subdiv_name]
                    countries_found.append(subdivisions[subdiv_name])
                    break

        # Check denonym
        if not word_checked:
            for denonym in sorted(country_lists.denonym_list, key=len, reverse=True):
                if text[i:].startswith(denonym + " "):
                    offset = len(denonym)
                    country_code = country_lists.denonym_list[denonym]["alpha_2"]
                    new_text += pycountry.countries.get(alpha_2=country_code).name
                    keep_data = True
                    word_checked = True
                    countries_found.append(pycountry.countries.get(alpha_2=country_code).name)

        if text[i:].find(" ") > -1:
            if not word_checked:
                new_text += text[i:i+text[i:].find(" ") + 1]
                i += text[i:].find(" ") + 1
            else:
                new_text += " "
                i += offset + 1

    end = time.time() - start

    # for i, item in enumerate(countries_found):
    #     countries_found[i] = "\\b" + item + "\\b"

    if keep_data:
        # print("TIME TOOK: ", end)
        return {"sentence": new_text, "dictionaries": {"country": countries_found}}
    else:
        return {"sentence": None, "dictionaries": None}

