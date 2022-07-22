import requests
import pandas as pd
import json
import requests

url = "https://prd-usta-kube.clubspark.pro/unified-search-api/api/Search/tournaments/Query"

querystring = {"indexSchema":"tournament"}

payload = {
    "options": {
        "size": 100,
        "from": 0,
        "sortKey": "date",
        "latitude": 36.07427978515625,
        "longitude": -86.76791381835938
    },
    "filters": [
        {
            "key": "organisation-id",
            "items": []
        },
        {
            "key": "location-id",
            "items": []
        },
        {
            "key": "region-id",
            "items": []
        },
        {
            "key": "publish-target",
            "items": [{"value": 1}]
        },
        {
            "key": "level-category",
            "items": [{"value": "junior"}],
            "operator": "Or"
        },
        {
            "key": "organisation-group",
            "items": [],
            "operator": "Or"
        },
        {
            "key": "date-range",
            "items": [
                {
                    "minDate": "2022-07-21T00:00:00.000Z",
                    "maxDate": "2022-08-31T23:59:59.999Z"
                }
            ],
            "operator": "Or"
        },
        {
            "key": "distance",
            "items": [{"value": 200}],
            "operator": "Or"
        },
        {
            "key": "tournament-level",
            "items": [{"value": "00000000-0000-0000-0000-000000000003"}, {"value": "00000000-0000-0000-0000-0000000000b3"}, {"value": "00000000-0000-0000-0000-000000000004"}, {"value": "00000000-0000-0000-0000-0000000000b4"}, {"value": "00000000-0000-0000-0000-000000000005"}, {"value": "00000000-0000-0000-0000-0000000000b5"}, {"value": "00000000-0000-0000-0000-000000000006"}, {"value": "00000000-0000-0000-0000-000000000003"}, {"value": "00000000-0000-0000-0000-0000000000b3"}, {"value": "00000000-0000-0000-0000-000000000004"}, {"value": "00000000-0000-0000-0000-0000000000b4"}, {"value": "00000000-0000-0000-0000-000000000005"}, {"value": "00000000-0000-0000-0000-0000000000b5"}, {"value": "00000000-0000-0000-0000-000000000006"}],
            "operator": "Or"
        },
        {
            "key": "event-division-gender",
            "items": [{"value": "boys"}, {"value": "boys"}, {"value": "boys"}],
            "operator": "Or"
        },
        {
            "key": "event-ntrp-rating-level",
            "items": [],
            "operator": "Or"
        },
        {
            "key": "event-division-age-category",
            "items": [],
            "operator": "Or"
        },
        {
            "key": "event-division-event-type",
            "items": [],
            "operator": "Or"
        },
        {
            "key": "event-court-location",
            "items": [],
            "operator": "Or"
        }
    ]
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://playtennis.usta.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://playtennis.usta.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring).text
res_dict = json.loads(response)

#ts = {"titles": [], "ids": []}
ts = {}
ov_list = []

for tourney in res_dict['searchResults']:
    t_title = tourney['item']['name']
    range = tourney['distance']
    #url = tourney['item']['url']
    id = tourney['item']['id']
    #print(name)
    ts[t_title] = id
    #ts["ids"].append(id)
    #ts["titles"].append(t_title)
    #print(range)

#print(ids)

for each_title, each_id in ts.items():
    players_list = []
    specific_url = "https://prd-usta-kube-tournaments.clubspark.pro/"


    payload = {
        "operationName": "GetPlayers",
        "variables": {
            "id": each_id,
            "queryParameters": {
                "limit": 0,
                "offset": 0,
                "sorts": [
                    {
                        "property": "playerLastName",
                        "sortDirection": "ASCENDING"
                    }
                ],
                "filters": []
            }
        },
        "query": """query GetPlayers($id: UUID!, $queryParameters: QueryParametersPaged!) {
    paginatedPublicTournamentRegistrations(
        tournamentId: $id
        queryParameters: $queryParameters
    ) {
        totalItems
        items {
        firstName: playerFirstName
        gender: playerGender
        lastName: playerLastName
        city: playerCity
        state: playerState
        playerName
        playerId {
            key
            value
            __typename
        }
        playerCustomIds {
            key
            value
            __typename
        }
        eventEntries {
            eventId
            players {
            firstName
            lastName
            customId {
                key
                value
                __typename
            }
            customIds {
                key
                value
                __typename
            }
            __typename
            }
            __typename
        }
        events {
            id
            division {
            ballColour
            gender
            ageCategory {
                todsCode
                minimumAge
                maximumAge
                type
                __typename
            }
            eventType
            wheelchairRating
            familyType
            ratingCategory {
                ratingType
                ratingCategoryType
                value
                minimumValue
                maximumValue
                __typename
            }
            __typename
            }
            level {
            name
            category
            __typename
            }
            formatConfiguration {
            ballColour
            drawSize
            entriesLimit
            eventFormat
            scoreFormat
            selectionProcess
            __typename
            }
            __typename
        }
        __typename
        }
        __typename
    }
    }
    """
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://playtennis.usta.com/",
        "content-type": "application/json",
        "Origin": "https://playtennis.usta.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }
    players_json = requests.request("POST", specific_url, json=payload, headers=headers).text
    p_list = json.loads(players_json)
    items_list = p_list['data']['paginatedPublicTournamentRegistrations']['items']
    for name in items_list:
        first_name = name['firstName']
        players_list.append(first_name)

    ov_list.append({"Title": each_title, "Names": players_list})


#print(p_names['Tournament']['Name'])
#print(ov_list)

df = pd.DataFrame(ov_list)
df.to_csv('players.csv')
print("Players to CSV")
