from transliteration import transliterate
import csv
import config
import json
import os


def main(filter_region=None):
    csv.register_dialect('csv', delimiter=';', quoting=csv.QUOTE_NONE)
    regions = {}
    with open(config.VLAN_PATH, 'r', encoding='utf-8-sig') as xl:
        result = csv.reader(xl, 'csv')

        for row in result:
            if row[0] !='' and row[1] == '':
                regions.update({transliterate(row[0]): []})
            elif len(row) == 16 and transliterate(row[15]) in regions:
                regions[transliterate(row[15])].append(row)
            else:
                regions.update({'description': row})

    if (os.path.isfile(config.VLAN_PATH_JSON)):
        os.remove(config.VLAN_PATH_JSON)

    json_file = open(config.VLAN_PATH_JSON, 'a+', encoding='utf-8-sig')
    json_file.write(json.dumps(regions))
    json_file.close()


if __name__ == "__main__":
        main()