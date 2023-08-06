import sys
import requests
import json
import os
import time

headers = {'content-type': 'application/json'}

zd_pw = os.environ.get('PRODUCTION_TOKEN')
zd_email = os.environ.get('PRODUCTION_EMAIL') + '/token'
sb_pw = os.environ.get('SANDBOX_TOKEN')
sb_email = os.environ.get('SANDBOX_EMAIL') + '/token'


class EndpointBuilder:
    class Domain:
        sb = 'https://'+os.environ.get('SANDBOX_SUBDOMAIN') + '.zendesk.com'
        zd = 'https://'+os.environ.get('PRODUCTION_SUBDOMAIN') + '.zendesk.com'

    class Query:
        bfg_id = 'external_ids={}'
        zd_id = 'ids={}'
        s_tickets = 'type:ticket '
        s_users = 'type:user '
        s_groups = 'type:group '
        s_agent = 'role: agent'
        side_load_tickets = '?include=tickets'
        side_load_last_audits = '?include=last_audits'

    class Endpoint:
        # https://developer.zendesk.com/rest_api/docs/support/job_statuses#show-job-status
        get_job_status = '/api/v2/job_statuses/{}.json'

        # https://developer.zendesk.com/rest_api/docs/support/users#update-many-users
        put_update_many_users = '/api/v2/users/update_many.json?'

        # https://developer.zendesk.com/rest_api/docs/support/users#create-or-update-many-users
        post_create_update_many_users = '/api/v2/users/create_or_update_many.json'

        # https://developer.zendesk.com/rest_api/docs/support/users#create-user
        post_create_user = '/api/v2/users.json'

        # https://developer.zendesk.com/rest_api/docs/support/tickets#create-many-tickets
        post_create_many_tickets = '/api/v2/tickets/create_many.json'

        # https://developer.zendesk.com/rest_api/docs/support/incremental_export#incremental-ticket-export
        get_tickets_incremental = '/api/v2/incremental/tickets/cursor.json?start_time={}'

        # https://developer.zendesk.com/rest_api/docs/support/search
        get_search = '/api/v2/search.json?query='

        # https://developer.zendesk.com/rest_api/docs/support/users#bulk-deleting-users
        del_bulk_delete_users = '/api/v2/users/destroy_many.json?'

        # https://developer.zendesk.com/rest_api/docs/support/user_identities#create-identity
        post_create_identity = '/api/v2/users/{}/identities.json'

        # https://developer.zendesk.com/rest_api/docs/support/user_identities#make-identity-primary
        put_make_identity_primary = '/api/v2/users/{}/identities/{}/make_primary'

        # https://developer.zendesk.com/rest_api/docs/support/users#show-many-users
        get_show_many_users = '/api/v2/users/show_many.json?'

        # https://developer.zendesk.com/rest_api/docs/support/user_identities#make-identity-primary
        get_list_identities = '/api/v2/users/{}/identities.json'

        # https://developer.zendesk.com/rest_api/docs/support/tickets#bulk-delete-tickets
        del_bulk_delete_tickets = '/api/v2/tickets/destroy_many.json?ids={}'

        # https://developer.zendesk.com/rest_api/docs/support/tickets#update-many-tickets
        put_update_many_tickets = '/api/v2/tickets/update_many.json?ids={}'

        # https://developer.zendesk.com/rest_api/docs/support/tickets#update-many-tickets
        put_batch_update_tickets = '/api/v2/tickets/update_many.json'

        # https://developer.zendesk.com/rest_api/docs/support/users#update-user
        put_update_user = '/api/v2/users/{}.json'

        # https://developer.zendesk.com/rest_api/docs/support/users#delete-user
        del_delete_user = '/api/v2/users/{}.json'

        # https://developer.zendesk.com/rest_api/docs/support/automations#show-automation
        get_automation = '/api/v2/automations/{}.json'

        # https://developer.zendesk.com/rest_api/docs/support/tickets#show-multiple-tickets
        get_many_tickets = '/api/v2/tickets/show_many.json?ids={}'

        # https://developer.zendesk.com/rest_api/docs/support/organizations#update-organization
        put_update_organization = '/api/v2/organizations/{}.json'


class HTTP:
    zd_pw = os.environ.get('PRODUCTION_TOKEN')
    zd_email = os.environ.get('PRODUCTION_EMAIL') + '/token'
    sb_pw = os.environ.get('SANDBOX_TOKEN')
    sb_email = os.environ.get('SANDBOX_EMAIL') + '/token'

    def __init__(self, sb_or_zd):
        self.email = getattr(HTTP, sb_or_zd+'_email')
        self.pw = getattr(HTTP, sb_or_zd+'_pw')
        self.domain = getattr(EndpointBuilder.Domain, sb_or_zd)

    def http_post(self, endpoint, payload):
        r = requests.post(url=endpoint, data=json.dumps(payload), auth=(self.email, self.pw), headers=headers)
        print(endpoint, 'status code:', r.status_code)
        if str(r.status_code).startswith("2"):
            return r.json()
        print(r.json())
        sys.exit()

    def http_put(self, endpoint, payload=None):
        if payload:
            r = requests.put(url=endpoint, data=json.dumps(payload), auth=(self.email, self.pw), headers=headers)
        else:
            r = requests.put(url=endpoint, auth=(self.email, self.pw), headers=headers)
        print(endpoint, 'status code:', r.status_code)
        if str(r.status_code).startswith("2"):
            return r.json()
        if r.status_code == 429:
            return r.json()
        print(r.json())
        sys.exit()

    def http_get(self, endpoint):
        r = requests.get(url=endpoint, auth=(self.email, self.pw))
        print(endpoint, 'status code:', r.status_code)
        if str(r.status_code).startswith("2"):
            return r.json()
        print(r.json())
        sys.exit()

    def http_del(self, endpoint):
        r = requests.delete(url=endpoint, auth=(self.email, self.pw))
        print(endpoint, 'status code:', r.status_code)


class Requests:
    def __init__(self, sb_or_zd):
        self.http = HTTP(sb_or_zd=sb_or_zd)

    def batch_request(self, endpoint, call_type, type, objects=None, payload=None, zendesk_attr=None):
        if type == 'batch':
            Requests.batch(self, endpoint=endpoint, call_type=call_type, payload=payload, zendesk_attr=zendesk_attr)
        elif type == 'many':
            Requests.many(self, endpoint=endpoint, call_type=call_type, objects=objects, payload=payload)

    def bulk_put(self, call_type, endpoint, payload, stop_at, j):
        job_statuses = []
        broken_jobs = []
        print(json.dumps(payload, sort_keys=True, indent=4))
        r = getattr(self.http, call_type)(endpoint=endpoint, payload=payload)
        if r.get('error', None) != 'TooManyJobs' and j == stop_at:
            job_statuses.append(r['job_status']['id'])
        if r.get('error', None) == 'TooManyJobs' or j == stop_at:
            # Check job statuses after all calls (or too many calls) are made.
            for job in job_statuses:
                job_status = False
                x = 0
                while not job_status:
                    x += 1
                    job_status = Requests.status_checker(self, job_id=job)
                    if x == 12:
                        broken_jobs.append(job)
                        break
        else:
            job_statuses.append(r['job_status']['id'])
        return broken_jobs

    def batch(self, endpoint, call_type, payload, zendesk_attr):
        len_payload = len(payload)
        for i in range(0, len_payload, 100):
            j = min(i + 100, len_payload)  # Increment through 100 update items at a time
            if call_type == 'http_put':
                updates = {zendesk_attr: payload[i:j]}
                Requests.bulk_put(self,
                                  payload=updates,
                                  call_type=call_type,
                                  endpoint=endpoint,
                                  stop_at=len_payload,
                                  j=j)

    def many(self, endpoint, call_type, objects, payload):
        broken_jobs = []
        r = []

        len_objects = len(objects)
        for i in range(0, len_objects, 100):

            j = min(i + 100, len_objects)  # Increment through 100 ids at a time
            if call_type == 'http_put':
                broken_jobs += Requests.bulk_put(self,
                                                 call_type=call_type,
                                                 endpoint=endpoint.format(','.join(objects[i:j])),
                                                 payload=payload,
                                                 stop_at=len_objects,
                                                 j=j)
            elif call_type == 'http_get':
                r += getattr(self.http, call_type)(endpoint=endpoint.format(','.join(objects[i:j])))
            else:
                r = getattr(self.http, call_type)(endpoint=endpoint.format(','.join(objects[i:j])))

        if call_type == 'http_put':
            return broken_jobs
        return r

    def status_checker(self, job_id):
        while True:
            url = self.http.domain + EndpointBuilder.Endpoint.get_job_status.format(job_id)
            status = self.http.http_get(url)['job_status']['status']
            print('Job status:', status)
            if status == 'completed':
                return True
            if status == 'failed':
                return False
            if status == 'working' or status == 'queued':
                for i in range(15, 0, -1):
                    print('Checking again in {} seconds.'.format(i))
                    time.sleep(1)