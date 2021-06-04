library 'ableton-utils@0.21'
library 'groovylint@0.9'
library 'python-utils@0.10'


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
  cleanup: { data -> data.venv?.cleanup() },
)
