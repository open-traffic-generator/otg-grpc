#!/bin/sh

DOCKER_HUB_USERNAME=""
DOCKER_HUB_ACCESS_TOKEN=""
DOCKERHUB_IMAGE=""
EXPERIMENT=""

# Avoid warnings for non-interactive apt-get install
export DEBIAN_FRONTEND=noninteractive


dockerhub_image_exists() {
    image=${1}
    echo "Checking ${image} already exists in DockerHub or not..."
    docker login -p ${DOCKER_HUB_ACCESS_TOKEN} -u ${DOCKER_HUB_USERNAME}
    if DOCKER_CLI_EXPERIMENTAL=enabled docker manifest inspect $image >/dev/null; then
        echo "${image} already exists in DockerHub, Please use different tag!!!"
        exit 1
    fi
    docker logout ${DOCKER_HUB_USERNAME}
}


publish() {
    DOCKER_HUB_USERNAME=${1}
    DOCKER_HUB_ACCESS_TOKEN=${2}
    EXPERIMENT=${3}

    TAG=$(head ./version | cut -d' ' -f1)

    if [ ${EXPERIMENT} = true ]
    then 
        DOCKERHUB_IMAGE="${DOCKER_HUB_USERNAME}/experiments:${TAG}"
    else
        DOCKERHUB_IMAGE="${DOCKER_HUB_USERNAME}/otg-grpc-server:${TAG}"
        # dockerhub_image_exists "${DOCKERHUB_IMAGE}"
    fi

    echo "Publishing image to DockerHub..."
    docker tag otg-grpc-server "${DOCKERHUB_IMAGE}"

    docker login -p ${DOCKER_HUB_ACCESS_TOKEN} -u ${DOCKER_HUB_USERNAME} \
    && docker push "${DOCKERHUB_IMAGE}" \
    && docker logout ${DOCKER_HUB_USERNAME}
    echo "${DOCKERHUB_IMAGE} published in DockerHub..."


    echo "Deleting local docker images..."
    docker rmi -f "otg-grpc-server" "${DOCKERHUB_IMAGE}"> /dev/null 2>&1 || true

    echo "Verifying image from DockerHub..."
    verify_dockerhub_images "${DOCKERHUB_IMAGE}"
}

verify_dockerhub_images() {
    for var in "$@"
    do
        image=${var}
        echo "pulling ${image} from DockerHub"
        docker pull $image
        if docker image inspect ${image} >/dev/null 2>&1; then
            echo "${image} pulled successfully from DockerHub"
            docker rmi -f $image > /dev/null 2>&1 || true
        else
            echo "${image} not found locally!!!"
            docker rmi -f $image > /dev/null 2>&1 || true
            exit 1
        fi
    done
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