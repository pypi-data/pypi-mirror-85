from pathlib import Path

FMT= '%Y-%m-%dT%H:%M:%S'

RUN_SCRIPT_NAME = 'run'
RUNS_DIR = 'runs'
MSG_PATH = Path('_MSG')

DEFAULT_UPSTREAM_BRANCH = 'master'
RUNS_REMOTE = 'runs'
RUNS_BRANCH = 'runs'

CONFIG_PATH = Path('config.yaml')

SUCCESS_PATH = 'SUCCESS'
FAILURE_PATH = 'FAILURE'

LOGS_DIR = Path('logs')
STDOUT_BASENAME = 'out'
STDERR_BASENAME = 'err'
OUT_PATH = LOGS_DIR / STDOUT_BASENAME
ERR_PATH = LOGS_DIR / STDERR_BASENAME
RUNNER_LOGS_DIR = Path('runner')
RUNNER_STDOUT_BASENAME = 'out'
RUNNER_STDERR_BASENAME = 'err'

DOCKERFILE_PATH = 'Dockerfile'
GIT_CONFIG_PATH = Path('conf') / '.gitconfig'

DEFAULT_IMAGE_BASE = 'runsascoded/gsmo'
DEFAULT_IMAGE_VERSION = 'v0.1'

EARLY_EXIT_EXCEPTION_MSG_PREFIX = 'OK: '

CRON_MODULE_RC = '.cron-module-rc'
CRON_MODULE_RC_ENV = 'CRON_MODULE_RC'

JUPYTER_KERNEL_NAME = '3.7.4'
