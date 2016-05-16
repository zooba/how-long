from azure.mgmt.web import WebSiteManagementClient, WebSiteManagementClientConfiguration

from importlib.util import find_spec
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, splitpasswd, splituser, urljoin

import requests
import subprocess
import sys

def get_package(name):
    n = Path(name)
    for root in find_spec(name).submodule_search_locations:
        r = Path(root)
        yield from ((f, str(n / f.relative_to(r))) for f in r.rglob('**/*'))

def get_requirements(requirements, target):
    requirements = Path(requirements)
    target = Path(target)

    subprocess.check_output([
        sys.executable, '-m', 'pip', 'install',
        '-r', str(requirements), '--target', str(target)
    ])
    return ((f, str(f.relative_to(target))) for f in target.rglob('**/*'))

def print_operation_results(resources_client, resource_group, deployment):
    pass


# HACK: Patch User model so we get scm_uri back
from azure.mgmt.web.models import User
User._attribute_map['scm_uri'] = {'key': 'properties.scmUri', 'type': 'str'}
_User_init = User.__init__
def User_init(s, *a, **kw):
    s.scm_uri = kw.pop('scm_uri', '')
    _User_init(s, *a, **kw)
User.__init__ = User_init
# End of hack

class Site:
    def __init__(self, credentials, subscription_id, resource_group, website):
        self._wsc = WebSiteManagementClient(WebSiteManagementClientConfiguration(
            credentials, subscription_id
        ))
        self._resource_group = resource_group
        self._website = website
        self._api_url = None
        self._api_auth = None

    def _ensure_api(self):
        if self._api_url:
            return
        scm_uri = self._wsc.sites.list_site_publishing_credentials(
            self._resource_group, self._website
        ).result().scm_uri

        scheme, netloc, path, query, fragment = urlsplit(scm_uri)
        userpass, netloc = splituser(netloc)
        self._api_auth = splitpasswd(userpass)
        self._api_url = urlunsplit((scheme, netloc, path, query, fragment))

    def mkdir(self, target):
        self._ensure_api()
        path = urljoin(self._api_url, '/api/vfs/' + target)
        if not path.endswith('/'):
            path += '/'
        requests.put(path, auth=self._api_auth).raise_for_status()

    def upload_python(self, version, target):
        self.mkdir(target)
        self.upload_zip(
            Path(__file__).absolute().parent / 'python-{}-embed-amd64.zip'.format(version),
            target
        )

    def upload_zip(self, zip_or_path, target):
        self._ensure_api()
        path = urljoin(self._api_url, '/api/zip/' + target)
        if isinstance(zip_or_path, (str, Path)):
            with open(str(zip_or_path), 'rb') as f:
                zip_data = f.read()
        else:
            zip_data = zip_or_path
        requests.put(path, data=zip_data, auth=self._api_auth).raise_for_status()

    def exec(self, cmd, dir):
        self._ensure_api()
        path = urljoin(self._api_url, '/api/command')
        resp = requests.post(path, json={
            'command': cmd,
            'dir': dir,
        }, auth=self._api_auth)
        resp.raise_for_status()
        output = resp.json()
        return output.get('output') or output.get('error')

    @property
    def host_names(self):
        conf = self._wsc.sites.get_site(self._resource_group, self._website)
        return conf.host_names
