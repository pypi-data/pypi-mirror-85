from pathlib import Path
import bulk_actions_users as bulk
import sys

file_path = None
org_id = None
shared = None
try:
    file_path = str(Path.home()) + '/' + list(sys.argv)[1]
    org_id = str(list(sys.argv)[2])
    shared = bool(list(sys.argv)[3])
    user_file = open(file_path, 'r')
except FileNotFoundError:
    print('File Not Found. ({})'.format(file_path))
    print('\nMake sure it is in your home folder, check spelling and try again. \nExiting.')
    sys.exit()
except IndexError:
    if not file_path:
        print('Run this script with a .csv file as the first argument.')
        print('\nMake sure it is in your home folder, check spelling and try again.')
    if not org_id:
        print('Run this script with the organization ID as the second argument')
    if shared == None:
        print('Run this script with True or False as the third argument')
        print("This determines whether users in this org can see each others' tickets")
    print('\nExiting.')
    sys.exit()

manager = bulk.ManageUsers(file_object=user_file,
                           sb_or_zd='zd',
                           bfg_or_zd='zd_id')

user_ids = manager.lookup_users()
manager.update_many(ids=user_ids, payload={'user': {'organization_id': org_id}})
if shared:
    manager.share_org_tickets(org_id)
