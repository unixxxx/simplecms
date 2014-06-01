###Simple CMS written in python3 bottle framework

by default, project is configured to work on openshift cloud: https://openshift.redhat.com.
You only need to add mongodb cartridge and restart app.


If you want to deploy app on your own server, you have to configure ```DB_CREDENTIALS``` variable
in ```config/__init__.py```

```
DB_CREDENTIALS = {
    'creds': {
        'username': 'database username',
        'password': 'database password',
        'host': 'database host name',
        'port': database port #must be integer
    },
    'db': 'database name'
}
```

When application is deployed default user is created for admin interface.
```
username: admin
password: admin
```
**It is strongly recomended to change password after deployment.**


