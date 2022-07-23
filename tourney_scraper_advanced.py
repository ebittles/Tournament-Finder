import requests
import pandas as pd
import json
from datetime import date, timedelta, datetime
import creds
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_new(df):
    message = MIMEMultipart()
    message["Subject"] = "Tournament List"
    message["From"] = creds.sender
    message["To"] = creds.recipient

    html = MIMEText(df.to_html(index=False), "html")
    message.attach(html)
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(creds.sender, creds.password)
        server.sendmail(creds.sender, creds.recipient, message.as_string())

today = date.today()
today_w_sec = datetime.now()
next_month = today + timedelta(days=30)

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
                    "minDate": str(today)+"T00:00:00.000Z",
                    "maxDate": str(next_month)+"T23:59:59.999Z"
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


#gets tournament title and id from USTA main and appends to ts
for tourney in res_dict['searchResults']:
    points_t = 0
    t_title = tourney['item']['name']
    range_t = float(tourney['distance'])
    id = tourney['item']['id']
    url_seg = tourney['item']['organization']['urlSegment']
    url = tourney['item']['url']
    full_url = "https://playtennis.usta.com/Competitions/" + url_seg + url
    level_full = tourney['item']['level']['name']
    level_s = level_full[:7]
    start_date = tourney['item']['startDateTime'][:10]
    sDate_format = datetime.strptime(start_date, '%Y-%m-%d').ctime()
    entries_close = tourney['item']['registrationRestrictions']['entriesCloseDateTime'].replace("T", " ").replace("Z", "")
    close_date = datetime.strptime(entries_close, '%Y-%m-%d %H:%M:%S')


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


    ts[t_title] = id, level_s, points_t, range_t, full_url, close_date, sDate_format

#gets players for each tournament and appends them to ov_list
for each_title, each_id in ts.items():
    players_list = []
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
                players_list.append(playerName)
    if each_id[5] > today_w_sec:
        cDate_format = datetime.ctime(each_id[5])
        ov_list.append({"Date": each_id[6], "Title": each_id[1] +": " + each_title, "Points": each_id[2], "URL": each_id[4], "Entries Close": cDate_format, "Names": players_list})

sorted_list = sorted(ov_list, key=lambda x: x['Points'], reverse=True)
del_points = 'Points'
for t in sorted_list:
    if del_points in t:
        del t[del_points]
df = pd.DataFrame(sorted_list)
df.index += 1

email_new(df)

