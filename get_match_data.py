import requests, json, time, os

def get_match_data(match_id):
    m_id = str(match_id)
    r = requests.get("https://api.opendota.com/api/matches/" + m_id)
    
    if r.ok:
        print("GET:", m_id)
        data = r.json()
        
        file = open("datafolder" + os.sep + m_id + '_data.json', 'w')
        json.dump(data, file)
        file.close()

#match_id = 6514142739
match_id = 6514162731

for i in range(0, 5000):
    get_match_data(match_id + i)
    time.sleep(2)

#This works, it is slow but it gets matches by their id. Next step is loading
#these json files into pandas dataframes. From then on I can experiment with them.

