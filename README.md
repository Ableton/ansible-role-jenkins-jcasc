Ansible role ableton.jenkins_jcasc
==================================

This role provisions the [Jenkins CI Service][jenkins] on a Unix host. It uses [JCasC
(Jenkins Configuration as Code)][jcasc] to configure the instance, and the [Jenkins Plugin
Installation Manager Tool][pimt] to download Jenkins plugins and their respective
dependencies. Generally speaking, this is much faster and more reliable than using
Ansible's `jenkins_plugin` module or with API calls to a running instance of Jenkins.

Requirements
------------

Ansible >= 2.9, and a target host which meets the following requirements:

- Supports one of the following package managers:
  - apt
- Supports one of the following service managers:
  - systemd
  - sysvinit

Additionally, you'll need a `jenkins.yaml` file for the Jenkins system configuration and a
`plugins.yaml` file to specify the Jenkins plugins to install.

The `jenkins.yaml` configuration file can be generated from an existing Jenkins
installation by performing the following steps:

1. Install the JCasC plugin (and restart Jenkins)
2. Navigate to the "Manage Jenkins" page
3. Navigate to the"Configuration as Code" page under the "System Configuration" section
4. On this page, there is a button under the "Actions" section labeled "Download
   Configuration", which generate a YAML file that can be used with this role

Please see the [JCasC homepage][jcasc] for more details on this YAML file format.

As for the `plugins.yaml` file, please refer to the [tool's homepage][pimt] for
information on this file's format. **Important**: the `plugins.yaml` file must at least
contain the `configuration-as-code` (JCasC) plugin.

Both the `jenkins.yaml` and `plugins.yaml` files are treated as templates, so Jinja2
syntax can be used to customize them during provisioning.

Role Variables
--------------

See the [`defaults/main.yml`](defaults/main.yml) file for full documentation on required
and optional role variables.

Example Playbook
----------------

```yaml
---
- name: Provision Jenkins
  hosts: all
  vars:
    jenkins_java_args: "-server -Xmx2g -Xms512m"
    jenkins_jcasc_config_file: "jenkins.yaml.j2"
    jenkins_pimt_args: "--latest false"
    jenkins_plugins_file: "plugins.yaml"
    jenkins_jobs:
      - "example_job"
    jenkins_jobs_dir: "{{ playbook_dir }}/files/jenkins/jobs"

  roles:
    - ableton.jenkins_jcasc
```

HTTPS
-----

This role **does not** support HTTPS, due to the complexity of configuration. If HTTPS
support is needed, the easiest way to add this is using an `nginx` proxy.

However, HTTP must be enabled to provision Jenkins with this role. In other words, you may
not define `jenkins_port` to `-1` to disable HTTP altogether. To provide a secure-only
Jenkins service, you should instead use a proxy service for HTTPS (with nginx, for
example), and firewall off HTTP traffic.

License
-------

MIT

Maintainers
-----------

This project is maintained by the following GitHub users:

- [@ala-ableton](https://github.com/ala-ableton)
- [@nre-ableton](https://github.com/nre-ableton)


[jcasc]: https://github.com/jenkinsci/configuration-as-code-plugin
[jenkins]: https://jenkins.io
[maven]: https://maven.apache.org
[pimt]: https://github.com/jenkinsci/plugin-installation-manager-tool
