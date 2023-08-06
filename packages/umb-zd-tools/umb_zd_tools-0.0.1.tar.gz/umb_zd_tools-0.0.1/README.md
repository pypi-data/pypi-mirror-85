# zd_tools Package

This package can be used to reduce the amount of copy/pasting required for scripts that make api calls to Zendesk.

zd_requests includes PUT, GET, DEL and POST functions, as well as a Batch Request function that can be called with any of the HTTP functions using objects=[zd_id1, zd_id2,...], call_type="http_del" etc.

It also includes a class that can facilitate Endpoint construction. EndPointBuilder.Domain.zd runs scripts on the prod instance of Zendesk. EndPointBuilder.Domain.sb runs on the Sandbox. Specific endpoints have been added as needed. 
