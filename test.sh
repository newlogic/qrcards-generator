#!/usr/bin/env bash

docker build -f Dockerfile -t newlogic/qrcards_generator . > /dev/stderr
OUTPUT=$(docker run -it --rm -v $PWD/output:/app/output newlogic/qrcards_generator --cards 8 --batch 1 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code=')
PDF_PATH=$(echo -n $OUTPUT | sed "s@^.*/app/@@g" | sed "s/\s$//")
xdg-open "$PDF_PATH"
