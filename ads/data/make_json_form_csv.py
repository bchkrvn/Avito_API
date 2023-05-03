import csv
import json


def create_json(csv_path, json_path, model):
    with open(csv_path) as file:
        dict_ = csv.DictReader(file)
        result = []
        for object_ in dict_:
            object_dict = {
                'model': model,
                'pk': object_['id'],
                'fields': object_
            }
            del object_dict['fields']['id']
            if 'is_published' in object_dict['fields']:
                if object_dict['fields']['is_published'] == 'TRUE':
                    object_dict['fields']['is_published'] = True
                else:
                    object_dict['fields']['is_published'] = False
            result.append(object_dict)

    with open(f'../fixtures/{json_path}', 'w') as file:
        json.dump(result, file, ensure_ascii=False)


create_json('ad.csv', 'ad.json', 'ads.ad')
create_json('category.csv', 'category.json', 'ads.category')
create_json('location.csv', 'location.json', 'ads.location')
create_json('user.csv', 'user.json', 'ads.user')
