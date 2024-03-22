
import csv
import re


file_csv = 'phonebook_raw.csv'

def anti_chaos(file):
    with open(file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)  #
    nested_list = []

    for contact in contacts_list:
        contact_info = []
        for info in contact:
            contact_info.append([info])
        nested_list.append(contact_info)

    for contact in nested_list:
        full_name = contact[0][0]
        names = full_name.split()
        full_firstname = contact[1][0]
        firstnames = full_firstname.split()

        if len(names) == 3:
            contact[0] = [names[0]]
            contact[1] = [names[1]]
            contact[2] = [names[2]]
        elif len(names) == 2:
            contact[0] = [names[0]]
            contact[1] = [names[1]]
            contact[2] = ['']
        elif len(names) == 1:
            contact[0] = [names[0]]
            contact[1] = [''] if not contact[1] else contact[1]
            contact[2] = [''] if not contact[2] else contact[2]

        if len(firstnames) == 2:
            contact[1] = [firstnames[0]]
            contact[2] = [firstnames[1]]

    for contact in nested_list:
        try:
            contact[5] = re.sub(
                r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб.)?[\s]*(\d+)*[\)]*',
                r'+7(\2)-\3-\4-\5 \6\7',
                str(contact[5])
            )
        except TypeError:
            contact[5] = ''

    dict_contacts = {}
    for contact in nested_list[0:]:
        key = (contact[0][0], contact[1][0])
        if key not in dict_contacts:
            value = (contact[2][0], contact[3][0], contact[4][0], contact[5][2:-2], contact[6][
                0])
            dict_contacts[key] = value
        elif key in dict_contacts.keys():
            value = (contact[2][0], contact[3][0], contact[4][0], contact[5][2:-2], contact[6][0])
            new_value = []
            for q, w in zip(dict_contacts[key], value):
                if q == w:
                    new_value.append(q)
                elif q == '' and w != '':
                    new_value.append(w)
                elif q != '' and w == '':
                    new_value.append(q)
                else:
                    new_value.append('')
            dict_contacts[key] = tuple(new_value)

    final_list = []
    for key, value in dict_contacts.items():
        contact_list = list(key) + list(value)
        final_list.append(contact_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_list)
