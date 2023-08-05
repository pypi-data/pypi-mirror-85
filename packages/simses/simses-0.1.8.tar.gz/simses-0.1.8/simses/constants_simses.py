import os

from simses import config

ROOT_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\','/') + '/'
CONFIG_PKG_NAME: str = config.__name__.replace('.','/') + '/'
CONFIG_PATH: str = ROOT_PATH + CONFIG_PKG_NAME
BATCH_DIR: str = 'batch/'

#print(ROOT_PATH)

for file in os.listdir(CONFIG_PATH):
    if file.endswith('.ini'):
        # uncomment to track changes of configuration files (locally)
        # subprocess.run(['git', 'update-index', '--no-skip-worktree', CONFIG_PATH + file])
        # uncomment to download last configuration files; Attention: your version will be overwritten!
        # subprocess.run(['git', 'checkout', CONFIG_PATH + file])
        # comment to stop setting untracking changes of configuration files (locally)
        # subprocess.run(['git', 'update-index', '--skip-worktree', CONFIG_PATH + file])
        pass
