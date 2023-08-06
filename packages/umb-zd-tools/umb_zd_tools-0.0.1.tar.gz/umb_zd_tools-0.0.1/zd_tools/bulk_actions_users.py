import zd_requests as zd
from zd_requests import EndpointBuilder as ep
import csv


class EP(ep):
    post_create_update_many_users = '/api/v2/users/create_or_update_many.json'


class ManageUsers:
    def __init__(self, sb_or_zd: str, bfg_or_zd: str, file_object=None):
        # opened file object is passed to class on init
        if file_object:
            self.file_object = file_object
            # parse the file:
            self.user_list = [line for line in csv.reader(self.file_object)]
            try:
                if self.id_type == 'zd_id':
                    try:
                        self.id_col = self.user_list[0].index('id')
                    except ValueError:
                        self.id_col = self.user_list[0].index('ID')
                elif self.id_type == 'bfg_id':
                    self.id_col = self.user_list[0].index('external_id')
                else:
                    raise AttributeError
            except ValueError:
                print('Problem loading file headers. Oh well, lets try it anyway.')
                pass

            self.email_col = self.user_list[0].index('email')
            self.cec_col = self.user_list[0].index('cec')
            self.user_list = self.user_list[1:]
            self.ids = [uid[self.id_col] for uid in self.user_list]

        # Some Endpoints do not require the bfg_or_zd query
        self.domain = getattr(ep.Domain, sb_or_zd)
        self.query_type = getattr(ep.Query, bfg_or_zd)
        self.id_type = bfg_or_zd





    def log_start(self, verb, noun, lst=None):
        if not lst:
            lst = self.user_list
        print('=================================')
        print(verb, noun)
        [print(user) for user in lst]
        print('=================================')

    def lookup_users(self):
        ManageUsers.log_start(self, verb='Searching for', noun='Users by Email')
        res = []
        if len(self.user_list[0]) > 1:
            for email in [user[self.cec_col]+'@cisco.com' for user in self.user_list]:
                try:
                    r = zd.HTTP.http_get(endpoint=self.domain +
                                         ep.Endpoint.get_search +
                                         ep.Query.users +
                                         email)['results'][0]
                    if r['role'] == 'end-user':
                        res.append(str(r['id']))
                    else:
                        print('Will skip deletion of {}. Cisco account is an Agent.'.format(email))
                except IndexError:
                    print('{} does not have a Cisco account provisioned in Zendesk'.format(email))
                    # If the user has no cisco account provisioned in Zendesk, move on to the next user.
                    continue
            return res
        new = []
        for user in self.user_list:
            if user:
                try:
                    res.append(str(zd.HTTP.http_get(endpoint=ep.Domain.zd +
                                                    ep.Endpoint.get_search +
                                                    ep.Query.s_users + user[0])['results'][0]['id']))
                except IndexError:
                    new.append(user[0].strip())
        if new:
            ManageUsers.create_many(self, emails=new)
            for user in new:
                res.append(str(zd.HTTP.http_get(endpoint=ep.Domain.zd +
                                                         ep.Endpoint.get_search +
                                                         ep.Query.s_users + user)['results'][0]['id']))
        return res

    @staticmethod
    def create_payload(emails):
        payload = {'users': []}
        payload['users'] += [{'name': user.split('@')[0], 'email': user, 'role': 'end-user'} for user in emails]
        return payload

    def create_many(self, emails=None):
        ManageUsers.log_start(self, verb='Creating', noun='Users', lst=emails)
        if emails:
            payload = ManageUsers.create_payload(emails=emails)
            if len(payload['users']) > 100:
                # TODO Will need to update zd.batch_requests to accept this specific kind of payload (dictionary)
                raise NotImplemented
            else:
                r = zd.HTTP.http_post(endpoint=ep.Domain.zd + EP.post_create_update_many_users,
                                      payload=payload)
                zd.status_checker(r['job_status']['id'])

    def update_many(self, payload):
        ManageUsers.log_start(self, verb='Updating', noun='Users')
        zd.batch_request(objects=self.ids,
                         endpoint=self.domain + ep.Endpoint.put_update_many_users + self.query_type,
                         call_type='http_put',
                         payload=payload)

        print('Update Complete!')

    def share_org_tickets(self, org_id):
        zd.HTTP.http_put(self.domain + ep.Endpoint.put_update_organization.format(org_id),
                         payload={'organization': {'shared_tickets': True, 'shared_comments': True}})

    def suspend_many(self):
        ManageUsers.log_start(self, verb='Suspending', noun='Users')
        zd.batch_request(objects=[user[self.id_col] for user in self.user_list],
                         endpoint=self.domain + ep.Endpoint.put_update_many_users + self.query_type,
                         payload={'user': {'suspended': True}},
                         call_type='http_put')

        print('Suspension Complete!')

    def delete_many(self, ids=None):
        ManageUsers.log_start(self, verb='Deleting', noun='Users')
        if not ids:
            ids = self.ids
        zd.batch_request(objects=ids,
                         endpoint=self.domain + ep.Endpoint.del_bulk_delete_users + self.query_type,
                         call_type='http_del')

        print('Deletion Complete!')

    def create_many_identities(self):
        res = []
        ManageUsers.log_start(self, verb='Creating', noun='Identities')
        for user in self.user_list:
            if user:
                cisco_email = user[self.cec_col] + '@cisco.com'
                payload = {'identity':
                           {'type': 'email',
                            'value': cisco_email,
                            'verified': True}
                           }
                print('Adding email:', payload['identity']['value'])

                r = zd.HTTP.http_post(endpoint=self.domain + ep.Endpoint.post_create_identity.format(user[self.id_col]),
                                      payload=payload)
                if r != 422 and r != 404:
                    # http_post returns the status code when
                    # it gets something other than 200. 422 = email already exists
                    res.append((user[self.id_col], r['identity']['id']))
                if r == 404:
                    print('User {} Terminated from Cisco.'.format(payload['identity']['value']))
                else:
                    r = zd.HTTP.http_get(endpoint=self.domain + ep.Endpoint.get_list_identities.format(user[self.id_col]))
                    for identity in r['identities']:
                        if identity['value'] == cisco_email:
                            res.append((user[self.id_col], identity['id']))
                            break
        print('Update Complete!')
        return res

    def set_many_primary_identities(self, user_tuples):
        print('Setting primary email')
        for user_id, identity_id in user_tuples:
            if user_id:
                print('Setting primary identity for ID:', user_id)
                endpoint = ep.Endpoint.put_make_identity_primary.format(user_id, identity_id)
                zd.HTTP.http_put(endpoint=self.domain + endpoint)

    def search(self, query):
        r = zd.HTTP.http_get(self.domain + ep.Endpoint.get_search + ep.Query.s_users + query)
        url = r['next_page']
        res = r['results']
        while url:
            r = zd.HTTP.http_get(url)
            url = r['next_page']
            res += r['results']

        return res