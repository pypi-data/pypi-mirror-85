import csv
import zd_requests
from zd_requests import EndpointBuilder as ep

writable_fields = [
    'assignee_id',
    'brand_id',
    'collaborator_ids',
    'collaborators',
    'custom_fields',
    'due_at',
    'email_cc_ids',
    'external_id',
    'follower_ids',
    'group_id',
    'macro_ids',
    'organization_id',
    'priority',
    'problem_id',
    'raw_subject',
    'recipient',
    'requester_id',
    'status',
    'subject',
    'submitter_id',
    'tags',
    'ticket_form_id',
    'type',
    'via_followup_source_id',
    ]


class ManageTickets:
    def __init__(self, file_object, sb_or_zd: str, bfg_or_zd: str):
        # opened file object is passed to class on init
        self.file_object = file_object
        # Some Endpoints do not require the bfg_or_zd query
        self.domain = getattr(ep.Domain, sb_or_zd)
        self.query_type = getattr(ep.Query, bfg_or_zd)
        self.id_type = bfg_or_zd
        self.zd = zd_requests.Requests(sb_or_zd)

        # parse the file:
        if isinstance(self.file_object, list) or isinstance(self.file_object, dict):
            self.tickets_to_edit = self.file_object

        else:
            self.ticket_list = [line for line in csv.reader(self.file_object)]
            self.id_list = [ticket[0] for ticket in self.ticket_list]
            self.id_list.pop(0)
            self.tickets_to_edit = ManageTickets.comprehend_payload(self.ticket_list)

    @staticmethod
    def comprehend_payload(ticket_list):
        tickets_to_edit = []
        for i in range(len(ticket_list[1:])):
            tickets_to_edit.append({'id': ticket_list[i + 1][0]})
            for j in range(len(ticket_list[0][1:])):
                col = ticket_list[0][j + 1]
                val = ticket_list[i + 1][j + 1]
                if col == 'email_ccs':
                    ccs = val.split(',')
                    tickets_to_edit[i]['email_ccs'] = [{'user_email': cc} for cc in ccs]
                if col in writable_fields:
                    tickets_to_edit[i].update({col: val})
                else:
                    tickets_to_edit[i]['custom_fields'] = \
                        tickets_to_edit[i].get('custom_fields', []) + [{'id': col,'value': val}]
        return tickets_to_edit



    def log_start(self, verb, noun, lst=None):
        if not lst:
            lst = self.ticket_list
        print('=================================')
        print(verb, noun)
        [print(ticket) for ticket in lst]
        print('=================================')

    def set_many_priorities(self, priority):
        ManageTickets.log_start(self, verb='Setting', noun='Priorities')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.put_update_many_tickets,
                              payload={'ticket': {'priority': priority}},
                              call_type='http_put')

    def delete_many(self):
        ManageTickets.log_start(self, verb='Deleting', noun='Tickets')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.del_bulk_delete_tickets,
                              call_type='http_del')

    def set_many_statuses(self, status):
        if status in ['closed', 'solved']:
            ManageTickets.add_tags(self, tags=['no-sat', 'no-email'])
        ManageTickets.log_start(self, verb='Setting', noun='Statuses')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.put_update_many_tickets,
                              payload={'ticket': {'status': status}},
                              call_type='http_put')

    def add_tags(self, tags):
        ManageTickets.log_start(self, verb='Adding', noun='Tags')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.put_update_many_tickets,
                              payload={'ticket': {'additional_tags': tags}},
                              call_type='http_put')

    def remove_tags(self, tags):
        ManageTickets.log_start(self, verb='Removing', noun='Tags')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.put_update_many_tickets,
                              payload={'ticket': {'remove_tags': tags}},
                              call_type='http_put')

    def batch_update_fields(self):
        ManageTickets.log_start(self, verb='Updating', noun='Fields')
        self.zd.batch_request(endpoint=self.domain + ep.Endpoint.put_batch_update_tickets,
                              payload=self.tickets_to_edit,
                              zendesk_attr='tickets',
                              call_type='http_put',
                              type='batch')

    def set_assignee(self, assignee_id):
        ManageTickets.log_start(self, verb='Adding', noun='Assignee')
        self.zd.batch_request(objects=self.id_list,
                              endpoint=self.domain + ep.Endpoint.put_update_many_tickets,
                              payload={'ticket': {'assignee_id': assignee_id}},
                              call_type='http_put')
