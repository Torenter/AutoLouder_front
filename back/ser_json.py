import json

def to_js(params,folder_name):
    for_result = {}
    for_result['ID'] = folder_name
    for_result['Class'] = params['Class']
    for_result['Name'] = params['project_name']
    for_result['ExportDate'] = ''
    for_result['Country'] =''
    for_result['Start'] =''
    for_result['End'] =''
    for_result['Client'] = params['Client']
    for_result['Folder'] = params['folder']
    to_connect = {}
    to_connect['result'] = [for_result]
    with open("{}.json.done".format(folder_name), "w") as write_file:
        json.dump(to_connect, write_file)
if __name__ == "__main__":
    print('Должен быть импортирован')