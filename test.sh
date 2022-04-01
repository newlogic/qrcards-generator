#!/usr/bin/env bash

docker build -f Dockerfile -t newlogic/qrcards_generator . > /dev/stderr
if [ -z "$1" ]
then
      TEMPLATE="card.svg"
else
      TEMPLATE=$1
fi
OUTPUT=$(docker run -it --rm -v $PWD/output:/app/output newlogic/qrcards_generator --cards 8 --batch 1 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code=' --card-template $TEMPLATE)
PDF_PATH=$(echo -n $OUTPUT | sed "s@^.*/app/@@g" | sed "s/\s$//")
xdg-open "$PDF_PATH"
