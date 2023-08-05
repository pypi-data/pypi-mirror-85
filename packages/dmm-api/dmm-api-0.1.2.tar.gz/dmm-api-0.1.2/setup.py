# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dmm_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'dmm-api',
    'version': '0.1.2',
    'description': 'DMM API Client for Python',
    'long_description': "# DMM Affiliate API Client for Python\n\n* **This SDK is unofficial**\n* API Guide is [here](https://affiliate.dmm.com/api/guide/).\n\n## Install\n\n```sh\npip install dmm-api\n```\n\n## Usage\n\n* [Examples](https://github.com/takelushi/dmm-api-py/tree/master/examples))\n\n```py\nimport os\n\nfrom dmm_api import DMMApiClient\n\nAPI_ID = os.environ.get('DMM_API_ID', '')\nAFFILIATE_ID = os.environ.get('DMM_AFFILIATE_ID', '')\n\nclient = DMMApiClient(API_ID, AFFILIATE_ID)\nres = client.get_floor()\nprint(res.json())\n```\n\n## Supported API list\n\n### v3\n\n* 商品情報 API (ItemList)\n* フロア API (FloorList)\n* 女優検索 API (ActressSearch)\n* ジャンル検索 API (GenreSearch)\n* メーカー検索 API (MakerSearch)\n* シリーズ検索 API (SeriesSearch)\n* 作者検索 API (AuthorSearch)\n\n## For developers\n\n* Setup\n\n   **Require: poetry**\n\n   ```she\n   git clone git@github.com:takelushi/dmm-api-py.git\n   cd dmm-api-py\n   poetry install\n   ```\n\n* Build\n\n   ```sh\n   poetry build\n   ```\n\n* Register PyPI and install.\n\n   ```sh\n   poetry publish\n   pip --no-cache-dir install --upgrade dmm-api\n   ```\n",
    'author': 'Takeru Saito',
    'author_email': 'takelushi@gmail.com',
    'maintainer': 'Takeru Saito',
    'maintainer_email': 'takelushi@gmail.com',
    'url': 'https://github.com/takelushi/dmm-api-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
