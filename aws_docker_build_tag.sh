#!/bin/bash
set -e

PREFIX="ID_HERE.dkr.ecr.eu-west-2.amazonaws.com"
echo $PREFIX

cd dremio-docker && docker build --file Dockerfile --tag ${PREFIX}/dremio:latest . && cd ..
cd ontop-docker && docker build --file Dockerfile --tag ${PREFIX}/ontop:latest . && cd ..
cd benchmark-docker && docker build --file Dockerfile --tag ${PREFIX}/benchmark:latest . && cd ..

docker push ${PREFIX}/dremio:latest
docker push ${PREFIX}/ontop:latest
docker push ${PREFIX}/benchmark:latest