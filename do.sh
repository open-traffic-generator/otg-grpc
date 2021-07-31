#!/bin/sh

OTG_API_VERSION=0.4.10

DOCKER_HUB_USERNAME=""
DOCKER_HUB_ACCESS_TOKEN=""
DOCKERHUB_IMAGE=""
EXPERIMENT=""

# Avoid warnings for non-interactive apt-get install
export DEBIAN_FRONTEND=noninteractive

install_deps() {
	echo "Installing dependencies required by this project"
    apt-get update \
	&& apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install python-is-python3 python3-pip \
    && python -m pip install --default-timeout=100 -r requirements.txt \
    && apt-get -y clean all
}

install_ext_deps() {
    echo "Installing extra dependencies required by this project"
    apt-get -y install curl vim git \
    && python -m pip install --default-timeout=100 flake8 requests pytest pytest-cov pytest_dependency \
    && apt-get -y clean all
}

get_otg_proto() {
    echo "Fetching OTG proto for ${OTG_API_VERSION} ..."
    rm -rf grpc_server/proto/> /dev/null 2>&1 || true
    mkdir grpc_server/proto/ \
    && curl -kL https://github.com/open-traffic-generator/models/releases/download/v${OTG_API_VERSION}/otg.proto> ./grpc_server/proto/otg.proto
}

gen_py_stubs() {
    echo "Generating python stubs ..." \
    rm -rf grpc_server/autogen/*.py> /dev/null 2>&1 || true
    python -m grpc_tools.protoc --experimental_allow_proto3_optional -I./grpc_server/proto --python_out=./grpc_server/autogen --grpc_python_out=./grpc_server/autogen ./grpc_server/proto/otg.proto \
    && sed -i "s/import otg_pb2/from . import otg_pb2/g" grpc_server/autogen/*_grpc.py
}

run() {
    echo "Running gRPC server ..."
    python -m grpc_server ${@}
}

run_unit_test() {
    echo "Running unit tests ..."
    python -m pytest ./tests -p no:cacheprovider --cov=./grpc_server
    rm -rf ./grpc_server/__pycache__
    rm -rf ./tests/__pycache__
    rm -rf ./tests/.pytest_cache
    rm .coverage
}

echo_version() {
    version=$(head ./version | cut -d' ' -f1)
    echo "gRPC version : ${version}"
}

cicd_publish_to_docker_repo() {
    version=${1}
    echo "Publishing image to DockerHub..."
    docker tag otg-grpc-server "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version}"

    docker login -p ${DOCKER_HUB_ACCESS_TOKEN} -u ${DOCKER_HUB_USERNAME} \
    && docker push "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version}" \
    && docker logout ${DOCKER_HUB_USERNAME}
    echo "${DOCKER_HUB_USERNAME}/${DOCKERHUB_IMAGE}:${version} published in DockerHub..."
}

cicd() {
    echo "Running CICD build & publish..."

    DOCKER_HUB_USERNAME=${1}
    DOCKER_HUB_ACCESS_TOKEN=${2}
    EXPERIMENT=${3}

    if [ ${EXPERIMENT} = true ]
    then 
        DOCKERHUB_IMAGE=experiments
    else
        DOCKERHUB_IMAGE=otg-grpc-server
    fi

    echo "Building production docker image..."
    docker build -t otg-grpc-server .
    version=$(head ./version | cut -d' ' -f1)
    echo "gRPC - Server version : ${version}"
    cicd_publish_to_docker_repo ${version}
}



clean() {
    rm -rf logs
}

case $1 in
    deps  )
        install_deps
        ;;
    ext   )
        install_ext_deps
        ;;
    clean   )
        clean
        ;;
	run	    )
        # pass all args (except $1) to run
        shift 1
		run ${@}
		;;
	art	    )
		install_ext_deps && get_otg_proto && gen_py_stubs && run_unit_test
		;;
    unit    )
        run_unit_test
        ;;
    cicd    )
        # pass all args (except $1) to run
        shift 1
        cicd ${@}
        ;;
    version )
        echo_version
        ;;
	*   )
        $1 || echo "usage: $0 [deps|ext|clean|run|art|unit|cicd|version]"
		;;
esac
