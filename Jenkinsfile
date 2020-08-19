library 'ableton-utils@0.18'
library 'groovylint@0.8'
library 'python-utils@0.10'


devToolsProject.run(
  setup: { data ->
    Object venv = virtualenv.create('python3.8')
    venv.run('pip install -r requirements-dev.txt')
    data['venv'] = venv
  },
  test: { data ->
    parallel(failFast: false,
      groovylint: { groovylint.check('./Jenkinsfile') },
      molecule: { data.venv.run('molecule --debug test') },
    )
  },
  deployWhen: { runTheBuilds.isPushTo(['develop']) && env.PRODUCTION == 'true' },
  deploy: { data ->
    String versionNumber = readFile('VERSION').trim()
    version.tag(versionNumber)
  },
  cleanup: { data -> data.venv?.cleanup() },
)
