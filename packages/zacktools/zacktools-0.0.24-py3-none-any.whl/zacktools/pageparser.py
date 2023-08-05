from bs4 import BeautifulSoup, Comment
from collections import Counter
import pyap, re, requests

def visiableText(page):
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in 
                        ['style', 'script','script','img', 'head', 'title', 
                        'meta','link','footer','base','applet','iframe','embed',
                        'nodembed','object','param','source','[document]']]
    visible =  '\n'.join([re.sub(r'[\t/]+',' ', t) for t in visable_tags])
    visible = re.sub(r' +\n','\n', visible)
    visible = re.sub(r'\n+','\n', visible)
    return re.sub(r' +', ' ', visible)

def toDomain(link):
    return (re.sub(r'^(https?://)?(www\d?\.)?','', link).split('/')+[''])[0].strip()

def parse(page,domain=''):
    result = {
              'title':'',
              'corpName':'',
              'contactLink':'', 
              'aboutLink':'', 
              'email':'',
              'phone':'',
              'mainAddress':'',
              'addresses':[],
              'facebook':'',
              'twitter':'',
              'instagram':'',
              'linkedin':'',
              'city':'',
              'region':'',
              'country':'',
              'postalCode':''
              }        
    soup = BeautifulSoup(page,'lxml')
    vis = visiableText(page)
    addresses = pyap.parse(vis, country='CA')
    addresses += pyap.parse(vis, country='US')
    addresses = [a for a in addresses if not re.findall(r'\band\b', str(a), re.I) and not re.findall(r'\bis\b', str(a), re.I)]
    addressesNoAnd = [a for a in addresses if not re.findall(r'\band\b', str(a), re.I)]
    if len(addressesNoAnd)>1:
      addresses = addressesNoAnd
    allLinks = [s.get('href') for s in soup.select('a[href]')]
    allLinks = [s for s in allLinks if 'javascript' not in s and 'void' not in s]
    if allLinks:
      for social in ['facebook', 'twitter', 'instagram','linkedin']:
        result[social] = ([l for l in allLinks if social in l]+[''])[0]
      if not domain:
        domain = Counter([toDomain(l) for l in allLinks]).most_common(1)[0][0]
      else:
        domain = toDomain(domain)

      innerLinks = [f'http://{domain}'+s if s.startswith('/') else s for s in allLinks if s.startswith('/') or domain in s]
      result['contactLink'] = ([l for l in innerLinks if 'contact' in l.lower() or 'location' in l.lower()] + [''])[0]
      result['aboutLink'] = ([l for l in innerLinks if 'about' in l.lower()] + [''])[0]

    result['title'] = soup.find('title').text.replace('\n','').strip() if soup.find('title') else ''
    namepattern = r'\W?'.join([l for l in domain.split('.')[0]])

    result['email'] = ';'.join(re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', vis))
    result['phone'] = ';'.join(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', vis))

    if not addresses and result['aboutLink']:
      try:
        res = requests.get(result['aboutLink'])
        resvis = visiableText(res.content)
        addresses = pyap.parse(resvis, country='CA')
        addresses += pyap.parse(resvis, country='US')
        addressesNoAnd = [a for a in addresses if not re.findall(r'\band\b', str(a), re.I)]
        if len(addressesNoAnd)>1:
          addresses = addressesNoAnd
      except Exception as e:
        pass
    names = []
    if result['title']:
      names = re.findall(namepattern, result['title'], re.I)
    elif result['aboutLink']:
      try:
        aboutres = requests.get(result['aboutLink'])
        aboutvis = visiableText(aboutres.content)
        names = re.findall(namepattern, aboutvis, re.I)
      except:
        pass
    if names:
      result['corpName'] = sorted(names, key=lambda x: len(x.split(' ')), reverse=True)[0]
    if addresses:
        result['mainAddress'] = re.split(r'\band\b(?i)',str(addresses[-1]))[-1]
        result['addresses'] = addresses
    if result['mainAddress']:
      result['city'] = addresses[-1].city
      result['region'] = addresses[-1].region1
      result['country'] = addresses[-1].country_id
      result['postalCode'] = addresses[-1].postal_code
      result['addressLine'] = addresses[-1].full_street
    result['addresses'] = [str(a) for a in result['addresses']]
    return result


if __name__ == '__main__':
  res = requests.get('https://mamayolandas.ca')
  result = parse(res.content)
  print(result)