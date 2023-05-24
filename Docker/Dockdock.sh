#!/bin/bash

docker build -t <nomdelimage> -f <nom du dockerfile si il ne s'appelle jamais docker .

docker run -d pp:1

dockID=$(docker ps -a --filter "ancestor=<nom de limage" --format "{{.ID}}")

echo $dockID

docker cp $dockID:/output ./output


echo "finished"
