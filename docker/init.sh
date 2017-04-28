#!/bin/bash
set -e -f -u -o pipefail

START_DIR="${PWD}"
DRY_RUN="no"
DOCKER_DIR="${START_DIR}/docker"
DEPENDENCIES_ONLY="no"
NO_CACHE="no"

while [[ $# -gt 0 ]]; do
    option="$1"
    case $option in
        -d|--dry-run)
            DRY_RUN="yes"
            ;;
        -w|--where)
            DOCKER_DIR="$2"
            shift
            ;;
        -o|--dependencies-only)
            DEPENDENCIES_ONLY="yes"
            ;;
        -n|--no-cache)
            NO_CACHE="yes"
            ;;
        -h|--help)
            echo "Initialize Docker images"
            echo "Usage: init.sh [-d] [-w DIR] [-o] [-n]"
            echo "    -d|--dry-run => Do dry run; don't actually build"
            echo "    -w|--where => Location of Docker spec directories [${DOCKER_DIR}]"
            echo "    -o|--dependencies-only => Only build dependencies"
            echo "    -n|--no-cache Don't use cache when building images"
            exit
            ;;
        -*)
            echo "Unknown option: $option" 1>&2
            exit 1
            ;;
    esac
    shift
done

if [ "$DRY_RUN" = "yes" ]; then
    echo "DRY RUN"
fi

if [ "$DEPENDENCIES_ONLY" = "yes" ]; then
    echo "BUILDING DEPENDENCIES ONLY"
fi

if [ "$NO_CACHE" = "yes" ]; then
    echo "NOT USING DOCKER CACHE"
fi

function build {
    local path="${1}"
    local no_cache=""
    if [ "$NO_CACHE" = "yes" ]; then local no_cache="--no-cache"; fi
    cd "${path}"
    local name="${PWD##*/}"
    printf "\n\nRunning 'docker build' in ${PWD}...\n"
    if [ "$DRY_RUN" = "no" ]; then
        docker build -t "${name}" ${no_cache} .
    else
        echo "docker build -t ${name} ${no_cache} ."
    fi
    echo "Done running 'docker build' in ${PWD}."
    cd "$START_DIR"
}

for name in $(ls "${DOCKER_DIR}"); do
    path="${DOCKER_DIR}/${name}"
    if [ -d "${path}" ] && [ -f "${path}/Dockerfile" ]; then
        build "${path}"
    else
        printf "\n\nSkipping non-Docker directory or file: ${path}\n"
    fi
done

if [ "${DEPENDENCIES_ONLY}" = "no" ]; then
    build "${START_DIR}"
fi
