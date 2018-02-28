import os
import re
from numpy.random import rand as r
import json

def generate_hsl_colour_dictionary(keys):
    colour_dict = {}
    for key in keys:
        colour_dict[key] = "hsl({hue},{saturation}%,{lightness}%)".format(hue=360*r(), saturation=25 + 70*r(),
                                                                          lightness=85 + 10*r())

    return colour_dict

def generate_error_report(output_directory, html_output_filename, html_template, variable_name, class_names, failures_dict,
                          highlight_regexes=True, custom_class_colours=None):
    json_filename = html_output_filename.split('.')[0] + '.json'
    generate_generic_report(output_directory, html_output_filename, html_template)
    generate_error_json(output_directory, json_filename, variable_name, class_names, failures_dict, highlight_regexes)

def generate_error_json(output_directory, json_filename, variable_name, class_names, failures_dict,
                        highlight_regexes=True, custom_class_colours=None):

    json_fname = os.path.join(output_directory, json_filename)

    data = {}

    data['var_name'] = variable_name
    data['classes'] = generate_hsl_colour_dictionary(class_names) if not custom_class_colours else custom_class_colours
    data['patient_cases'] = {}

    with open(json_fname, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def generate_generic_report(output_directory, html_output_filename, html_template):
    html_fname = os.path.join(output_directory, html_output_filename)

    with open(html_template) as in_file:
        with open(html_fname, "w") as out_file:
            for line in in_file:
                out_file.write(line)
