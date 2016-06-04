import uuid
from urlparse import urljoin
from urlparse import urlparse
import os

def get_url(url,value):
	if value.startswith("http"):
		return value
	else:
		return urljoin(url,value)

def name_file(url,suffix='pdf'):
    '''
    input:
        url is a full url path, start with http
    '''
    tparser = urlparse(url)
    name = ''
    if tparser.path != '':
        tmp = os.path.split(tparser.path)[-1]
        if tmp != '':
            name = tmp
    if name == '':
        name = str(uuid.uuid4()) + '.' + suffix
    return name

def regulate_filename(name):
	name = name.replace('?','').replace(':','').replace(' ','').replace('*','')
	return name

if __name__ == "__main__":
    url = "http://www.baidu.com"
    print name_file(url)
