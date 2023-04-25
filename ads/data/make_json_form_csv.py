import csv
import json

with open('categories.csv') as file:
    categories = list(csv.reader(file))
    del categories[0]

result_1 = []
for category_data in categories:
    result_1.append(
        {
            "model": "ads.category",
            "pk": int(category_data[0]),
            "fields": {
                "name": category_data[1],
            }
        })

with open('../fixtures/categories.json', 'w') as file:
    json.dump(result_1, file)



with open('ads.csv') as file:
    ads = list(csv.reader(file))
    del ads[0]

result_2 = []
for category_data in ads:
    result_2.append(
        {
            "model": "ads.ads",
            "pk": int(category_data[0]),
            "fields": {
                "name": category_data[1],
                'author': category_data[2],
                'price': int(category_data[3]),
                'description': category_data[4],
                'address': category_data[5],
                'is_published': True if category_data[6] == 'TRUE' else False,
            }
        })

with open('../fixtures/ads.json', 'w') as file:
    json.dump(result_2, file)
