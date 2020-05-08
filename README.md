Justice Augment Python SDK
==========================

Python SDK for Justice Augment Project.

## Development Setup
Set these local environment variables:

- `IAM_CLIENT_ID` - IAM client id
- `IAM_CLIENT_SECRET` - IAM client secret
- `ADMIN_USERNAME` - _(optional)_ user/admin username
- `ADMIN_PASSWORD` - _(optional)_ user/admin password

Then run:
``` shell
$ make build
```

It will create a docker image with env variables interpolated in `tox.ini` file for testing.

To test it, run this command:
```shell
$ make test
```

After that, you can cleanup the working directory with this command:
```shell
$ make clean
```


## How to use
To use this SDK you can install it from pip with this command:

```shell
$ pip install justice-augment-python-sdk
```

Alternatively, you can add `justice-augment-python-sdk` as dependency in `requirements.txt`.
Then you install it with this command:

```shell
$ pip install -r requirements.txt
```

After that you can import the package, and use it like this:

```python
import os
from justice import Justice


endpoint = "https://demo.accelbyte.io"
namespace = 'accelbyte'

core = Justice(namespace, endpoint)
wallet_id = 'some-wallet-string-id'
resp = core.wallet.get_wallet(wallet_id)
my_wallet = resp.json()
print("Wallet balance: {0} {1}".format(my_wallet['balance'], my_wallet['currencyCode']))
```

Do not forget to set `IAM_CLIENT_ID` and `IAM_CLIENT_SECRET` in your local environment variables if you want to try it in your local machine.


## Commit Message Guidelines
We use [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/) as a guidelines to write commit message. You use this format to write your commit message:

```
<type>(optional scope): <description>
<BLANK LINE>
<optional-body>
<BLANK LINE>
<optional-footer>
```

Any line of the commit message cannot be longer than 100 characters!

Samples:

```
docs(changelog): update changelog to beta.5
```
```
fix(login): add the missing username field

We made login system without username field in our Database!
```

### Type
Must be one of the following:

* **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
* **ci**: Changes to our CI configuration files and scripts (example scopes: Circle, BrowserStack, SauceLabs)
* **docs**: Documentation only changes
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **test**: Adding missing tests or correcting existing tests
* **chore**: Repository maintenance