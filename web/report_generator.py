import os
from jinja2 import Environment, FileSystemLoader
from numpy.random import rand as r
import json

def _generate_match_for_json(match_obj):

    match_dict = {}

    for class_name in match_obj:
        match_dict[class_name] = {}
        for sentence_id in match_obj[class_name]:
            match_dict[class_name][sentence_id] = [{"name": regex_obj.name, "score": regex_obj.score,
                                                    "pattern": regex_obj.regex.pattern, "match_start": match.start(),
                                                    "match_end": match.end(), "matched_string": match.group()}
                                                   for regex_obj in match_obj[class_name][sentence_id]['matches']
                                                   for match in regex_obj.matches]
    return match_dict

def _generate_hsl_colour_dictionary(keys):
    colour_dict = {}
    for key in keys:
        colour_dict[key] = "hsl({hue},{saturation}%,{lightness}%)".format(hue=360*r(), saturation=25 + 70*r(),
                                                                          lightness=85 + 10*r())

    return colour_dict

def generate_error_report(output_directory, html_output_filename, template_directory, html_template, variable_name, class_names, failures_dict,
                          highlight_regexes=True, custom_class_colours=None):
    json_filename = html_output_filename.split('.')[0] + '.json'
    generate_generic_report(output_directory, html_output_filename, template_directory, html_template, json_file=json_filename)
    generate_error_json(output_directory, json_filename, variable_name, class_names, failures_dict, highlight_regexes)

def generate_error_json(output_directory, json_filename, variable_name, class_names, failures_dict,
                        highlight_regexes=True, custom_class_colours=None):

    json_fname = os.path.join(output_directory, json_filename)

    data = {}

    data["var_name"] = variable_name
    data["classes"] = _generate_hsl_colour_dictionary(class_names) if not custom_class_colours else custom_class_colours
    data["patient_cases"] = {}

    for patient_id in failures_dict:
        data["patient_cases"][patient_id] = {"data": failures_dict[patient_id]["data"],
                                            "matches": _generate_match_for_json(failures_dict[patient_id]["matches"]),
                                             "pred": failures_dict[patient_id]["pred"],
                                             "actual": failures_dict[patient_id]["label"],
                                             "score": failures_dict[patient_id]["score"]}

    with open(json_fname, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def generate_generic_report(output_directory, html_output_filename, template_folder, html_template, **template_args):
    html_fname = os.path.join(output_directory, html_output_filename)

    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template(html_template)

    output = template.render(**template_args)

    with open(html_fname, "w") as out_file:
        out_file.write(output)
