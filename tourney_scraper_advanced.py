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

#dictionary of tournament title:tournament id
ts = {}
#overview of tournament and players
ov_list = []

#def point_sys(level, range, points):



#gets tournament title and id from USTA main and appends to ts
for tourney in res_dict['searchResults']:
    points_t = 0
    t_title = tourney['item']['name']
    range_t = float(tourney['distance'])
    id = tourney['item']['id']
    level_full = tourney['item']['level']['name']
    level_s = level_full[:7]


    if level_s == "Level 4" or level_s == "Level 3":
        points_t += 60
    elif level_s == "Level 5":
        points_t += 35
    elif level_s == "Level 6":
        points_t += 20
    
    if range_t <= 120.0:
        points_t += 40
    elif 120.0 < range_t <= 200.0:
        points_t += 25


    ts[t_title] = id, level_s, points_t, range_t

#gets players for each tournament and appends them to ov_list
for each_title, each_id in ts.items():
    players_list = {}
    specific_url = "https://prd-usta-kube-tournaments.clubspark.pro/"


    payload = {
        "operationName": "GetPlayers",
        "variables": {
            "id": each_id[0],
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
    for player_info in items_list:
        playerName = player_info['playerName']
        playerGender = player_info['gender']
        playerEvents = player_info['events']
        for events in playerEvents:
            playerDivision = events['division']['ageCategory']['todsCode']
            if playerGender == "MALE" and playerDivision == "U16":
                players_list[playerName] = playerGender, playerDivision

    ov_list.append({"Title": each_title, "Level": each_id[1], "Points": each_id[2], "Range": each_id[3], "Names": players_list})

sorted_list = sorted(ov_list, key=lambda x: x['Points'], reverse=True)
df = pd.DataFrame(sorted_list)
df.to_csv('players.csv')
print("Players to CSV")
