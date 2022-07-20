from requests_html import HTMLSession

url = 'https://playtennis.usta.com/tournaments?location=37220,%20TN&level-category=junior&distance=200&tournament-level[,]=00000000-0000-0000-0000-000000000003,00000000-0000-0000-0000-0000000000b3,00000000-0000-0000-0000-000000000004,00000000-0000-0000-0000-0000000000b4,00000000-0000-0000-0000-000000000005,00000000-0000-0000-0000-0000000000b5,00000000-0000-0000-0000-000000000006&event-division-gender[,]=boys'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=1)
print(r.status_code)

tournaments = r.html.find('div.csa-results', first=True).absolute_links
#print(tournaments)

for tourney in tournaments:
    r = s.get(tourney)