#!/bin/bash -e

# To debug each command executed
#set -x

# This will run in the project root
echo -n "    We are in: " && pwd

# We can run git commands
if test -e .git ; then
  echo -n "    Git remote name: "
  git remote
fi

# We can stop going into the other projects by failing
#exit 1

# We can use yq (if it exists) to read the version field from the Circle CI YAML config file (if it exists)
if test -f .circleci/config.yml && which -s yq ; then
  echo -n "    Circle CI config version: "
  yq read -e '.circleci/config.yml' 'version'
fi
