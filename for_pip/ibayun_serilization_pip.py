import re

PRIMITIVE_TYPES = [
    int,
    float,
    complex,
    str,
    bool
]
CONTAINER_TYPES = [
    list,
    tuple,
    set,
    frozenset
]
DICTIONARY_TYPES = [
    dict
]

PRIMITIVE_REGEX = re.compile(r"^\((.+?)\)([^(])$")
CONTAINER_REGEX = re.compile(r"^\((.{8}[^d].+?)\)(.+?;)$")
DICTIONARY_REGEX = re.compile(r"^\((.+?)\)(.+?);$")
FIND_REGEX_CONTAINER = re.compile(r"\((.+?)\)(.+?);")
FIND_REGEX_DICTIONARY = re.compile(r"\((.+?)\)(.+?):\((.+?)\)(.+?);")


def parse_type(str_type):
    if str_type == "<class 'str'>":
        return str
    elif str_type == "<class 'float'>":
        return float
    elif str_type == "<class 'int'>":
        return int
    elif str_type == "<class 'list'>":
        return list
    elif str_type == "<class 'set'>":
        return set
    elif str_type == "<class 'frozenset'>":
        return frozenset
    elif str_type == "<class 'complex'>":
        return complex
    elif str_type == "<class 'tuple'>":
        return tuple
    elif str_type == "<class 'dict'>":
        return dict


def dump(obj, fp):
    if type(obj) in PRIMITIVE_TYPES:
        fp.write(f"({type(obj)}){obj}")
    elif type(obj) in CONTAINER_TYPES:
        fp.write(
            "({}){}".format(type(obj),
            " ".join([f"({type(el)}){el};" for el in obj]), )
        )
    elif type(obj) in DICTIONARY_TYPES:
        fp.write(
            "({}){}".format(type(obj),
            " ".join([f"({type(k)}){k}:({type(v)}){v});" for k, v in obj.items()]))
        )


def load(fp):
    lines = fp.readlines()
    for line in lines:
        container_result = []
        dictionary_result = {}
        primitive_regex_result = PRIMITIVE_REGEX.match(line)
        container_regex_result = CONTAINER_REGEX.match(line)
        dictionary_regex_result = DICTIONARY_REGEX.match(line)
        if primitive_regex_result:
            return parse_type(
                primitive_regex_result.group(1)
            )(
                primitive_regex_result.group(2)
            )
        elif container_regex_result:
            for el in re.finditer(FIND_REGEX_CONTAINER,
                                  container_regex_result.group(2)):
                value = parse_type(el.group(1))(el.group(2))
                container_result.append(value)
            return parse_type(container_regex_result.group(1))\
                (container_result)
        elif dictionary_regex_result:
            for el in re.finditer(FIND_REGEX_DICTIONARY,
                                  dictionary_regex_result.group(2)):
                key, value = "{}".format(parse_type(el.group(1))(el.group(2))),\
                             "{}".format(parse_type(el.group(3))(el.group(4)))
                dictionary_result[key] = value
            return dictionary_result


if __name__ == "__main__":
    new_txt = open('forserialization.txt', 'w')
    set_test = {2, 3, 4}
    int_test = 2
    list_test = (2, 3, "4", True)
    tuple_test = [2, 3, 5, 5.3]
    frozenset_test = frozenset({2, 3, 4})
    complex_test = 4 + 6j
    complex_test_second = complex(4, 6)
    dict_test = {"3": 2, "8": 4, "34": 58, "45": 1}

    dump(set_test, new_txt)
    new_txt.write("\n")
    dump(int_test, new_txt)
    new_txt.write("\n")
    dump(list_test, new_txt)
    new_txt.write("\n")
    dump(tuple_test, new_txt)
    new_txt.write("\n")
    dump(frozenset_test, new_txt)
    new_txt.write("\n")
    dump(complex_test, new_txt)
    new_txt.write("\n")
    dump(complex_test_second, new_txt)
    new_txt.write("\n")
    dump(dict_test, new_txt)
    new_txt.write("\n")

    new_txt.close()
    with open("tmp.txt") as f:
        b = load(f)
        print(type(b), b)
