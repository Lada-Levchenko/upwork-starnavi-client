import csv
import requests

token = "bearer <your token>"
page = 0
names = []
while True:
    # maybe you'll need to change callerOrgId
    response = requests.get('https://www.upwork.com/api/v3/search/public/browse?query=&limit=15&includeGroupRooms=false'
                            '&includeInterviewRooms=false&includeContractRooms=false&includeOneOnOneRooms=false'
                            '&includeCompanyContacts=true&includeOtherContacts=true&includeSubscribedPublicRooms=false'
                            '&includeSubscribe872754503644524544dPrivateRooms=false&includeUnsubscribedPublicRooms=false&sortOrder=desc'
                            '&sortField=time'
                            '&callerOrgId=872754503644524544'
                            '&page={}'.format(page),
                            headers={"Authorization": token})
    users_list = response.json()['2']['lst']
    if users_list[1] == 0:
        break
    for index in range(2, len(users_list) - 1):
        user = users_list[index]['4']['map'][3]
        names.append(user['firstName']['1']['str'] + " " + user['lastName']['1']['str'])
    page += 1

names = list(set(names))    # to remove duplicates
names_with_companies = []
for name in names:
    response = requests.get('https://www.upwork.com/api/v3/search/public/spotlight?limit=1&sortField=time'
                            '&sortOrder=desc&callerOrgId=872754503644524544'
                            '&query={}'.format(name.split(' ')[0]),
                            headers={"Authorization": token})
    results_list = response.json()['1']['lst']
    message = results_list[len(results_list) - 1]['2']['lst'][2]['4']['map'][3]
    if message.get('roomName'):
        name += ', ' + message['roomName']['1']['str']
    names_with_companies.append(name)

with open('names.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows([[name] for name in names_with_companies])
