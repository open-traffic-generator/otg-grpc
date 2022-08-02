#!/bin/sh

SNAPPI_VERSION=0.8.8
UT_REPORT=ut-report.html

# Avoid warnings for non-interactive apt-get install
export DEBIAN_FRONTEND=noninteractive

install_deps() {
	echo "Installing dependencies required by this project"
    apt-get update \
	&& apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install python-is-python3 python3-pip \
    && python -m pip install --default-timeout=100 -r requirements.txt \
    && python -m pip install snappi[ixnetwork]==${SNAPPI_VERSION} \
    && apt-get -y clean all
}

install_ext_deps() {
    echo "Installing extra dependencies required by this project"
    apt-get -y install curl vim git \
    && python -m pip install --default-timeout=100 flake8 requests pytest pytest-cov pytest_dependency pytest-html \
    && apt-get -y clean all
}

run() {
    echo "Running gRPC server ..."
    python -m grpc_server ${@}
}

run_unit_test() {
    echo "Running unit tests ..."
    python -m pytest --html=${UT_REPORT} --self-contained-html ./tests -p no:cacheprovider --cov=./grpc_server
    rm -rf ./grpc_server/__pycache__
    rm -rf ./tests/__pycache__
    rm -rf ./tests/.pytest_cache
    rm -rf ./tests/mockstatus.txt 2>&1 || true
    rm .coverage
}

analyze_unit_test_result() {
    total=$(cat ${UT_REPORT} | grep -o -P '(?<=(<p>)).*(?=( tests))')
    echo "Number of Total Unit Tests: ${total}"
    passed=$(cat ${UT_REPORT} | grep -o -P '(?<=(<span class="passed">)).*(?=( passed</span>))')
    echo "Number of Passed Unit Tests: ${passed}"
    if [ ${passed} = ${total} ]
    then 
        echo "All unit tests are passed..."
    else
        echo "All unit tests are passed, Please check locally!"
        exit 1
    fi
    rm -rf ./${UT_REPORT} 2>&1 || true
}

echo_version() {
    version=$(head ./version | cut -d' ' -f1)
    echo "gRPC version : ${version}"
}

build() {
    docker rmi -f "ixia-c-grpc-server"> /dev/null 2>&1 || true
    echo "Building production docker image..."
    docker build -t ixia-c-grpc-server .
    version=$(head ./version | cut -d' ' -f1)
    echo "gRPC - Server version : ${version}"
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
		install_ext_deps && run_unit_test && analyze_unit_test_result
		;;
    unit    )
        run_unit_test
        ;;
    build    )
        build
        ;;
    version )
        echo_version
        ;;
	*   )
        $1 || echo "usage: $0 [deps|ext|clean|run|art|unit|build|version]"
		;;
esac
