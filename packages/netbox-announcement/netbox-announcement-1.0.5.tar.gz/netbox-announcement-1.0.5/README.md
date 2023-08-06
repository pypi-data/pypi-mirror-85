# Netbox Announcement Plugin

This the netbox announcement plugin.
You can use [netbox_announcement](https://github.com/vas-git/netbox-announcement) plugin in Github.com

## Installing Netbox Announcement Plugin
The instructions below detail the process for installing and enabling a Netbox announcement plugin.

### Install Package
Download and install the plugin package per its installation instructions. Plugins published via PyPI are typically installed using pip. Be sure to install the plugin within Netbox`s virtual environment.

please refer [how to use netbox plugins](https://netbox.readthedocs.io/en/stable/plugins/)


```
$ source /opt/netbox/venv/bin/activate

(venv)$ pip install netbox_announcement==[latest version]
```

### Enable the Plugin

In `configuration.py`, add the plugin's name to the `PLUGIINS` list:

```
PLUGINS = [
    'netbox_announcement',
]
```

### Configure Plugin
Open `configuration.py` with your preferred editor to begin configuring of Netbox announcement plugin. The following configuration are required only when you migrate the model of the netbox announcement plugin to the Netbox database.

```
DEVELOPER=True 
```

### Run Database Migrations

The Netbox announcement plugin has 3 models related with Virtual Machine / Device announcement, and Site announcement.
To introduce these new db models, run the provided schema migrations.
Next, we can apply the migration of the Netbox_announcement model to the database with the `migrate` command

```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py makemigrations netbox_announcement
(venv) $ python3 manage.py migrate netbox_announcement
```

### Restart service

Then, restart the `netbox` and `netbox-rq` services to enable them

```
# systemctl restart netbox netbox-rq
# systemctl restart nginx
```

## Reference

Please refer [Netbox plugin development document](https://netbox.readthedocs.io/en/stable/plugins/development/)