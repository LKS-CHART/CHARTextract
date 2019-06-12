# -*- coding: utf-8 -*-
# @Author: Shaun
# @Date:   2018
# @Last Modified by:   Chloe
# @Last Modified time: 2019-05-31 12:31:24

import csv
import json
import os
import argparse
import re
import random
import string

DICTIONARY_REGEX = r"dict:'\\?\\\((\w*)\\\\?\)'"

MAPPING = {"r": "Replace", "a": "Add", "i": "Ignore"}

def random_string(N=7):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=N))

def convert_regex(regex_pattern):
    # Remove parentheses
    if re.match(r"\((.*\|)*.*\)", regex_pattern):
        pattern_no_paren = regex_pattern[1:-1]
    else:
        pattern_no_paren = regex_pattern
    
    modified_pattern = []

    # Split by OR tag
    or_pattern_elements = pattern_no_paren.split("|")

    for i, el in enumerate(or_pattern_elements):

        # Replace dictionaries with dictionary tag
        dictionary_match = re.search(DICTIONARY_REGEX, el)
        if dictionary_match:
            dict_name = "{" + dictionary_match.groups()[0] + "}"
            keyword_tag = re.sub(DICTIONARY_REGEX, dict_name, el)
        else:
            keyword_tag = el

        # Split by .*
        wildcard_pattern_elements = keyword_tag.split(".*")
        for tag in wildcard_pattern_elements:
            try:
                re.search(tag, regex_pattern)
                modified_pattern += [tag]
            except Exception:
                # Unbalanced parenthesis error
                return [regex_pattern]

        # Add OR tag
        if i < len(or_pattern_elements) - 1:
            modified_pattern += ["OR"]
    return modified_pattern


def regexes_from_csv(filename):

    regexes = []
    class_name = None
    data = {}
    rules = []

    with open(filename, "r", encoding="utf8") as f:
        lines = csv.reader(f, delimiter=",", quotechar='"')
        for i, line in enumerate(lines):
            line = [token.strip().strip("\"") for token in line]

            # Load variable information from first line
            if i == 0:
                if not line[0].startswith("!"):
                    break
                class_name = line[0][1:]
                data["Name"] = class_name
                data["Dirty"] = False
                continue

            # Ignore blank lines
            if len(line) == 0:
                continue

            # Ignore commented code
            if line[0].startswith("#"):
                continue

            # Reading primary score and primary regex
            score = int(line[1])
            primary_pattern = convert_regex(line[0])
            rule = {
                "Primary": {
                    "Rule": primary_pattern, 
                    "Score": score, 
                    "Selected": False, 
                    "type": "Primary", 
                    "u_id": random_string()
                    }, 
                "Secondary": {
                    "Replace": [],
                    "Add": [],
                    "Ignore": []
                }}

            # Adding secondary rules
            for j in range(2, len(line) - 2, 3):
                pattern = convert_regex(line[j])
                effect = line[j+1]
                secondary_score = int(line[j+2])

                if len(effect) == 2:
                    secondary_rule = {
                        "Rule": pattern, 
                        "Modifier": effect[1], 
                        "Selected": False, 
                        "type": MAPPING[effect[0]], 
                        "Score": secondary_score, 
                        "u_id": random_string()
                    }
                else:
                    secondary_rule = {
                        "Rule": pattern, 
                        "Modifier": "None", 
                        "Selected": False, 
                        "type": MAPPING[effect[0]], 
                        "Score": secondary_score, 
                        "u_id": random_string()
                    }

                rule["Secondary"][MAPPING[effect[0]]].append(secondary_rule)

            rules.append(rule)

    data["Rules"] = rules

    return data


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("input_file",
                           help="Advanced view rules file")
    argparser.add_argument("output_file",
                           help="Basic view output rules file")
    args = argparser.parse_args()
    simple_rules = regexes_from_csv(args.input_file)
    with open(os.path.abspath(args.output_file), "w") as outfile:
        json.dump(simple_rules, outfile, indent=4)
