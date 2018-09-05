import csv
import requests

page = 0
names = []
while True:
    # maybe you'll need to change callerOrgId
    response = requests.get('https://www.upwork.com/api/v3/search/public/browse?query=&limit=15&includeGroupRooms=false'
                            '&includeInterviewRooms=false&includeContractRooms=false&includeOneOnOneRooms=false'
                            '&includeCompanyContacts=true&includeOtherContacts=true&includeSubscribedPublicRooms=false'
                            '&includeSubscribedPrivateRooms=false&includeUnsubscribedPublicRooms=false&sortOrder=desc'
                            '&sortField=time'
                            '&callerOrgId=872754503644524544'
                            '&page={}'.format(page),
                            headers={"Authorization": "bearer <your token>"})
    users_list = response.json()['2']['lst']
    if users_list[1] == 0:
        break
    for index in range(2, len(users_list) - 1):
        user = users_list[index]['4']['map'][3]
        names.append(user['firstName']['1']['str'] + " " + user['lastName']['1']['str'])
    page += 1

names = list(set(names))    # to remove duplicates
with open('names.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows([[name] for name in names])
