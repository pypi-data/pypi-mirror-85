## AtlantisBot API (Django App)

This is a Django App made to create an API that interfaces with [AtlantisBot](https://github.com/johnvictorfs)'s Database.

---

### Setup

- Install the app
    ```python
    # Or 'pip install atlantisbot-api'
    poetry add atlantisbot-api
    ```

- Add `"atlantisbot_api"` to your `INSTALLED_APPS` (in `settings.py`):
    ```python
    INSTALLED_APPS = [
        ...
        'atlantisbot_api'
    ]
    ```

- (Optional, Discord Oauth) Setup Discord Oauth settings and API keys in your `settings.py` (sensitive configuration)
    ```python
    DISCORD_OAUTH2_CLIENT_ID = 'CLIENT_ID'
    DISCORD_OAUTH2_CLIENT_SECRET = 'CLIENT_SECRET'
    DISCORD_OAUTH2_REDIRECT_URI = 'https://your-website-callback-url.com'

    DISCORD_API_BASE_URL = 'https://discord.com/api/v6'
    DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + '/oauth2/authorize'
    DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + '/oauth2/token'
    if 'http://' in DISCORD_OAUTH2_REDIRECT_URI:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    ```

- Include API paths in your project `urls.py`:
    ```python
    path('atlantisbot/', include('atlantisbot_api.urls'))
    ```

- Run `python manage.py migrate` to create the `atlantisbot` models.

- Your API paths should now be running at the following routes:
    ```bash
    # Database API Routes
    /atlantisbot/api/

    # Discord API Oauth routes
    /atlantisbot/api/oauth/user/
    /atlantisbot/api/oauth/authorize/
    ```

---

## Docs

### Management Commands

- `python manage.py clear_secretsanta`
    - Clears receiving and giving_to fields on every Secret Santa entry

- `python manage.py roll_secretsanta`
    - Make pairs for Secret Santa
