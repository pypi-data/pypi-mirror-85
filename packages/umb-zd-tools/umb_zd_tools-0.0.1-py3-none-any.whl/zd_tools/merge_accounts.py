from pathlib import Path
import bulk_actions_users as bulk
import sys

file_path = None
try:
    file_path = str(Path.home()) + '/' + list(sys.argv)[1]
    user_file = open(file_path, 'r')
except FileNotFoundError:
    print('File Not Found. ({})'.format(file_path))
    print('\nMake sure it is in your home folder, check spelling and try again. \nExiting.')
    sys.exit()
except IndexError:
    print('Run this script with a .csv file as an argument.')
    print('\nMake sure it is in your home folder, check spelling and try again. \nExiting.')
    sys.exit()

manager = bulk.ManageUsers(file_object=user_file,
                           sb_or_zd='zd',
                           bfg_or_zd='zd_id')

# First, lookup and delete the @cisco.com addresses that aren't associated with Agent accounts
cisco_ids = manager.lookup_users()
manager.delete_many(cisco_ids)
# Then add a @cisco.com address to the associated account
new_identities = manager.create_many_identities()
# Then make it the primary address
manager.set_many_primary_identities(user_tuples=new_identities)

