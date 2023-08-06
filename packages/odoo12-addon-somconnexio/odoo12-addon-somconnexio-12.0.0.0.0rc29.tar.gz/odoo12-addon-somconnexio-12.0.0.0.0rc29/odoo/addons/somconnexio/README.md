
This project provides an ERP system for [Som Connexio](https://somosconexion.coop/) telecommunication users cooperative.

### DEVELOPMENT

#### Create development enviornment

Create the `devenv` container with the `somconnexio` module mounted and provision it. Follow the [instructions](https://gitlab.com/coopdevs/odoo-somconnexio-inventory#requirements) in [odoo-somconnexio-inventory](https://gitlab.com/coopdevs/odoo-somconnexio-inventory).

Once created, we can stop or start our `odoo-sc` lxc container as indicated here:
```
$ sudo systemctl start lxc@odoo-sc
$ sudo systemctl stop lxc@odoo-sc
```

To check our local lxc containers and their status, run:
```
$ sudo lxc-ls -f
```

#### Start the ODOO application

Enter to your local machine as the user `odoo`, activate the python enviornment first and run the odoo bin:
```
$ ssh odoo@odoo-sc.local
$ pyenv activate odoo
$ cd /opt/odoo
$ set -a && source /etc/default/odoo && set +a
$ ./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo
```

To use the local somconnexio module (development version) instead of the PyPI published one, you need to upgrade the [version in the manifest](https://gitlab.com/coopdevs/odoo-somconnexio/-/blob/master/somconnexio/__manifest__.py#L3) and then update the module with `-u` in the Odoo CLI.


#### Restart ODOO database from scratch

Enter to your local machine as the user `odoo`, activate the python enviornment first, drop the DB, and run the odoo bin to create it again:
```
$ ssh odoo@odoo-sc.local
$ pyenv activate odoo
$ dropdb odoo
$ cd /opt/odoo
$ ./odoo-bin -c /etc/odoo/odoo.conf -i somconnexio -d odoo --stop-after-init
```

#### Run tests

You can run the tests with this command:
```
$ ./odoo-bin -c /etc/odoo/odoo.conf -u somconnexio -d odoo --stop-after-init --test-enable
```

The company data is rewritten every module upgrade

Credits
=======

###### Authors

* Coopdevs Treball SCCL

###### Contributors

* Coopdevs Treball SCCL
