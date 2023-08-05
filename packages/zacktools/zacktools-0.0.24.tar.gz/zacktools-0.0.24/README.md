# zacktools

### Useful tools created by zackdai

# install
`pip install zacktools`

or from git

`pip3 install git+https://github.com/ZackAnalysis/zacktools.git`

## pageparser

A tool for parse address,phone, email, facebook, twitter, linkedin, contact link, about us link from a webpage

### usage

```
from zacktools import pageparser
import requests
res = requests.get('http://rel8ed.to')
result = pageparser.parse(res.content)
print(result)
```

Note: MainAddress is an Object, and can be further extacted like:

`print(result['Mainaddress'].city)`

If want to convert to json directly, add parameters tojson=True
```
import json

result2 = pageparser.parse(res.content, tojson=True)

print(json.dumps(result2, indent=2))

{
  "facebook": "https://www.facebook.com/rel8edto/",
  "twitter": "https://twitter.com/rel8edto",
  "instagram": "",
  "linkedin": "https://www.linkedin.com/company/rel8ed-to",
  "contactlink": "http://www.rel8ed.to/contact-us/",
  "aboutlink": "http://www.rel8ed.to/about-us/",
  "title": "Big Data Analysis Data Mining Predictive Analytics",
  "email": "info@rel8ed.to",
  "phone": "905.321.0466",
  "Mainaddress": "1 St. Paul St., Unit A303, St. Catharines, ON L2R 7L2",
  "addresses": [
    "1 St. Paul St., Unit A303, St. Catharines, ON L2R 7L2"
  ]
}
```
### Test it [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1aE8PeQhJym8G6I_yHVfqIuydod5tlQuQ?usp=sharing)
