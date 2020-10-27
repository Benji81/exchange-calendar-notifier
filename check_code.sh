#!/bin/bash
set -e -x
cp requirements.txt requirements-new.txt
sha256sum requirements-new.txt > sum.txt
poetry export -f requirements.txt > requirements-new.txt
echo "If this fails, rebuild requirement.txt with previous line"
sha256sum -c sum.txt
rm sum.txt requirements-new.txt

poetry run black --check .
poetry run isort --check .
find . -name '*.py' | xargs poetry run pylint --output-format=colorized
poetry run bandit --exclude venv -r .
echo -e "\n\033[0;32mAll tests are OK, you can commit"

