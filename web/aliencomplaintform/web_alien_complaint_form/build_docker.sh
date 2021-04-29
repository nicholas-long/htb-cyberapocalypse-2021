#!/bin/bash
docker rm -f web_alien_complaint_form
docker build -t web_alien_complaint_form . && \
docker run --name=web_alien_complaint_form --rm -p1337:1337 -it web_alien_complaint_form
