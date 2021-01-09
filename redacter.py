import json
import os

def read_muscles_file(path):
    with open(path) as f:
        muscles = json.load(f)
        return muscles


def get_description(name, muscles):
    description = ""
    try:
        description = muscles[name]["DESCRIPCIÓN"]
    finally:
        return description


def get_functions(name, muscles):
    function = ""
    try:
        function = muscles[name]["FUNCIÓN"]
    finally:
        return function


def get_insertions(name, muscles):
    insertion = ""
    try:
        insertion = muscles[name]["INSERCIÓN"]
    finally:
        return insertion

def get_reference(name, muscles):
    reference = ""
    try:
        reference = muscles[name]["IMAGEN"]
    finally:
        return reference


def strip_from_list(str_list):
    new_list = []

    for item in str_list:
        new_str = " ".join(item.split())

        if item:
            if new_str[-1] == ".":
                new_str = new_str[:-1]

            new_str = new_str.replace(":", ",")

        new_list.append(new_str)

    return new_list


def redact_info(name, muscles):
    functions = get_functions(name, muscles)
    insertions = get_insertions(name, muscles)
    description = get_description(name, muscles)

    if isinstance(functions, str):
        functions = [functions]

    if isinstance(insertions, str):
        insertions = [insertions]

    functions = strip_from_list(functions)
    insertions = strip_from_list(insertions)

    function_redaction = ""
    insertion_redaction = ""

    # Add function to redaction
    if len(functions) == 1:
        function_redaction = f"Su función es la de " + functions[0].lower()
    elif len(functions) > 1:
        for i, function in enumerate(functions):
            if i == 0:
                # First function
                function_redaction = f"Sus funciones son: " + function.lower() + '; '
            elif i == len(functions) - 1:
                # Last function
                function_redaction = function_redaction + "y " + function.lower() + ""
            else:
                # Middle functions.
                function_redaction = function_redaction + function.lower() + "; "

    # Add insertion to redaction
    if len(insertions) > 1:
        insertions = [insertions[0]]

    if insertions:
        insertion_redaction = ". Se inserta " + insertions[0].lower() + "."

    # Redact final
    redaction = ""
    if functions and insertions:
        redaction = function_redaction + insertion_redaction
    elif description:
        redaction = description

    return redaction


def redact_line(name, muscles):
    name_corrected = name.replace("Musculo", "Músculo")
    info = redact_info(name, muscles)
    reference = get_reference(name, muscles)

    redaction = f"**{name_corrected}:** {info} ({reference})" 

    return redaction


def start_redacting_all():
    this_path = os.path.dirname(__file__)
    muscles_path = os.path.join(this_path, 'results.json')

    muscles = read_muscles_file(muscles_path)
    muscles_names = list(muscles.keys())

    with open("redaction.txt", "w+", encoding="utf-8") as f:
        for i, muscle in enumerate(muscles_names):
            line = redact_line(muscle, muscles)
            f.write(line + "\n\n")
            
    # print(get_description(muscles_names[6], muscles))


if __name__ == "__main__":
    os.system('cls')

    start_redacting_all()
    print("Done!")