ableton.jenkins-jcasc plugins
=============================

This directory contains a Gradle project, which is used to download dependencies for the
plugins required by this role. The plugins specified here **should be excluded** from your
`plugins.yaml` file, as they may conflict with the versions of the plugins specified here.

The Gradle project exists primarily so that this role can use [dependabot][dependabot] to
automatically update the plugins when new releases are published.


[dependabot]: https://dependabot.com
