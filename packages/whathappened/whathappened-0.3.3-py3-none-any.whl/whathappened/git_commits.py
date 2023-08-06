# https://gist.github.com/simonw/091b765a071d1558464371042db3b959#file-get_commits-py

import subprocess
import re

leading_4_spaces = re.compile('^    ')


def get_commits(git_log_args=()):
    lines = (
        subprocess.check_output(
            ['git', 'log', '--decorate'] + list(git_log_args), stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split('\n')
    )
    commits = []
    current_commit = {}

    def save_current_commit():
        title = current_commit['message'][0]
        message = current_commit['message'][1:]
        if message and message[0] == '':
            del message[0]
        current_commit['title'] = title
        current_commit['message'] = '\n'.join(message)
        commits.append(current_commit)

    for line in lines:
        if not line.startswith(' '):
            if line.startswith('commit '):
                if current_commit:
                    save_current_commit()
                    current_commit = {}
                sections = line.split(' ', 2)
                current_commit['hash'] = sections[1]
                current_commit['tags'] = []
                try:
                    references = sections[2][1:-1]  # drop brackets
                    references = references.split(', ')

                    for ref in references:
                        if ref.startswith('tag'):
                            current_commit['tags'].append(ref.split(' ')[1])
                except IndexError:  # if commit has no references
                    pass
            else:
                try:
                    key, value = line.split(':', 1)
                    current_commit[key.lower()] = value.strip()
                except ValueError:
                    pass
        else:
            current_commit.setdefault('message', []).append(
                leading_4_spaces.sub('', line)
            )
    if current_commit:
        save_current_commit()
    return commits
