# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atlantisbot_api',
 'atlantisbot_api.api',
 'atlantisbot_api.management.commands',
 'atlantisbot_api.migrations',
 'atlantisbot_api.tests']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<3.0',
 'djangorestframework>=3.10.3,<4.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests[security]>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'atlantisbot-api',
    'version': '1.0.7',
    'description': 'Django App to interface with the AtlantisBot API',
    'long_description': '## AtlantisBot API (Django App)\n\nThis is a Django App made to create an API that interfaces with [AtlantisBot](https://github.com/johnvictorfs)\'s Database.\n\n---\n\n### Setup\n\n- Install the app\n    ```python\n    # Or \'pip install atlantisbot-api\'\n    poetry add atlantisbot-api\n    ```\n\n- Add `"atlantisbot_api"` to your `INSTALLED_APPS` (in `settings.py`):\n    ```python\n    INSTALLED_APPS = [\n        ...\n        \'atlantisbot_api\'\n    ]\n    ```\n\n- (Optional, Discord Oauth) Setup Discord Oauth settings and API keys in your `settings.py` (sensitive configuration)\n    ```python\n    DISCORD_OAUTH2_CLIENT_ID = \'CLIENT_ID\'\n    DISCORD_OAUTH2_CLIENT_SECRET = \'CLIENT_SECRET\'\n    DISCORD_OAUTH2_REDIRECT_URI = \'https://your-website-callback-url.com\'\n\n    DISCORD_API_BASE_URL = \'https://discord.com/api/v6\'\n    DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + \'/oauth2/authorize\'\n    DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + \'/oauth2/token\'\n    if \'http://\' in DISCORD_OAUTH2_REDIRECT_URI:\n        os.environ[\'OAUTHLIB_INSECURE_TRANSPORT\'] = \'true\'\n    ```\n\n- Include API paths in your project `urls.py`:\n    ```python\n    path(\'atlantisbot/\', include(\'atlantisbot_api.urls\'))\n    ```\n\n- Run `python manage.py migrate` to create the `atlantisbot` models.\n\n- Your API paths should now be running at the following routes:\n    ```bash\n    # Database API Routes\n    /atlantisbot/api/\n\n    # Discord API Oauth routes\n    /atlantisbot/api/oauth/user/\n    /atlantisbot/api/oauth/authorize/\n    ```\n\n---\n\n## Docs\n\n### Management Commands\n\n- `python manage.py clear_secretsanta`\n    - Clears receiving and giving_to fields on every Secret Santa entry\n\n- `python manage.py roll_secretsanta`\n    - Make pairs for Secret Santa\n',
    'author': 'John Victor',
    'author_email': 'johnvfs@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johnvictorfs/atlantisbot-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
