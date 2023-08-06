# python-cyrating

A python wrapper for Cyrating https://www.cyrating.com.

[![Latest PyPI Release](https://img.shields.io/pypi/v/cyrating.svg)](https://pypi.org/project/cyrating/)
[![License](https://img.shields.io/pypi/l/cyrating.svg)](https://github.com/wq/python-requirejs/blob/master/LICENSE)
[![Python Support](https://img.shields.io/pypi/pyversions/cyrating.svg)](https://pypi.org/project/cyrating/)

## Installation
```sh
pip install cyrating
```

Then in your application root directory use the following command to set up your configuration including your Cyrating token which is provided in your user interface:

```sh
echo -e "[cyrating]\ntoken: cyratingtoken" > cyrating.ini
```


## Usage example

```python
>>> import cyrating
>>> cr = cyrating.init()
```

The init method takes into account 2 optional parameters:

- token: the Cyrating token
- proxies: the list of proxies to use when making a request. See [requests docs](https://requests.readthedocs.io/en/master/user/advanced/#proxies) for more information

Additional methods listed below are available

Method  | Description
------------- | -------------
get_main_company | returns main company
get_entities  | returns list of entities
get_suppliers | returns list of suppliers
domains | return list of domains for a company
set_tags | set tags to a specified domain (require admin privileges)
get_assets | get assets for a company
get_facts | get results of best practices controls
get_events | get list of active reputation events
get_certificate | returns certificate of a specific company
get_members | returns list of members, including child subscriptions' ones (require admin privileges)

# Examples

**Returns main company**
```python
>>> cr.main_company()
[...]
```

**Returns list of entities**
```python
>>> cr.entities()
[...]
```

**Returns list of suppliers**
```python
>>> cr.suppliers()
[...]
```

**Returns domains of a company**
```python
>>> cr.domains(main_company)
[...]
```

**Tag a domain**
```python
>>> cr.set_tags('example.com', ['tag1', 'tag2'])
[...]
```

**Get assets**

The method get_assets returns a dictionary of assets with tags and type attributes. Each key of this dictionary represents an asset and is linked to the following attributes:

- type: type of the asset, may be 'domain', 'host' or 'ip'
- tags: list of tags linked with the asset
- domains: list of domains linked with the asset
- entities: list of entities linked with the asset. Entities are the ones included in the subscription.



```python
>>> cr.get_assets(cr.domains(main_company))
[...]
```


**Get results of best practices controls**

The method get_facts returns the results of best practices controls. _assets_
parameter is optional and is needed to provide tags association.

An best practice result includes the following attributes:

- domain: domain name linked with the asset
- category: name of the best practice's category
- entities: list of entities linked with the asset. Entities are the ones included in the subscription.
- tags: list of tags linked with the asset
- type: type of the asset, may be 'domain', 'host' or 'ip'
- name: name of the resource
- results: raw results of the control
- grade: unitary score of the control
- impact: for Unexpected Services controls only, impact on rating of the company. Please note that Cyrating algorithm streamlines this score by IP address and control

```python
>>> main_company = cr.main_company()
>>> cr.get_events(main_company, assets=cr.get_assets(main_company))
[...]
```


**Get the list of active reputation events**

The method get_events returns a list of active reputation events. _assets_
parameter is optional and is needed to provide tags association.

An active reputation event includes the following attributes:

- name: name of the asset concerned
- category: name of the reputation's category
- domains: list of domains linked with the asset
- entities: list of entities linked with the asset. Entities are the ones included in the subscription.
- tags: list of tags linked with the asset
- type: type of the asset, may be 'domain', 'host' or 'ip'
- source: a dictionary with the tag and the url of the reputation source
- occurrences: dates of occurrences of the event
- score: deprecated, replaced by impact
- impact: impact on rating of the company. Please note that Cyrating algorithm streamlines this score by resource and reputation's category

```python
>>> main_company = cr.main_company()
>>> cr.get_events(main_company, assets=cr.get_assets(main_company))
[...]
```

**Returns certificate of a specific company**
```python
>>> main_company = cr.get_main_company()
>>> cr.get_certificate(main_company)
```

**Save certificate of a specific company to a file**
```python
>>> main_company = cr.get_main_company()
>>> cr.get_certificate(main_company, filename='Cyrating - Certificate of {}.pdf'.format(main_company['name']))
```

**Get list of members**
```python
>>> cr.get_members()
[...]
```

## Meta

Cyrating – [@cyrating](https://twitter.com/cyrating) – hello@cyrating.com

Distributed under the ISCL licence. See ``LICENSE`` for more information.


## Contributing

1. Send issues to issues@cyrating.com


