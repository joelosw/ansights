import os
"""Little Helper for absolute paths. Will evaluate to this repositories path."""
path = os.path.dirname(os.path.realpath(__file__))
while 'src' in path:
    path = os.path.abspath(path+'/..')

__RepoPath__ = path
repo_path = path
