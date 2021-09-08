#!/bin/bash

# ignore git changes in credentials and db
git update-index --assume-unchanged .env
git update-index --assume-unchanged database.db