#!/bin/bash
# run.sh
#
# This script starts a Linux container mapped to your Tavros git clone.
# The container shell presented will contain various tools and dependencies
# needed to work on Tavros. This saves much explanation and time.
#

docker run -it --rm -v $PWD:$PWD:Z -w $PWD ghcr.io/ms3inc/tavros-collection:latest
