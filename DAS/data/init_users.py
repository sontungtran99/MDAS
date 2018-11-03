from .User import db, User
from .Location import Location, db_locations


def init_user(phonenum, message):
	if message:
		district, province = process(message)
		newUser = User(phonenum=phonenum, district=district, province=province)
		db.session.add(newUser)

		try:
			db.session.commit()
			print('Successfully added {}'.format(newUser))
		except Exception:
			print('Unable to initialize user', newUser)
			db.session.rollback()

def process(msg):
	# Format: [Xã]; [Huyện]; [Tỉnh]

	if msg.count(';') < 2:
		raise Exception('Unknown Format')
	else:
		parts = msg.split(';')
		# Since the last 2 parts are always province and district
		district = parts[len(parts)-2]
		province = parts[-1]
		district, province = fitIntoFormat(district), fitIntoFormat(province)
		if is_valid_loc(district, province):
			return district, province

def fitIntoFormat(loc):
	# Strip unnecessary things and capitalize first character
	loc = loc.lower()
	loc = loc.strip()
	words = loc.split()
	for i in range(len(words)):
		words[i] = words[i][0].upper() + words[i][1:]

	if words[0] in ['Xã', 'Huyện', 'Tỉnh']:
		words = words[1:]
	loc = ' '.join(words)
	return loc

def is_valid_loc(district, province):
	if Location.query.filter_by(district=district, province=province).all():
		return True
	else:
		return False

