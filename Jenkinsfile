library(identifier: 'ableton-utils@0.21', changelog: false)
library(identifier: 'groovylint@0.12', changelog: false)
library(identifier: 'python-utils@0.11', changelog: false)


devToolsProject.run(
  setup: { data ->
    Object venv = virtualenv.create('python3.8')
    venv.run('pip install -r requirements-dev.txt')
    data['venv'] = venv
  },
  test: { data ->
    parallel(failFast: false,
      'ansible-lint': { data.venv.run('ansible-lint -c .ansible-lint.yml') },
      groovylint: { groovylint.check('./Jenkinsfile') },
      molecule: { data.venv.run('molecule --debug test') },
    )
  },
  deployWhen: { runTheBuilds.isPushTo(['main']) && env.PRODUCTION == 'true' },
  deploy: { data ->
    String versionNumber = readFile('VERSION').trim()
    version.tag(versionNumber)
  },
)
