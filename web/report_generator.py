import os
from jinja2 import Environment, FileSystemLoader
from numpy.random import rand as r
import json
import pickle

def _generate_match_for_json(match_obj):
    '''
    Generates a simplified match object to be exported as a json

    :param match_obj: {class_name -> {sentence_id -> Regex Objects}}

    :return: match_dictionary
    '''

    match_dict = {}

    for class_name in match_obj:
        match_dict[class_name] = {}
        for sentence_id in match_obj[class_name]:
            matches = []
            match_dict[class_name][sentence_id] = matches

            for regex_obj in match_obj[class_name][sentence_id]['matches']:
                matches.extend([{"name": regex_obj.name, "score": regex_obj.score,
                                                    "pattern": regex_obj.regex.pattern, "effect": "p", "match_start": match.start(),
                                                    "match_end": match.end(), "matched_string": match.group()} for match in regex_obj.matches])

                for secondary_regex in regex_obj.secondary_regexes:
                    secondary_dict = [{"name": secondary_regex.name, "score": secondary_regex.score,
                                                    "pattern": secondary_regex.regex.pattern, "effect": secondary_regex.effect, "match_start": match.start(),
                                                    "match_end": match.end(), "matched_string": match.group()} for match in secondary_regex.matches]
                    matches.extend(secondary_dict)

    return match_dict

def _generate_hsl_colour_dictionary(keys, lightness=85):
    '''
    Given keys names, generates light colours

    :param keys: class names

    :return: {class_name -> colour}
    '''
    colour_dict = {}
    for key in keys:
        colour_dict[key] = "hsl({hue},{saturation}%,{lightness}%)".format(hue=360*r(), saturation=25 + 70*r(),
                                                                          lightness=lightness + 10*r())

    return colour_dict

def generate_error_report(output_directory, html_output_filename, template_directory, html_template, variable_name, class_names, failures_dict, effects, custom_class_colours=None, custom_effect_colours=None):
    '''
    Generates an error report html file and corresponding json file

    :param output_directory: Where to output the html json file
    :param html_output_filename: The name of the output file
    :param template_directory: Location of html templates
    :param html_template: Name of the template we are using
    :param variable_name: Name of the variable in question
    :param class_names: List of classes for the variable (e.g nonsmoker, smoker, exsmoker etc...)
    :param failures_dict: {id -> {label:, data:, matches:, pred:, actual:, score:}
    :param custom_class_colours: Using predefined user colours
    '''
    json_filename = html_output_filename.split('.')[0] + '.json'
    generate_generic_report(output_directory, html_output_filename, template_directory, html_template, json_file=json_filename)
    generate_json(output_directory, json_filename, variable_name, class_names, failures_dict, effects, custom_class_colours, custom_effect_colours)

def generate_json(output_directory, json_filename, variable_name, class_names, patients_dict, effects, custom_class_colours=None, custom_effect_colours=None):
    '''
    Generates a json file for the html

    :param output_directory: Where to output the json file
    :param json_filename: Wame of the json file
    :param variable_name: Name of the variable in question
    :param class_names: List of classes for the variable (e.g non smoker, smoker, exsmoker etc..)
    :param patients_dict: {id -> {data:, matches:, pred:, actual:, score:}
    :param custom_class_colours: Using predefined user colours
    '''

    json_fname = os.path.join(output_directory, json_filename)

    data = {}

    data["var_name"] = variable_name
    data["classes"] = _generate_hsl_colour_dictionary(class_names) if not custom_class_colours else custom_class_colours
    data["effects"] = _generate_hsl_colour_dictionary(effects, lightness=0) if not custom_effect_colours else custom_effect_colours
    data["patient_cases"] = {}

    for patient_id in patients_dict:
        data["patient_cases"][patient_id] = {"data": patients_dict[patient_id]["data"],
                                            "matches": _generate_match_for_json(patients_dict[patient_id]["matches"]),
                                             "pred": patients_dict[patient_id]["pred"],
                                             "actual": patients_dict[patient_id]["label"],
                                             "score": patients_dict[patient_id]["score"]}

    #Regex Objects memory consumption  approximation
    pickled_str = pickle.dumps(data)
    print(len(pickled_str))

    with open(json_fname, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def generate_classification_report(output_directory, html_output_filename, template_directory, html_template, variable_name, class_names, all_patients, effects, custom_class_colours=None, custom_effect_colours=None):
    '''
    Generates a classification report html file and corresponding json file

    :param output_directory: Where to output the html json file
    :param html_output_filename: The name of the output file
    :param template_directory: Location of html templates
    :param html_template: Name of the template we are using
    :param variable_name: Name of the variable in question
    :param class_names: List of classes for the variable (e.g nonsmoker, smoker, exsmoker etc...)
    :param all_patients: {id -> {label:, data:, matches:, pred:, actual:, score:}
    :param custom_class_colours: Using predefined user colours
    '''
    json_filename = html_output_filename.split('.')[0] + '.json'
    generate_generic_report(output_directory, html_output_filename, template_directory, html_template, json_file=json_filename)
    generate_json(output_directory, json_filename, variable_name, class_names, all_patients, effects, custom_class_colours, custom_effect_colours)

def generate_generic_report(output_directory, html_output_filename, template_folder, html_template, **template_args):
    '''
    Given a template, create a report with the given template_args

    :param output_directory: Where to output the report file
    :param html_output_filename: Name of the output file
    :param template_folder: Location of html templates
    :param html_template: The template we want to generate the report from
    :param template_args: List of vars that will be replaced in the template with the given values
    '''
    html_fname = os.path.join(output_directory, html_output_filename)

    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template(html_template)

    output = template.render(**template_args)

    with open(html_fname, "w") as out_file:
        out_file.write(output)
