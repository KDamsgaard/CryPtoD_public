"""
Project CryPtoD,
Copyright PogD april 2021,
Primary author: Kristian K. Damsgaard
"""


from odin.services.db_services import DBServices

"""
RUNNING THIS SCRIPT WILL MAKE EXTENSIVE CHANGES TO DATABASE!
USE WITH CAUTION!
"""

db_services = DBServices()
db = db_services.db
all_pairs = db_services.all_pairs
db.settings.update_one({'_id': 'system_settings'}, {'$set': {'watched_pairs': all_pairs}})


print(db_services.watched_pairs)