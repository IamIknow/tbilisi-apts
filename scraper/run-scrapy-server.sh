#!/bin/bash

set -m

# Start the scrapyd server in the background
scrapyd &

# Deploy the default target with the scrapyd-deploy tool
scrapyd-deploy container

# Bring scrapyd back to foreground
fg
