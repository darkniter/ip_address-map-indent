import json
import os
import config
import re
from main import json_output


def main():
    oz = json_input(config.OZ_JSON)
    broken = json_input(config.BROKENOZ_JSON)
    exclude = found_doubles(oz, broken)
    json_output('compars_oz_lost',lost(oz, exclude, 'oz'))
    json_output('compars_broken_lost',lost(broken, exclude, 'broken'))
            # [3,4,7]
    return exclude


def lost(file_name, exclude,name):
    losted = {}
    for record in file_name:
        if not file_name[record][0]+file_name[record][1] in exclude:
            losted.update({' '.join([file_name[record][0],file_name[record][1]]):{name:file_name[record]}})
    return losted

def found_doubles(oz, broken):
    coincidence = {}
    for record_oz in oz:
        for record_broken in broken:
            broken[record_broken][7] = re.sub('[-,:.]','',broken[record_broken][7].lower())
            # oz[record_oz][7] = oz[record_oz][7].lower()
            oz[record_oz][7] = re.sub('[-,:.]','',oz[record_oz][7].lower())
            if (broken[record_broken][3] == oz[record_oz][3] and
            broken[record_broken][4] == oz[record_oz][4] and
            broken[record_broken][7] == oz[record_oz][7]):
                coincidence.update({
                    ' '.join([oz[record_oz][0],oz[record_oz][1]]):{
                    'record_oz':oz[record_oz],
                    'record_broken':broken[record_broken]
                    }
                    })
    return coincidence


def json_input(object_csv):
    with open(object_csv,'r',encoding='utf-8-sig') as csv:
        file_obj = json.load(csv)
    return file_obj

if __name__ == "__main__":
    json_output('compars_file_compars',main())
