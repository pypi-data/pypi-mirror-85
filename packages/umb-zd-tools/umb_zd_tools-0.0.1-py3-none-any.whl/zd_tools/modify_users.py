from pathlib import Path
import bulk_actions_users as bulk
import sys
import getopt

arg_help = """
Input File:
    .csv file: The best way to create one is by creating a Personal View in Zendesk and exporting it.

Commands:
    delete: permanently delete all users
    org-join-[organization_id]: Add all users to the specified end-user organization.
    list-[admin/agent]: list all users with the given role.
"""


def main(argv):
    file_path = None
    cmd = None
    try:
        try:
            opts, args = getopt.getopt(argv, 'i:c:', ['input=', 'cmd='])
            print(opts, args)
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-i", "--input"):
                file_path = str(Path.home()) + '/' + arg
            elif opt in ("-c", "--cmd"):
                cmd = arg
        if (not file_path and 'list' not in cmd) or not cmd:
            print('modify_users.py -i <inputfile> -c <command>')
            print(arg_help)
            sys.exit(2)
        if 'list' not in cmd:
            ticket_file = open(file_path, 'r')
            manager = bulk.ManageUsers(file_object=ticket_file,
                                       sb_or_zd='zd',
                                       bfg_or_zd='zd_id')
        else:
            manager = bulk.ManageUsers(file_object=None,
                                       sb_or_zd='zd',
                                       bfg_or_zd='zd_id')
    except FileNotFoundError:
        print('File Not Found. ({})'.format(file_path))
        print('\nMake sure it is in your home folder, check spelling and try again. \nExiting.')
        sys.exit()

    if 'org-join' in cmd:
        manager.update_many(payload={'user': {'organization_id': cmd.split('-')[2]}})
    elif 'list' in cmd:
        if 'both' in cmd:
            query = 'role:admin role:agent'
        else:
            query = 'role:' + cmd.split('-')[1]
        [print("('"+user['email'].split('@')[0]+"', "+str(user['id'])+'),') for user in manager.search(query=query)]
    elif 'delete' in cmd:
        manager.delete_many()


if __name__ == '__main__':  main(sys.argv[1:])
