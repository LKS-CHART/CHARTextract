import os
from jinja2 import Environment, FileSystemLoader
from numpy.random import rand as r
import json
import pickle
import csv
import shutil
import pathlib

class CyclicIterator:
    def __init__(self, iterable):
        self.i = 0
        self.max_len = len(iterable)
        self.iterable = iterable

    def __iter__(self):
        return self

    def next(self):
        if self.max_len == 0:
            raise StopIteration

        if self.i >= self.max_len:
            self.i = 0

        i = self.i
        self.i += 1
        return self.iterable[i]

def _generate_match_for_json(match_obj):
    """Generates a simplified match object to be exported as a json
    
    Arguments:
        match_obj {dict} -- {class_name -> {sentence_id -> [match_objs]}}
    
    Returns:
        match_dict {dict} -- Simplified match dictionary {class_name -> {sentence_id -> [unrolled match_objs]}}
    """

    match_dict = {}

    #For each class e.g smoker, nonsmoker etc..
    for class_name in match_obj:
        match_dict[class_name] = {}

        #For each sentence that had a match for that class
        for sentence_id in match_obj[class_name]:
            matches = []
            match_dict[class_name][sentence_id] = {"matches": matches, "text_score":  match_obj[class_name][sentence_id]["text_score"]}

            #TODO: Duplicate values generated if all_matches parameter is used. Fix this?

            #Looping through the matches in the sentence
            for regex_obj in match_obj[class_name][sentence_id]['matches']:

                #Adding the primary matches in the match_obj
                primary = {"name": regex_obj["name"], "score": regex_obj["score"],
                                                    "pattern": regex_obj["pattern"], "effect": regex_obj["effect"], "aggregate_score": regex_obj["aggregate_score"], "matches": [], "secondary_regexes": []}

                for match in regex_obj["matches"]:
                    primary["matches"].append({"match_start": match.start(), "match_end": match.end(), "matched_string": match.group()})

                #Unrolling the secondary matches and just adding them on
                for secondary_regex in regex_obj["secondary_matches"]:
                    secondary = {"name": secondary_regex["name"], "score": secondary_regex["score"],
                                                    "pattern": secondary_regex["pattern"], "effect": secondary_regex["effect"], "matches": []}

                    for secondary_match in secondary_regex["matches"]:
                        secondary["matches"].append({"match_start": secondary_match.start(), "match_end": secondary_match.end(), "matched_string": secondary_match.group()})

                    primary["secondary_regexes"].append(secondary)

                matches.append(primary)
    return match_dict

def _generate_hsl_colour_dictionary(keys, lightness=85):
    """Given keys, generates dictionary of key -> light colour
    
    Arguments:
        keys {list} -- List of key names
    
    Keyword Arguments:
        lightness {int} -- How light to make the colour (default: {85})
    
    Returns:
        colour_dict{dict} -- Dictionary which maps the class name to a colour
    """

    colours = ["#c4e5ff", "#c0ffbc", "#ffe8b2", "#ffb8b5", "#f9f9b1", "#e8bcff"]
    colour_dict = {}

    if len(keys) > len(colours):
        for key in keys:
            colour_dict[key] = "hsl({hue},{saturation}%,{lightness}%)".format(hue=360*r(), saturation=25 + 70*r(),
                                                                              lightness=lightness + 10*r())
    else:
        iterator = CyclicIterator(colours)

        colour_dict = {key: iterator.next() for key in keys}

    return colour_dict

def generate_error_report(output_directory, template_directory, variable_name, class_names, failures_dict, effects, custom_class_colours=None, custom_effect_colours=None, addition_json_params=None):
    """Generates an error report html file and corresponding json file
    
    Arguments:
        output_directory {String} -- Where to output the html json file
        html_output_filename {String} -- The name of the output file
        template_directory {String} -- Location of the html templates
        html_template {String} -- Name of the template we are using
        variable_name {String} -- Variable name in question
        class_names {List} -- List of classes for the variable (e.g nonsmoker, smoker, exsmoker etc..)
        failures_dict {dict} -- {id -> {label, data, matches, pred, actual, score}}
        effects {List} -- List of effects (e.g rb, ra, ib etc..) 
    
    Keyword Arguments:
        custom_class_colours {dict} -- Dictionary which maps class name to a colour (default: {None})
        custom_effect_colours {dict} -- Dictionary which maps effect name to a colour (default: {None})
    """

    #generating report
    json_filename = 'error_report.json'
    generate_generic_report(output_directory, template_directory, ['index.html', 'javascripts/main.js', 'javascripts/DataService.js',
                                                                   'javascripts/ErrorController.js', 'views/view.html', 'views/overview.html',
                                                                   'stylesheets/styles.css', 'views/settings.html',
                                                                   'settings.json', 'views/regexes.html',
                                                                   'javascripts/text-editor.js',
                                                                   'javascripts/RuleController.js',
                                                                   "javascripts/LoaderService.js",
                                                                   "javascripts/LoaderController.js"])
    generate_json(output_directory, json_filename, variable_name, class_names, failures_dict, effects, custom_class_colours, custom_effect_colours, addition_json_params=addition_json_params)

def generate_json(output_directory, json_filename, variable_name, class_names, patients_dict, effects, custom_class_colours=None, custom_effect_colours=None, addition_json_params=None):
    """Generates a json file for the html
    
    Arguments:
        output_directory {String} -- Where to output the json file
        json_filename {String} -- Name of the json file
        variable_name {String} -- Name of the variable in question
        class_names {list} -- List of classes for the variable (e.g non smoker, smoker, exsmoker etc..)
        patients_dict {dict} -- {id -> {data, matches, pred, actual, score}}
        effects {list} -- List of effect types (e.g rb,ra,ib,aa etc..)
    
    Keyword Arguments:
        custom_class_colours {dict} -- Dictionary which maps class name to a colour (default: {None})
        custom_effect_colours {dict} -- Dictionary which maps effect name to a colour (default: {None})
    """

    #TODO: refactor patient_cases

    json_fname = os.path.join(output_directory, json_filename)

    data = {}

    data["var_name"] = variable_name
    data["classes"] = _generate_hsl_colour_dictionary(class_names) if not custom_class_colours else custom_class_colours
    data["effects"] = _generate_hsl_colour_dictionary(effects, lightness=0) if not custom_effect_colours else custom_effect_colours
    if addition_json_params:
        data.update(addition_json_params)

    data["patient_cases"] = {}

    failure_files = list(filter(lambda file: file.startswith("failure_set"), os.listdir(output_directory)))

    latest_file = None

    if failure_files:
        latest_file = max(failure_files, key=lambda i: int(i.split("_")[2].split(".")[0]))

    recurring = set()

    if latest_file:
        with open(os.path.join(output_directory, latest_file)) as f:
            lines = csv.reader(f)
            recurring = set(list(lines)[0])

    #Generating information for each patient
    for patient_id in patients_dict:
        data["patient_cases"][patient_id] = {"data": patients_dict[patient_id]["data"],
                                            "matches": _generate_match_for_json(patients_dict[patient_id]["matches"]),
                                             "pred": patients_dict[patient_id]["pred"],
                                             "actual": patients_dict[patient_id]["label"],
                                             "score": patients_dict[patient_id]["score"], "recurring": False}

        if str(patient_id) in recurring:
            data["patient_cases"][patient_id]["recurring"] = True



    errors_write_name = "failure_set_0.txt" if not latest_file else "failure_set_" \
                                                                    + str(int(latest_file.split("_")[2].split(".")[0])
                                                                    + 1)\
                                                                    + ".txt"

    with open(os.path.join(output_directory, errors_write_name), "w") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(list(patients_dict))

    #Creating the json
    with open(json_fname, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def generate_classification_report(output_directory, template_directory, variable_name, class_names, all_patients, effects, custom_class_colours=None, custom_effect_colours=None, addition_json_params=None):
    """Generates a classification report html file and corresponding json file

    Arguments:
        output_directory {String} -- Where to output the html json file
        html_output_filename {String} -- The name of the output file
        template_directory {String} -- Location of the html templates
        html_template {String} -- Name of the template we are using
        variable_name {String} -- Variable name in question
        class_names {List} -- List of classes for the variable (e.g nonsmoker, smoker, exsmoker etc..)
        failures_dict {dict} -- {id -> {label, data, matches, pred, actual, score}}
        effects {List} -- List of effects (e.g rb, ra, ib etc..) 
    
    Keyword Arguments:
        custom_class_colours {dict} -- Dictionary which maps class name to a colour (default: {None})
        custom_effect_colours {dict} -- Dictionary which maps effect name to a colour (default: {None})
    """
    json_filename = 'classification_report.json'
    generate_generic_report(output_directory, template_directory, ['classification_report.html'], {'classification_report.html': {"json_file": json_filename}})
    generate_json(output_directory, json_filename, variable_name, class_names, all_patients, effects, custom_class_colours, custom_effect_colours, addition_json_params=addition_json_params)

def generate_generic_report(output_directory, template_folder, templates, template_args=None):
    """Given a tempalte, create a report with the given template_args
    
    Arguments:
        output_directory {string} -- Where to output the file
        html_output_filename {String} -- Name of the output file
        template_folder {String} -- Location of the html templates
        html_template {String} -- The template we want to generate the report from
        template_args {**kwargs} -- List of vars that will be replaced in the template with the given values
    """
    #Creating Jinga Environment
    env = Environment(loader=FileSystemLoader(template_folder))

    for template in templates:
        file_path_tokens = template.split("/")
        template_fname = file_path_tokens[-1]

        #Getting the template we want to use

        if len(file_path_tokens) > 1:
            if not os.path.exists(os.path.join(*file_path_tokens[0:-1])):
                pathlib.Path(os.path.join(output_directory, *file_path_tokens[0:-1])).mkdir(parents=True, exist_ok=True)

        fname = os.path.join(output_directory, *file_path_tokens)

        template = env.get_template(template_fname)
        #Rendering the template with the given args
        if template_args and template_fname in template_args:
            output = template.render(**template_args[template_fname])
        else:
            output = template.render()

        with open(fname, "w") as out_file:
            out_file.write(output)
