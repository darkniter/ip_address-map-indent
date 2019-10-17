import pynetbox
import config
import csv
from transliteration import transliterate
import os
import json
import sys
from Vlan import main as vlan_load

net_box = pynetbox.api(config.NETBOX_URL, config.TOKEN)
csv.field_size_limit(10000000)

def main():

    csv_file, error_csv = excel_map(config.CSV_PATH,config.VLAN_PATH_XL)
    with open(config.PATH_FILTER_XML, 'r', encoding='utf-8-sig') as loaded_map:
        smart_map = json.load(loaded_map)
        smart_map = sort_smart_map(smart_map)
    found, not_found = finder(csv_file,smart_map)

    not_found_hard = scan_broken(found, not_found)

    regions_without_hardware_notbr, not_vlan_notbr = region_founder(not_found)
    regions_without_hardware, not_vlan = region_founder(not_found_hard)

    json_output('Regions_regions_without_hardware_notbr', regions_without_hardware_notbr)
    json_output('Regions_not_vlan_notbr', not_vlan_notbr)
    json_output('Regions_regions_without_hardware', regions_without_hardware)
    json_output('Regions_not_vlan', not_vlan)
    json_output('found', found)
    json_output('work_not_found', not_found)
    json_output('err_csv', error_csv)


    return found,not_found


def region_founder(records):
    found_region = []
    n_found_region = []
    if not os.path.isfile(config.VLAN_PATH_JSON):
        vlan_load()

    with open(config.VLAN_PATH_JSON,'r',encoding='utf-8-sig') as regions:
        regions = json.load(regions)

    for record in records:
        region_tmp = None
        for region in regions:
            for region_child in regions[region]:
                if region != 'description':
                    ip_reg = '.'.join(region_child[4].split('.')[0:3:1])
                    if record.find(ip_reg) !=-1:
                        region_tmp = {record:[records[record], region_child]}
        if region_tmp:
            found_region.append(region_tmp)
        else:
            n_found_region.append({record:records[record]})
    return found_region, n_found_region

def scan_broken(found, not_found):

    if config.BROKENOZ:
        csvOZ, errorOZ = excel_map(config.OZ, config.OZ_JSON)
        csv_file, error_csv = excel_map(config.BROKENOZ, config.BROKENOZ_JSON)
        json_output('work_err_broken', error_csv)
        json_output('work_errorOZ', errorOZ)
    if csv_file:
        found_OZ, not_found_OZ = finder(csvOZ, found)
        found_brokenOZ, not_found_brokenOZ = finder(csv_file,found_OZ)
        found_err_broken, not_found_err_broken = finder(csv_file,not_found)


        json_output('work_found_brokenOZ', found_brokenOZ)
        json_output('work_not_found_brokenOZ', not_found_brokenOZ)
        json_output('work_found_err_broken', found_err_broken)
        json_output('work_not_found_err_broken', not_found_err_broken)
        json_output('work_found_OZ', found_OZ)

    return not_found_err_broken

def json_output(fname,file_object):
    if (os.path.isfile(config.DIR + fname + '.json')):
        os.remove(config.DIR + fname + '.json')

    json_file = open(config.DIR + fname + '.json', 'a+', encoding='utf-8-sig')
    json_file.write(json.dumps(file_object))
    json_file.close()
    print(fname + ' done')


def finder(csv,xml):
    not_found = {}
    found = {}
    for dev in xml:
        if dev in csv:
            found.update({dev:[xml[dev],csv[dev],'found_mark']})

        else :
            not_found.update({dev: xml[dev]})


    return found, not_found

def sort_smart_map(smart_map):
    result = {}
    for row in smart_map:
        result.update({smart_map[row].get('address'): smart_map[row]})
    return result


def hint_init(hint, val):
    result = {}
    count = -1
    if len(hint) == len(val):
        for element in hint.keys():
            count += 1
            if element.find('RESERVED') == -1:
                result.update({element: val[count]})
        return result


def excel_map(fname_info,fname_result):
    if os.path.isfile(fname_result):
        os.remove(fname_result)

    err = {}

    map_xl = {}
    csv.register_dialect('csv', delimiter=';', quoting=csv.QUOTE_NONE)
    with open(fname_info, 'r') as xl:
        result = csv.reader(xl, 'csv')
        for row in result:
            init_name = row[0]
            if init_name != 'P_STREET':

                if len(row[4])>6:
                    map_xl.update({row[4]: row})
                elif len(row[3])>6:
                    map_xl.update({row[3]: row})
                else:
                    err.update({'err'+ row[0] + row[1]: row})

    json_file = open(fname_result, 'a+', encoding='utf-8-sig')
    json_file.write(json.dumps(map_xl))
    # json_file.write(json.dumps(err))
    json_file.close()

    return map_xl, err

if __name__ == "__main__":
    main()

    pass