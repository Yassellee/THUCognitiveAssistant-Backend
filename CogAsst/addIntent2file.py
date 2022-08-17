import codecs
import csv
import manage       


file_path = 'intent2db.csv'

def addIntent2file():
    file = open(file_path, 'a+', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    # csv_writer.writerow([f'Name', 'Entity'])
    csv_writer.writerow(['体育馆预约', "{'体育馆': ['体育馆名称', '体育场地'], 'datetimeV2': 0}"])
    file.close()


addIntent2file()
