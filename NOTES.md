# Notes

# Using ansible
Ansible is used here to set up quickly the server dependencies, the deployment tools
and the repository updates in a more automated form.

All following commands must be run inside the `deploy_tools/ansible` directory.

The `-v, -vv, -vvv` flags allows more or less verbose output in the playbook execution. 

In order to provision the server for the first time, run:
```shell
$ ansible-playbook dependencies.yaml -u <root user> [-v, -vv, -vvv]
```
Once this playbook is run, there will be a new user, `django`, which will be the one
to use to accomplish the deployment process.

The next commands can be run using the `django` user, which was created in the first step.

Set up the deployment tools (nginx and gunicorn)
```shell
$ ansible-playbook deployment.yaml -u django [-v, -vv, -vvv]
```

Set up the repository
```shell
ansible-playbook repository.yaml -u django [-v, -vv, -vvv]
```
