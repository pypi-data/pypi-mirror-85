# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
import configparser
import jwt
import arrow
import json

PATH_MASTER_TOKEN = "./cyrating.ini"
APP_URL = "https://api.cyrating.com"
COMPANY_ENDPOINT = '/company'
CLIENT_ENDPOINT = '/client'
CERTIFICATE_ENDPOINT = '/manage_report'
ASSETS_ENDPOINT = '/assets'
TAGS_ENDPOINT = '/tags'
EVENTS_ENDPOINT = '/events'
FACTS_ENDPOINT = '/facts'

event_categories = dict(SP='Spam propagation', IC='Involvement in cyberattacks', BR='Bad reputation', HM='Hosting malicious services')


def jsonFilter(dic):
  if isinstance(dic, list):
    return dic
  res = {}
  for key in dic.keys():
    if not key.startswith('_'):
      res[key] = dic[key]
  return res


class Cyrating(object):
  def __init__(self, **kwargs):
    """ Init a Cyrating context """

    self.__access_token__ = kwargs.get('token') if 'token' in kwargs else self.get_personal_token()
    self.__proxies__ = kwargs.get('proxies', None)
    decoded_atoken = jwt.decode(self.__access_token__, verify=False)
    self._requests = requests.Session()
    self._requests.mount('', HTTPAdapter(max_retries=5))
    self.__app_url__ = 'http://127.0.0.1:5000' if kwargs.get('debug') else APP_URL
    self.__headers__ = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + self.__access_token__}
    self.__current_user_id__ = decoded_atoken['sub']

    (tmp, self.__current_client_id__, self.__current_role) = decoded_atoken['ccs'].split(':')
    self.client(self.__current_client_id__)
    print("# Access Token for ", self.__app_url__, self.__current_client_id__, "expires at",
          arrow.get(decoded_atoken['exp']))
    if self.__proxies__ is not None:
      self._requests.proxies = self.__proxies__

  def get_personal_token(self):
    """ Read personal token from configuration file """

    config = configparser.ConfigParser()
    config.read(PATH_MASTER_TOKEN)
    return config['cyrating']['token']

  def get(self, endpoint, id, extraHttpRequestParams=None):
    url = self.__app_url__ + endpoint + '/' + id
    res = self._requests.get(url,
                             params=extraHttpRequestParams,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      return jData

    if res.status_code == 401:
      raise(Exception('Invalid token'))

    return None

  def post(self, endpoint, obj, extraHttpRequestParams=None):
    res = self._requests.post(self.__app_url__ + endpoint,
                              json.dumps(obj),
                              params=extraHttpRequestParams,
                              headers=self.__headers__)

    if res.ok:
      jData = json.loads(res.content)
      return jData

  def patch(self, obj, extraHttpRequestParams=None):
    headers = self.__headers__.copy()
    headers.update({"If-Match": obj['_etag']})

    res = self._requests.patch(self.__app_url__ + '/' + obj['_links']['self']['href'],
                               json.dumps(jsonFilter(obj)),
                               headers=headers,
                               params=extraHttpRequestParams,
                               stream=False)

    if res.ok:
      jData = json.loads(res.content)
      return jData

    if res.status_code == 403:
      raise(Exception('You need admin role to carry out this operation.'))

    if res.status_code == 422:
      jData = json.loads(res.content)
      print(jData)
      raise(Exception('Unprocessable Entity: {}'.format(jData['_issues'])))

    if res.status_code == 401:
      raise(Exception('Invalid token'))

    return None

  def find_one(self, endpoint, extraHttpRequestParams=None):
    queryParameters = {'page': 1, 'max_results': 100}

    if extraHttpRequestParams:
      queryParameters.update(extraHttpRequestParams)

    res = self._requests.get(self.__app_url__ + endpoint,
                             params=queryParameters,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      assert len(jData['_items']) >= 0, 'Error multiple instance of {} in {}'.format(extraHttpRequestParams, endpoint)
      if len(jData['_items']) == 0:
        return None
      return jData['_items'][0]

    if res.status_code == 401:
      raise(Exception('Invalid token'))

    return None

  def findall(self, endpoint, page=1, extraHttpRequestParams=None):
    queryParameters = {'page': page, 'max_results': 100}

    if extraHttpRequestParams:
      queryParameters.update(extraHttpRequestParams)

    res = self._requests.get(self.__app_url__ + endpoint,
                             params=queryParameters,
                             headers=self.__headers__)
    if res.ok:
      jData = json.loads(res.content)
      if len(jData['_items']) != 0:
        to_append = self.findall(endpoint, page + 1, extraHttpRequestParams)
        jData['_items'].extend(to_append)

      return jData['_items']

    if res.status_code == 401:
      raise(Exception('Invalid token'))

    return None

  def client(self, clientid):
    """ Retrieve client obj from API """

    answer = self.get(CLIENT_ENDPOINT, clientid)
    if not answer:
      self.__current_client__ = None
      return
    self.__current_client__ = dict(
        _id=answer['_id'] if '_id' in answer else None,
        name=answer['name'] if 'name' in answer else None,
        user=answer['user'] if 'user' in answer else None,
        company_id=answer['companyID'] if 'companyID' in answer else None,
        entities_id=answer['entitiesID'] if 'entitiesID' in answer else None,
        suppliers_id=answer['suppliersID'] if 'suppliersID' in answer else None,
    )

  def get_company(self, id):
    """ Retrieve company obj from API """

    return self.get(COMPANY_ENDPOINT, id)

  def get_certificate(self, company, filename=None):
    """ Get certificate of a company """

    httpParams = dict(
        client=self.__current_client_id__,
        organization=company['_id'],
        certificate='true'
    )
    answer = self._requests.get(self.__app_url__ + CERTIFICATE_ENDPOINT,
                                params=httpParams,
                                headers=self.__headers__)

    if not answer.ok:
      raise Exception('Failed to retreive certificate for {}'.format(company['name']))

    if filename:
      try:
        with open(filename, 'wb') as f:
          f.write(answer.content)
      except Exception as e:
        raise Exception('Failed to save {}: {}'.format(filename, e))
    else:
      return answer.content

  def main_company(self):
    """ Get main company """

    return self.get_company(self.__current_client__['company_id'])

  def entities(self):
    """ Get list of entities """

    return [self.get_company(companyid) for companyid in self.__current_client__['entities_id']]

  def suppliers(self):
    """ Get list of suppliers """

    return [self.get_company(companyid) for companyid in self.__current_client__['suppliers_id']]

  def assets(self, company):
    """ Get list of assets of a company """

    filter = {'where': json.dumps({'company': company['_id']})}
    return self.find_one(ASSETS_ENDPOINT, filter)

  def domains(self, company):
    """ Get list of domains associated to a company """

    assets = self.assets(company)
    if assets is not None:
      return [item['label'] for item in assets['nodes'] if item['type'] == 'domain']
    return None

  def set_tags(self, domainname, tags):
    if domainname is None:
      print('* Domain name is None')
      return
    if not isinstance(tags, list):
      print('* Tags is not an array')
      return
    tags_obj = self.get(TAGS_ENDPOINT, domainname)

    if not tags_obj:
      raise(Exception('{} does not exist.'.format(domainname)))
    tags_obj.update({'tags': tags})
    self.patch(tags_obj)

  def get_assets(self, company):
    filter = {'where': json.dumps({'company': company['_id']})}
    company_tags = self.findall(TAGS_ENDPOINT, 1, filter)
    tags = dict()
    domains_map = dict()

    enable_entities = False
    entities_map = dict()
    if company['_id'] == self.__current_client__['company_id']:
      enable_entities = True
      companies_id = self.__current_client__['entities_id'] or []
      filter = {'where': json.dumps({'_id': {'$in': companies_id}})}
      entities = self.findall(COMPANY_ENDPOINT, 1, filter)
      filter = {'where': json.dumps({'company': {'$in': companies_id}})}
      entities_assets = self.findall(ASSETS_ENDPOINT, 1, filter)

      for entity in entities:
        assets = next(assets for assets in entities_assets if assets['company'] == entity['_id'])
        domains = [node['label'] for node in assets['nodes'] if node['type'] == 'domain']
        for domainname in domains:
          if domainname not in entities_map:
            entities_map[domainname] = []
          entities_map[domainname].append(entity['name'])

    if company_tags:
      for item in company_tags:
        tags[item['domainname']] = item['tags'] if 'tags' in item else []
        domains_map[item['domainname']] = item['domainname']
    assets = self.assets(company)

    domains = [node['label'] for node in assets['nodes'] if node['type'] == 'domain']

    res = dict()
    for node in assets['nodes']:
      if node['label'] in res and node['type'] != 'domain':
        continue
      res[node['label']] = {'type': node['type'], 'tags': [], 'domains': [], 'entities': [], '_updated': False}
      if node['type'] == 'domain':
        res[node['label']]['tags'] = list(set(tags[node['label']] if node['label'] in tags else []))
        res[node['label']]['domains'] = [domains_map[node['label']]]
        res[node['label']]['entities'] = entities_map[node['label']] if enable_entities and node['label'] in entities_map else []
        res[node['label']]['_updated'] = True

    for link in assets['links']:
      if link['source'] in domains:
        res[link['target']]['tags'] = list(set(res[link['source']]['tags'] + res[link['target']]['tags']))
        res[link['target']]['domains'] = list(set(res[link['source']]['domains'] + res[link['target']]['domains']))
        res[link['target']]['entities'] = list(set(res[link['source']]['entities'] + res[link['target']]['entities']))
        res[link['target']]['_updated'] = True

    for link in assets['links']:
      if res[link['target']]['_updated'] is False:
        res[link['target']]['tags'] = list(set(res[link['source']]['tags'] + res[link['target']]['tags']))
        res[link['target']]['domains'] = list(set(res[link['source']]['domains'] + res[link['target']]['domains']))
        res[link['target']]['entities'] = list(set(res[link['source']]['entities'] + res[link['target']]['entities']))
        res[link['target']]['_updated'] = True

    return res

  def get_events(self, company, assets=None):
    filter = {'where': json.dumps({'company': company['_id']})}
    events = self.find_one(EVENTS_ENDPOINT, filter)

    res = []
    for key in events['assessment'].keys():
      for event in events['assessment'][key]:
        for source in event['sources']:
          item = {
              'name': event['name'],
              'type': event['type'],
              'occurrences': source['occurences'],
              'category': event_categories[key],
              'source': {
                  'tag': source['name'],
                  'url': source['url'] if 'url' in source else None
              },
              'score': -event['score'] / 2,
              'tags': assets[event['name']]['tags'] if assets else None,
              'domains': assets[event['name']]['domains'] if assets else None,
              'entities': assets[event['name']]['entities'] if assets and 'entities' in assets[event['name']] else None,
          }
          res.append(item)

    return res

  def format_result(self, results):
    res = ''
    for result in results:
      if 'label' in result:
        res += '{}: '.format(result['label'])
      if 'value' in result:
        res += '{}'.format(result['value'])
      res += '\r\n'
    return res

  def get_facts(self, company, assets=None):
    filter = {'where': json.dumps({'companies': company['_id']})}
    facts = self.findall(FACTS_ENDPOINT, 1, filter)

    res = []
    for fact in facts:
      tags = assets[fact['domainname']]['tags'] if assets else None
      entities = assets[fact['domainname']]['entities'] if assets and ('entities' in assets[fact['domainname']]) else None
      for category in fact['assessment'].keys():
        for control in fact['assessment'][category].keys():
          if control.startswith('HTTP') or control.startswith('SSL') or control.startswith('Web'):
            for result in fact['assessment'][category][control]['result']:
              try:
                grade = result['subscore'] / result['subbaseline']
              except Exception:
                grade = 'N/A'
              item = {
                  'domain': fact['domainname'],
                  'tags': tags,
                  'entities': entities,
                  'control': control,
                  'category': category,
                  'name': result['host'],
                  'type': 'host',
                  'grade': grade,
                  'results': '{}: {}'.format(result['label'], result['value'])
              }
              res.append(item)
          else:
            try:
              grade = fact['assessment'][category][control]['score'] / fact['assessment'][category][control]['baseline']
            except Exception:
              grade = 'N/A'
            # print(fact['domainname'], category, control)
            item = {
                'domain': fact['domainname'],
                'tags': tags,
                'entities': entities,
                'category': category,
                'control': control,
                'name': fact['domainname'],
                'type': 'domain',
                'grade': grade,
                'results': self.format_result(fact['assessment'][category][control]['result'])
            }
            res.append(item)
    return res

  def get_members(self):
    users = []
    for user in self.__current_client__['user']:
      user['client'] = self.__current_client__['name']
      user.pop('user')
      users.append(user)

    filter = {'where': json.dumps({'parent': self.__current_client__['_id']})}
    childs = self.findall(CLIENT_ENDPOINT, 1, filter)
    for child in childs:
      for user in child['user']:
        user['client'] = child['name']
        user.pop('user')
        users.append(user)
    return users
