from requests_html import HTMLSession

url = 'https://playtennis.usta.com/tournaments?location=37220,%20TN&level-category=junior&distance=200&tournament-level[,]=00000000-0000-0000-0000-000000000003,00000000-0000-0000-0000-0000000000b3,00000000-0000-0000-0000-000000000004,00000000-0000-0000-0000-0000000000b4,00000000-0000-0000-0000-000000000005,00000000-0000-0000-0000-0000000000b5,00000000-0000-0000-0000-000000000006&event-division-gender[,]=boys'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=1)
print(r.status_code)

tournaments = r.html.find('div.csa-search-result-item')

for tourney in tournaments:
    title = tourney.find('h3.csa-title', first=True).text
    date = tourney.find('li.csa-date-v2', first=True).text
    dist = tourney.find('span.csa-distance.m-xs', first=True).text
    status = tourney.find('p.csa-status', first=True).text
    level = title[:7]

    ov = {
        'title': title,
        'date': date,
        'dist': dist,
        'status': status,
        'level': level
    }

    print(ov)






