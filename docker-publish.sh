#!/bin/sh

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

    TAG=$(head ./version | cut -d' ' -f1)
    echo "Main Branch ..."
    DOCKERHUB_IMAGE="${DOCKERHUB_REPO}/ixia-c-grpc-server:${TAG}"
    dockerhub_image_exists "${DOCKERHUB_IMAGE}"
    echo "Publishing image to DockerHub..."
    docker tag ixia-c-grpc-server "${DOCKERHUB_IMAGE}"

    docker login -p ${DOCKERHUB_KEY} -u ${DOCKERHUB_USER} \
    && docker push "${DOCKERHUB_IMAGE}" \
    && docker logout ${DOCKERHUB_USER}
    echo "${DOCKERHUB_IMAGE} published in DockerHub..."


    echo "Deleting local docker images..."
    docker rmi -f "ixia-c-grpc-server" "${DOCKERHUB_IMAGE}"> /dev/null 2>&1 || true

    echo "Verifying image from DockerHub..."
    verify_dockerhub_images "${DOCKERHUB_IMAGE}"
    docker rmi -f "ixia-c-grpc-server"> /dev/null 2>&1 || true
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
        publish
        ;;
	*   )
        $1 || echo "usage: $0 [publish]"
		;;
esac