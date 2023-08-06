# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kalyke']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.6.1,<2.7.0', 'hyper>=0.7.0,<0.8.0', 'pyjwt>=1.7.1,<1.8.0']

setup_kwargs = {
    'name': 'kalyke-apns',
    'version': '0.1.3',
    'description': 'A library for interacting with APNs and VoIP using HTTP/2.',
    'long_description': '# kalyke\n\n![Test](https://github.com/nnsnodnb/kalyke/workflows/Test/badge.svg)\n[![Maintainability](https://api.codeclimate.com/v1/badges/fb85bcf746e1f4025afa/maintainability)](https://codeclimate.com/github/nnsnodnb/kalyke/maintainability)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9551aa9ca66a47a787e0db53068382b0)](https://app.codacy.com/app/nnsnodnb/kalyke?utm_source=github.com&utm_medium=referral&utm_content=nnsnodnb/kalyke&utm_campaign=Badge_Grade_Dashboard)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![PyPI Package version](https://badge.fury.io/py/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![Python Supported versions](https://img.shields.io/pypi/pyversions/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![PyPI status](https://img.shields.io/pypi/status/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![wheel](https://img.shields.io/pypi/wheel/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![format](https://img.shields.io/pypi/format/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![implementation](https://img.shields.io/pypi/implementation/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n[![LICENSE](https://img.shields.io/pypi/l/kalyke-apns.svg)](https://pypi.org/project/kalyke-apns)\n\nA library for interacting with APNs and VoIP using HTTP/2.\n\n## Installation\n\nkalyke requires python 3.6 or later.\n\n```bash\n$ pip install kalyke-apns\n```\n\n## Usage\n\n### APNs\n\n```python\nfrom kalyke.client import APNsClient\nfrom kalyke.payload import PayloadAlert, Payload\n\n\npayload_alert = PayloadAlert(title="YOUR TITLE", body="YOUR BODY")\nalert = Payload(alert=payload_alert, badge=1, sound="default")\n\nclient = APNsClient(\n    team_id="YOUR_TEAM_ID", auth_key_id="AUTH_KEY_ID", auth_key_filepath="/path/to/AuthKey_AUTH_KEY_ID.p8",\n    bundle_id="com.example.App", use_sandbox=True, force_proto="h2"\n)\n# or background push\n"""\nclient = APNsClient(\n    team_id="YOUR_TEAM_ID", auth_key_id="AUTH_KEY_ID", auth_key_filepath="/path/to/AuthKey_AUTH_KEY_ID.p8",\n    bundle_id="com.example.App", use_sandbox=True, force_proto="h2", apns_push_type="background"\n)\n"""\n\n# Send single push notification\n\nregistration_id = "a8a799ba6c21e0795b07b577b562b8537418570c0fb8f7a64dca5a86a5a3b500"\n\nresult = client.send_message(registration_id, alert)\n\n# Send multiple push notifications\nregistration_ids = [\n    "87b0a5ab7b91dce26ea2c97466f7b3b82b5dda4441003a2d8782fffd76515b73",\n    "22a1b20cb67a43da4a8f006176788aa20271ac2e3ac0da0375ae3dc1db0de210"\n]\n\nresults = client.send_bulk_message(registration_ids, alert)\n```\n\n### VoIP\n\n```python\nfrom kalyke.client import VoIPClient\n\n\nclient = VoIPClient(\n    auth_key_filepath="/path/to/YOUR_VOIP_CERTIFICATE.pem",\n    bundle_id="com.example.App.voip", use_sandbox=True\n)\n\nalert = {\n    "key": "value"\n}\n\n# Send single VoIP notification\n\nregistration_id = "14924adeeabaacc8b38cfd766965abffd0ee572a5a89e7ee26e6009a3f1a8e8a"\n\nresult = client.send_message(registration_id, alert)\n\n# Send multiple VoIP notifications\n\nregistration_ids = [\n    "84b7120bf190d171ff904bc943455d6081274714b32c486fa28814be7ee921fb",\n    "afaa8dcedc99d420e35f7435edad4821dbad3c8c7d5071b2697da9bd7a5037ad"\n]\n\nresults = client.send_bulk_message(registration_ids, alert)\n```\n\n## Todo\n\n- [ ] Tests\n\n## License\n\nThis software is licensed under the MIT License (See [LICENSE](LICENSE)).\n',
    'author': 'Yuya Oka',
    'author_email': 'nnsnodnb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnsnodnb/kalyke',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
