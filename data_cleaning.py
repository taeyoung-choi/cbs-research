import csv
import urllib.request
from bs4 import BeautifulSoup

current_courses = {}

with urllib.request.urlopen("https://www8.gsb.columbia.edu/execed/program-finder") as response:
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'class': 'views-table cols-17'})
    courses = table.find_all('div', {'class': 'heading'})
    topics = table.find_all('div', {'class': 'pf_col span_2_of_12 span_1_of_6 span_3_of_4 '})
    for i in range(len(courses)):
        current_courses[courses[i].text.replace('NEW', '').strip()] = topics[i].text.strip()


print(current_courses)
#
# current_courses += ['Columbia Senior Executive Program', 'Columbia Senior Executive Program 2x2 Option',
#                     'Marketing and Innovation', 'Middle Management Program', 'Strategic Problem Solving',
#                     'General Manager Leadership Program', 'EDP: Transition to General Management',
#                     'Negotiation and Decision-Making Strategies', 'Institute for Not-for-Profit Management Program']
#
# with open("data_version_1.csv", 'r', encoding='utf8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     csvreader = list(csvreader)
#     csvfile.close()
#
# with open("clean_data.csv", 'r', encoding='utf8') as csvfile:
#     csvreader2 = csv.reader(csvfile)
#     csvreader2 = list(csvreader2)
#     csvfile.close()
#
#
#
# function = ['administrative', 'customer service', 'engineering', 'finance/ accounting', 'general management',
#             'human resources', 'information systems/ technology', 'legal/compliance', 'manufacturing',
#             'marketing', 'operation', 'other', 'research', 'sales']
#
# position = []
# for i in range(len(csvreader2)):
#     position.append(csvreader2[i][5].lower())
#
# position = set(position)
# print(position)
#
#
# for i in range(len(csvreader)):
#     for j in function:
#         if csvreader[i][4].lower() in j or j in csvreader[i][4].lower():
#             csvreader[i][4] = j
#     for k in position:
#         if csvreader[i][5].lower() in k or k in csvreader[i][5].lower():
#             csvreader[i][5] = k
#     if 'vp' in csvreader[i][5].lower() or 'vice' in csvreader[i][5].lower() or 'v.p' in csvreader[i][5].lower():
#         csvreader[i][5] = 'vice president'
#     elif 'head' in csvreader[i][5].lower() or 'hod' in csvreader[i][5].lower():
#         csvreader[i][5] = 'head of department'
#     elif 'engineer' in csvreader[i][5].lower():
#         csvreader[i][5] = 'engineer'
#     elif 'chief' in csvreader[i][5].lower() or 'c/o' in csvreader[i][5].lower() :
#         csvreader[i][5] = 'chief officer'
#     elif 'senior' in csvreader[i][5].lower() or 'sr' in csvreader[i][5].lower():
#         csvreader[i][5] = 'senior employee'
#     elif 'lead' in csvreader[i][5].lower():
#         csvreader[i][5] = 'leader of department'
#     elif 'dir' in csvreader[i][5].lower():
#         csvreader[i][5] = 'director'
#     elif 'board' in csvreader[i][5].lower():
#         csvreader[i][5] = 'board member'
#     elif 'train' in csvreader[i][5].lower():
#         csvreader[i][5] = 'trainer'
#     elif 'special' in csvreader[i][5].lower() or 'expert' in csvreader[i][5].lower():
#         csvreader[i][5] = 'specialist'
#     elif 'exec' in csvreader[i][5].lower() or 'gm' in csvreader[i][5].lower() or 'md' in csvreader[i][5].lower():
#         csvreader[i][5] = 'executive'
#     elif 'owner' in csvreader[i][5].lower():
#         csvreader[i][5] = 'ceo'
#     elif 'control' in csvreader[i][5].lower() or 'com' in csvreader[i][5].lower():
#         csvreader[i][5] = 'senior employee'
#     elif 'editor' in csvreader[i][5].lower():
#         csvreader[i][5] = 'editor'
#     elif 'principal' in csvreader[i][5].lower():
#         csvreader[i][5] = 'principal employee'
#     elif 'mananger' in csvreader[i][5].lower() or 'manag' in csvreader[i][5].lower() or\
#                     'mang' in csvreader[i][5].lower() or 'pm' in csvreader[i][5].lower():
#         csvreader[i][5] = 'manager'
#     elif 'attorney' in csvreader[i][5].lower() or 'counsel' in csvreader[i][5].lower():
#         csvreader[i][5] = 'lawyer'
#     elif 'analy' in csvreader[i][5].lower():
#         csvreader[i][5] = 'analyst'
#     elif 'treasurer' in csvreader[i][5].lower():
#         csvreader[i][5] = 'treasurer'
#     elif 'investor' in csvreader[i][5].lower():
#         csvreader[i][5] = 'investor'
#     elif 'trader' in csvreader[i][5].lower():
#         csvreader[i][5] = 'trader'
#     elif 'associate' in csvreader[i][5].lower():
#         csvreader[i][5] = 'assistant position'
#     elif 'commander' in csvreader[i][5].lower() or 'colonel' in csvreader[i][5].lower() or \
#                     'brigadier' in csvreader[i][5].lower() or 'sergeant' in csvreader[i][5].lower():
#         csvreader[i][5] = 'military'
#     elif 'rep' in csvreader[i][5].lower():
#         csvreader[i][5] = 'senior employee'
#     elif 'economist' in csvreader[i][5].lower() or 'flocculants' in csvreader[i][5].lower():
#         csvreader[i][5] = 'researcher'
#     elif 'not provided' in csvreader[i][5].lower():
#         pass
#     else:
#         csvreader[i][5] = 'normal employee'
#
# current_list = []
# for i in range(len(csvreader)):
#     if csvreader[i][3] in current_courses:
#         current_list.append(csvreader[i])
#
# print(csvreader)
# print(current_list)
# with open('data_version_2.csv', 'w', newline='', encoding='utf8') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for i in range(len(current_list)):
#         csvwriter.writerow(current_list[i])
#     csvfile.close()
#
# # function2 = []
# for i in range(len(csvreader)):
#     function2.append(csvreader[i][5].lower())
#
# function2 = set(function2)
#
