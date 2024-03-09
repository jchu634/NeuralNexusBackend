
### Setting up Backend
1. Install the required packages using the following command:
    ```bash
    pip install -r requirements.txt
    ```
2. Set up the environment variables in the `.env` file.
    The following variables are required:
    - `ENV_TYPE` (The environment, either `development` or `production`)
    - `AUTH_SECRET_KEY` (A signing key for JWT tokens)
        - Generate a random 32-byte hex string using the following command:
            ```bash
            openssl rand -hex 32
            ```
    Optional `.env` variables:
    - `ALLOWED_IMAGE_EXTENSIONS` (A Python list of allowed image extensions)
        - Default: ['PNG', 'JPG', 'JPEG', 'GIF', 'WEBP']
    - `CACHE_TIMEOUT_PERIOD` (The timeout period for the cache in seconds)
        - Default: 900 (15 Minutes)
    - `ACCESS_TOKEN_EXPIRE_MINUTES` (The expiry time for the JWT access tokens in minutes)
        - Default: 30
    - `IMAGE_DEFAULT_EXPIRY_PERIOD` (The default expiry period for images in seconds)
        - Default: 2592000 (30 Days)

### Planned Features
- 3rd Party OAuth (Google, Facebook, Github etc.)
- User interface for admin tasks
- User throttling
- User rate limiting
- CMDLINE arguments for environment variables
- More test coverage