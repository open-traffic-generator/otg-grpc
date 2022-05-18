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

github_docker_image_exists() {
    img=${1}
    docker login -p ${TOKEN_GITHUB} -u biplamal ghcr.io
    if DOCKER_CLI_EXPERIMENTAL=enabled docker manifest inspect ${img} >/dev/null; then
        docker logout ghcr.io
        return 0
    else
        docker logout ghcr.io
        return 1
    fi
}

push_github_docker_image() {
    img=${1}
    echo "Pushing image ${img} in GitHub"
    docker login -p ${TOKEN_GITHUB} -u biplamal ghcr.io \
    && docker push "${img}" \
    && docker logout ghcr.io \
    && echo "${img} pushed in GitHub" \
    && docker rmi "${img}" > /dev/null 2>&1 || true
}

verify_github_images() {
    for var in "$@"
    do
        img=${var}
        echo "pulling ${img} from GitHub"
        docker login -p ${TOKEN_GITHUB} -u biplamal ghcr.io
        docker pull $img
        docker logout ghcr.io
        if docker image inspect ${img} >/dev/null 2>&1; then
            echo "${img} pulled successfully from GitHub"
            docker rmi $img > /dev/null 2>&1 || true
        else
            echo "${img} not found locally!!!"
            docker rmi $img > /dev/null 2>&1 || true
            exit 1
        fi
    done
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

    GITHUB_IMAGE="ghcr.io/open-traffic-generator/ixia-c-grpc-server:${TAG}"
    docker tag ixia-c-grpc-server "${GITHUB_IMAGE}"

    echo "${GITHUB_IMAGE} does not exist..."
    push_github_docker_image ${GITHUB_IMAGE}
    # if github_docker_image_exists ${GITHUB_IMAGE}; then
    #     echo "${GITHUB_IMAGE} already exists..."
    # else
    #     echo "${GITHUB_IMAGE} does not exist..."
    #     push_github_docker_image ${GITHUB_IMAGE}
    # fi

    echo "Deleting local docker images..."
    docker rmi -f "ixia-c-grpc-server" "${DOCKERHUB_IMAGE}" "${GITHUB_IMAGE}"> /dev/null 2>&1 || true

    echo "Verifying image from Docker & Git Hub..."
    verify_dockerhub_images "${DOCKERHUB_IMAGE}"
    verify_github_images ${GITHUB_IMAGE}
    docker rmi -f "ixia-c-grpc-server"> /dev/null 2>&1 || true
}

case $1 in
    publish    )
        publish
        ;;
	*   )
        $1 || echo "usage: $0 [publish]"
		;;
esac