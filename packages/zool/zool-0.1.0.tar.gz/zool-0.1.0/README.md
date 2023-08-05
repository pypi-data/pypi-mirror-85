# zool

A cli for reviewing PRs and zuul's progress

`pip install .`

or

`python -m zool`


```
$ zool --help
usage: __main__.py [-h] -c COLLECTION [-o ORGANIZATION] [-u USERNAME] [-t TOKEN]
                   [-l {debug,info,warning,error,critical}] [-f LOGFILE] [-zh ZUUL_HOST] [-zt ZUUL_TENANT]
                   [-gh GH_HOST] [-gha GH_API_HOST] [-p PBAR_WIDTH]

optional arguments:
  -h, --help            show this help message and exit
  -c COLLECTION, --collection COLLECTION
                        The collection name, used as the githubh repo (ie ansible.netcommon) (default: None)
  -o ORGANIZATION, --organization ORGANIZATION
                        The Github organization (default: ansible-collections)
  -u USERNAME, --username USERNAME
                        The Github username for the token (default: cidrblock)
  -t TOKEN, --token TOKEN
                        Github personal access token (default: d951afcad44a787b981ea2c8bd3bbbf2c58276c5)
  -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                        Set the logging level (default: info)
  -f LOGFILE, --log-file LOGFILE
                        Log file location (default: /tmp/zool.log)
  -zh ZUUL_HOST, --zuul-host ZUUL_HOST
                        The zuul hostname (default: dashboard.zuul.ansible.com)
  -zt ZUUL_TENANT, --zuul-tenant ZUUL_TENANT
                        The zuul tenant (default: ansible)
  -gh GH_HOST, --github_host GH_HOST
                        The github host (browser) (default: github.com)
  -gha GH_API_HOST, --github_api_host GH_API_HOST
                        The github host (api) (default: api.github.com)
  -p PBAR_WIDTH, --pbar-width PBAR_WIDTH
                        The width of the progress bars (default: 10)
```