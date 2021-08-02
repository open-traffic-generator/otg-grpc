#!/bin/sh

DOCKER_HUB_USERNAME=""
DOCKER_HUB_ACCESS_TOKEN=""
DOCKERHUB_IMAGE=""
EXPERIMENT=""

# Avoid warnings for non-interactive apt-get install
export DEBIAN_FRONTEND=noninteractive


publish() {
    DOCKER_HUB_USERNAME=${1}
    DOCKER_HUB_ACCESS_TOKEN=${2}
    EXPERIMENT=${3}

    if [ ${EXPERIMENT} = true ]
    then 
        DOCKERHUB_IMAGE=experiments
    else
        DOCKERHUB_IMAGE=otg-grpc-server
    fi

    version=$(head ./version | cut -d' ' -f1)

    echo "Publishing image to DockerHub..."
    docker tag otg-grpc-server "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version}"

    docker login -p ${DOCKER_HUB_ACCESS_TOKEN} -u ${DOCKER_HUB_USERNAME} \
    && docker push "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version}" \
    && docker logout ${DOCKER_HUB_USERNAME}
    echo "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version} published in DockerHub..."
}

case $1 in
    publish    )
        # pass all args (except $1) to run
        shift 1
        publish ${@}
        ;;
	*   )
        $1 || echo "usage: $0 [publish]"
		;;
esac