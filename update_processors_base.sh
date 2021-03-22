#!/bin/bash

NEW_TAG=$1

[ "$#" -eq 1 ]                 || { echo "USAGE: $0 <new_tag>" && exit 2; }
[ ! -z "$BLACKFYNN_CODE_DIR" ] || { echo "ERROR: BLACKFYNN_CODE_DIR environment variable not set." && exit 2; }

repos="
etl-nextflow
blackfynn-api
brukertiff-processor
dicom-processor
nifti-processor
ometiff-processor
standard-image-processor
svs-processor
tabular-processor
timeseries-processor
video-processor
"

function git_operations() {
    git checkout DEVELOPMENT 2>/dev/null || git checkout master
    git branch
    git pull
    echo "** git status **"
    git status
}

function update_base() {
    repo=$1

    echo "Updating Dockerfiles..."
    if [ $repo == "blackfynn-api" ]; then
        dockerfile="build.sbt"

        echo " - Dockerfile = $dockerfile"
        OLD_TAG=$(grep blackfynn/base-processor-java-python $dockerfile | sed 's/.*://' | cut -f1 -d '"' | head -n 1)
        sed -i.bak "s/$OLD_TAG/$NEW_TAG/" $dockerfile
        git commit $dockerfile -m "update base image to tag=$NEW_TAG"
    else
        dockerfiles=$(find . -name "Dockerfile")

        for dockerfile in $dockerfiles; do
            echo " - Dockerfile = $dockerfile"
            OLD_TAG=$(grep FROM $dockerfile | sed 's/.*://' | cut -f1 -d ' ' | head -n 1)
            sed -i.bak "s/$OLD_TAG/$NEW_TAG/" $dockerfile
            git commit $dockerfile -m "update base image to tag=$NEW_TAG"
        done
    fi

    git push
}


echo ""
echo "Updating the following repos: $repos"
echo ""

for repo in $repos; do
    echo ""
    echo "*************************************************"
    echo "* REPO: ${repo} "
    echo "*************************************************"
    echo ""

    if [[ ! -d "$BLACKFYNN_CODE_DIR/${repo}" ]]; then
        echo "No local copy of ${repo} found. Cloning..."
        cd $BLACKFYNN_CODE_DIR
        git clone git@github.com:Blackfynn/${repo}.git
    fi

    cd $BLACKFYNN_CODE_DIR/$repo

    git_operations

    read -p "Would you like to update this repo? (y/n) " user_input

    [ "$user_input" != "y" ] || update_base $repo
done
