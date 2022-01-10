import requests
res = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
dict_covid = res.json()
new_case = dict_covid[0]['new_case']
total_case = dict_covid[0]['total_case']
new_death = dict_covid[0]['new_death']
total_death = dict_covid[0]['total_death']
new_recovered = dict_covid[0]['new_recovered']
update_date = dict_covid[0]['update_date']

print(dict_covid[0])