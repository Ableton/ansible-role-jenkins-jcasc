"""Molecule tests for the default scenario."""

import os

import testinfra.utils.ansible_runner

from jenkins import Jenkins


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_jenkins_user(host):
    """Test that the Jenkins user was created."""
    assert host.user("juser").group == "jgroup"
    assert host.user("juser").home == "/jenkins"


def test_jenkins_dir(host):
    """Test that the Jenkins directory was created."""
    assert host.file("/jenkins").is_directory
    assert host.file("/jenkins").mode == 0o0755
    assert host.file("/jenkins").user == "juser"
    assert host.file("/jenkins").group == "jgroup"


def test_jenkins_job_files(host):
    """Test that Jenkins job files were copied."""
    test_job_dir = host.file("/jenkins/home/jobs/test_job")
    test_job_config_file = host.file("/jenkins/home/jobs/test_job/config.xml")
    test_jobs_dir = host.file("/jenkins/home/jobs")

    assert test_jobs_dir.is_directory
    assert test_jobs_dir.user == "juser"
    assert test_jobs_dir.group == "jgroup"
    assert test_job_dir.is_directory
    assert test_job_dir.user == "juser"
    assert test_job_dir.group == "jgroup"
    assert test_job_config_file.is_file
    assert test_job_config_file.user == "juser"
    assert test_job_config_file.group == "jgroup"


def test_jenkins_custom_files(host):
    """Test that static web content files were copied."""
    jenkins_icon_file = host.file("/jenkins/home/userContent/jenkins.png")
    sidebar_link_config_file = host.file("/jenkins/home/sidebar-link.xml")
    user_content_dir = host.file("/jenkins/home/userContent")

    assert sidebar_link_config_file.is_file
    assert sidebar_link_config_file.user == "juser"
    assert sidebar_link_config_file.group == "jgroup"
    assert user_content_dir.is_directory
    assert user_content_dir.user == "juser"
    assert user_content_dir.group == "jgroup"
    assert jenkins_icon_file.is_file
    assert jenkins_icon_file.user == "juser"
    assert jenkins_icon_file.group == "jgroup"


def test_jenkins_java_process(host):
    """Test that the Jenkins service is running."""
    process = host.process.get(comm="java")

    assert process.args == " ".join(
        [
            "/usr/bin/java",
            "-server",
            "-Djenkins.install.runSetupWizard=false",
            "-jar",
            "/jenkins/lib/jenkins-2.277.2.war",
            "--webroot=/jenkins/caches/war",
            "--httpPort=8100",
            "--sessionTimeout=1",
        ]
    )


def test_jenkins_version():
    """Test that the correct version of Jenkins was installed."""
    controller = Jenkins("http://localhost:8100")
    version = controller.get_version()

    assert version == "2.277.2"


def test_jenkins_plugins():
    """Test that Jenkins plugins were installed."""
    controller = Jenkins("http://localhost:8100")
    plugins = controller.get_plugins()

    assert plugins["sidebar-link"]["active"]
    assert plugins["sidebar-link"]["enabled"]
    # The sidebar-link plugin has an implied dependency on structs, which is not specified
    # in the plugins.yaml file. Jenkins should automatically install this plugin when it
    # starts up.
    assert plugins["structs"]["active"]
    assert plugins["structs"]["enabled"]


def test_jenkins_jobs():
    """Test that Jenkins jobs are present."""
    controller = Jenkins("http://localhost:8100")
    test_job = controller.get_job_info("test_job")

    assert test_job["name"] == "test_job"
    assert test_job["buildable"]


def test_jenkins_users(host):
    """Test that Jenkins service users were created."""
    expected_users = {
        "alice": {"api_token": False, "found": False},
        "bob": {"api_token": True, "found": False},
        "carol": {"api_token": True, "found": False},
    }
    users_dir = "/jenkins/home/users"
    test_users_dir = host.file(users_dir)
    token_attribute = "jenkins.security.apitoken.ApiTokenStore_-HashedToken"

    assert test_users_dir.is_directory
    for dir_item in test_users_dir.listdir():
        test_dir_item = host.file(os.path.join(users_dir, dir_item))
        if test_dir_item.is_directory:
            user_config_file = host.file(
                os.path.join(users_dir, dir_item, "config.xml")
            )

            assert user_config_file.is_file
            for user in expected_users:
                if dir_item.startswith(user):
                    expected_users[user]["found"] = True
                    assert (
                        token_attribute in user_config_file.content_string
                    ) == expected_users[user]["api_token"]

    for user_state in expected_users.values():
        assert user_state["found"]


def test_secret_files(host):
    """Test that secret files were copied."""
    test_secrets_dir = host.file("/jenkins/secrets")
    test_secrets_file = host.file("/jenkins/secrets/secret.txt")

    assert test_secrets_dir.is_directory
    assert test_secrets_dir.user == "juser"
    assert test_secrets_dir.group == "jgroup"
    assert test_secrets_dir.mode == 0o0700
    assert test_secrets_file.is_file
    assert test_secrets_file.user == "juser"
    assert test_secrets_file.group == "jgroup"
    assert test_secrets_file.content_string == "super secret stuff"
