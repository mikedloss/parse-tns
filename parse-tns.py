import re
import os


def parse_tns(var="", specific=""):
    """
    Reads in a TNS names file (as a string or file) and outputs a dictionary of all possible values.
    :param var: can be a string or file (default is empty string, will look for 'tnsnames.ora' file at the location
                    specified by 'TNS_ADMIN' system variable).
    :param specific: user choice of what keys they want returned. input list needs to be comma separated. if empty, all
                        TNS entries are returned.
    :return: database_dicts: all TNS entries in a clean dictionary.
    :return: database_specific: user choice of what keys they want returned.
    """
    tns = ""
    if var == "":
        if os.environ.get('TNS_ADMIN') is None:
            raise Exception('Cannot find TNS_ADMIN as system variable')
        else:
            try:
                tnsnames = open(os.environ.get('TNS_ADMIN') + "/tnsnames.ora", "r")
            except IOError as err:
                raise IOError('Cannot find tnsnames.ora in TNS_ADMIN location')
            else:
                for each in tnsnames:
                    tns += each
    else:
        if type(var) is file:
            with var as tnsnames:
                for each in tnsnames:
                    tns += each
            var.close()
        elif type(var) is str:
            tns = var

    text = re.sub(r'#[^\n]*\n', '\n', tns)  # remove comments
    text = re.sub(r'( *\n *)+', '\n', text.strip())  # remove excess blank lines

    databases = []
    start = 0
    index = 0
    while index < len(text):
        num_of_parenthesis = 0
        index = text.find('(')  # find first parenthesis
        while index < len(text):
            if text[index] == '(':
                num_of_parenthesis += 1
            elif text[index] == ')':
                num_of_parenthesis -= 1
            index += 1
            if num_of_parenthesis == 0:  # if == 0, we found all parenthesis for tns entry
                break

        databases.append(text[start:index].strip())
        text = text[index:]
        index = 0  # reset for next tns entry

    all_databases = {}
    for each in databases:
        clean = each.replace(" ", "").replace("\n", "")
        database_name = re.match(r'(\w+)\.(\w+)(,\w+)?=', clean).group().strip('=')
        connection_string = clean.replace(database_name, "").strip('=')
        all_databases[database_name] = connection_string

    if specific:
        specific_list = specific.upper().replace(' ', '').split(',')
        list_of_keys = all_databases.keys()
        found_list = []
        database_specific = {}

        for each in specific_list:
            # creates a regex statement to find any instance of 'each' in any of the keys
            reg = re.compile(".*(" + each + ").*")
            # searched the 'list_of_keys' for any instance of 'each' and returns the first instance
            found = [m.group() for i in list_of_keys for m in [reg.search(i)] if m]
            if found:
                for every in found:
                    found_list.append(every)

        for each in found_list:
            database_specific[each] = all_databases[each]

        return database_specific
    else:
        return all_databases
