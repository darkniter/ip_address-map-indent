import json
import os
import config
import re
from main import json_output


def main():
    oz = json_input(config.OZ_JSON)
    broken = json_input(config.BROKENOZ_JSON)
    exclude, model_not_equal = found_doubles(oz, broken)

    # json_output('old_ip_comparse', old_ip_comparse)
    json_output('compars_oz_lost',lost(oz, exclude, 'oz'))
    json_output('compars_broken_lost',lost(broken, exclude, 'broken'))
    json_output('compars_model_not_equal',model_not_equal)
    return exclude


def lost(file_name, exclude, name):
    losted = {}
    for record in file_name:
        if not (' '.join([file_name[record][0],file_name[record][1]]) in exclude) and not bool(file_name[record][19]):
            losted.update({' '.join([file_name[record][0],file_name[record][1]]):{'record_' + name:file_name[record]}})
    return losted

def found_doubles(oz, broken):
    coincidence = {}
    model_not_equal = {}
    # old_ip_comparse = {}
    # count = 0

    for record_oz in oz:
        for record_broken in broken:

            broken[record_broken][7] = re.sub('[-,:.]','',broken[record_broken][7].lower())
            oz[record_oz][7] = re.sub('[-,:.]','',oz[record_oz][7].lower())

            if ((broken[record_broken][3] == oz[record_oz][3] and broken[record_broken][3] != '')
            or (broken[record_broken][4] == oz[record_oz][4] and broken[record_broken][4] != '') and
            broken[record_broken][7] == oz[record_oz][7]

            # not bool(oz[record_oz][19]) and
            # not bool(broken[record_broken][19])
            ):
                coincidence.update({
                    ' '.join([oz[record_oz][0],oz[record_oz][1]]):{
                    'record_oz':oz[record_oz],
                    'record_broken':broken[record_broken]
                    }
                    })

                if not (oz[record_oz][2] == broken[record_broken][2]):
                    model_not_equal.update( {
                    ' '.join([oz[record_oz][0],oz[record_oz][1]]):{
                    'record_oz':oz[record_oz],
                    'record_broken':broken[record_broken]
                    }
                    })

    return coincidence, model_not_equal


def json_input(object_csv):
    with open(object_csv,'r',encoding='utf-8-sig') as csv:
        file_obj = json.load(csv)
    return file_obj

if __name__ == "__main__":
    json_output('comparse_file',main())
