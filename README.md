# Taking Python to Production - Python Package Template

1. created folder
1. `git init; git branch -M main`
1. `mkdir '{{cookiecutter.repo_name}}'`
1. `cp -R ../packaging/* ../packaging/.* '{{cookiecutter.repo_name}}'`
1. deleted the venvs since they're bad when moved
1. remove the .git folder inside of cookiecutter.repo_name
1. `cd '{{cookiecutter.repo_name}}'; ./run.sh clean`
