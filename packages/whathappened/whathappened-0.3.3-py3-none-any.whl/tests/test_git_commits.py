from whathappened.git_commits import get_commits


with open('tests/git-log.out') as f:
    test_log = f.read().encode("utf-8")


def mock_check_output(args, **kwargs):
    return test_log


def test_get_commits(monkeypatch):
    monkeypatch.setattr('subprocess.check_output', mock_check_output)

    commits = get_commits()

    print(commits)

    expected = [
        {
            'hash': 'e324c324df48a76113ad9b3c0887f161324046e4',
            'tags': ['v0.1.1'],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 17:30:25 2020 +0200',
            'message': '',
            'title': 'breaking feat(readme): specify expected message format',
        },
        {
            'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
            'tags': [],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 15:00:48 2020 +0200',
            'message': '',
            'title': 'breaking fix (code): repair things',
        },
        {
            'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
            'tags': [],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 15:00:48 2020 +0200',
            'message': '',
            'title': 'breaking fix: repair things',
        },
        {
            'hash': '7b4e7e657f9e3f2f4033cc5f47bcc637f5799fe9',
            'tags': [],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 15:00:48 2020 +0200',
            'message': '',
            'title': 'fix: add inspiration',
        },
        {
            'hash': 'f60445bba0ac48e12ce6be5526644037234ae500',
            'tags': ['v0.0.1'],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 15:00:31 2020 +0200',
            'message': '',
            'title': 'docs (readme): add badges',
        },
        {
            'hash': '9e57ba91f54244af913931c017480a39605c15f9',
            'tags': [],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 13:55:04 2020 +0200',
            'message': (
                'Setup Python 3.6 on ubuntu-latest\n'
                'Install pipenv and dependencies\n'
                'Test'
            ),
            'title': 'build(actions): create python-app.yml for github actions',
        },
        {
            'hash': '4094d22846daea951c4fe0d74abb2a798e9a3404',
            'tags': ['v0.0.0'],
            'author': 'Rollcloud <Rollcloud@users.noreply.github.com>',
            'date': 'Sat Oct 17 13:19:28 2020 +0200',
            'message': '',
            'title': 'Initial commit',
        },
    ]

    assert commits == expected
