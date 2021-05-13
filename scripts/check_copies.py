# check copies of utils.py up-to-date or not

from pathlib import Path

def check_utils():
  with open('./src/templates/template-common/utils.py', 'r') as f:
    common_utils = f.read()

  path = Path('./src/templates/')

  for file in path.rglob('**/utils.py'):
    utils = file.read_text('utf-8')
    if (utils.find(common_utils) > -1):
      print('Matched', file)
    else:
      print('Unmatched', file)


if __name__ == '__main__':
  check_utils()
