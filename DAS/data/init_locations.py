from bs4 import BeautifulSoup
import urllib.request
from .Location import db_locations
print('ok')
db_locations.create_all()
from .Location import Location


''' This script scrapes all Vietnam districts as (district, province) and puts them in locations.db '''


link = r'https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_%C4%91%C6%A1n_v%E1%BB%8B_h%C3%A0nh_ch%C3%ADnh_c%E1%BA%A5p_huy%E1%BB%87n_c%E1%BB%A7a_Vi%E1%BB%87t_Nam'


raw = urllib.request.urlopen(link).read()
soup = BeautifulSoup(raw)

tables = soup.find_all('table')
tbody = tables[1].find('tbody')
tds = tbody.find_all('td')


i = 0
while i < len(tds):
	i += 1
	district = tds[i].text
	i += 1
	province = tds[i].text
	i += 5
	newLoc = Location(district=district, province=province)
	db_locations.session.add(newLoc)
	try:
		db_locations.session.commit()
	except:
		print(province, state)
		db_locations.session.rollback()

