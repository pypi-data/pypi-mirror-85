from pathlib import Path
import bulk_actions_tickets as bulk
import sys
import getopt

arg_help = """
Prod:
    y: Production Zendesk Instance
    n: Sandbox Zendesk Instance

Input File:
    .csv file: The best way to create one is by creating a Personal View in Zendesk and exporting it.

Commands:
    delete: permanently delete all tickets
    status-[new/open/pending/hold/solved/closed]: set Status to specified stage 
    priority-[low/normal/high/urgent]: set Priority based on specified level for all tickets
    assignee-[assignee_id]: set the assignee on all tickets to the given ID
    change_many_fields: set fields (columns in input file) to new values (cells) based on id (first column)
"""


def main(argv):
    file_path = None
    cmd = None
    zd_or_sb = None
    try:
        try:
            opts, args = getopt.getopt(argv, 'p:i:c:', ['prod=', 'input=', 'cmd='])
            print(opts, args)
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-i', '--input'):
                file_path = str(Path.home()) + '/' + arg
            elif opt in ('-c', '--cmd'):
                cmd = arg
            elif opt in ('-p', '--prod'):
                if arg == 'y':
                    zd_or_sb = 'zd'
                else:
                    zd_or_sb = 'sb'
        if not file_path or not cmd or not zd_or_sb:
            print('modify_tickets.py -p <y/n> -i <inputfile> -c <command>')
            print(arg_help)
            sys.exit(2)
        ticket_file = open(file_path, 'r')
    except FileNotFoundError:
        print('File Not Found. ({})'.format(file_path))
        print('\nMake sure it is in your home folder, check spelling and try again. \nExiting.')
        sys.exit()

    manager = bulk.ManageTickets(file_object=ticket_file,
                                 sb_or_zd=zd_or_sb,
                                 bfg_or_zd='zd_id')

    if 'status' in cmd:
        status = cmd.split('-')[1]
        manager.set_many_statuses(status=status)
    elif 'priority' in cmd:
        priority = cmd.split('-')[1]
        manager.set_many_priorities(priority=priority)
    elif 'assignee' in cmd:
        assignee = cmd.split('-')[1]
        manager.set_assignee(assignee_id=assignee)
    elif 'delete' in cmd:
        manager.delete_many_tickets()
    elif 'add-tags' in cmd:
        tag = cmd.split('-')[-1]
        manager.add_tags(tags=[tag])
    elif 'del-tags' in cmd:
        tag = cmd.split('-')[-1]
        manager.remove_tags(tags=[tag])
    elif 'change_many_fields' in cmd:
        manager.batch_update_fields()


if __name__ == '__main__':  main(sys.argv[1:])
