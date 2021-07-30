#!/bin/sh

OTG_API_VERSION=0.4.10

# Avoid warnings for non-interactive apt-get install
export DEBIAN_FRONTEND=noninteractive

install_deps() {
	# Dependencies required by this project
    apt-get update \
	&& apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install python-is-python3 python3-pip \
    && python -m pip install --default-timeout=100 -r requirements.txt \
    && apt-get -y clean all
}

install_ext_deps() {
    apt-get -y install curl vim git \
    && python -m pip install --default-timeout=100 flake8 requests pytest pytest-cov pytest_dependency \
    && apt-get -y clean all
}

get_otg_proto() {
    echo "Fetching OTG proto for ${OTG_API_VERSION} ..."
    rm -rf grpc_serve/proto> /dev/null 2>&1 || true
    mkdir -p grpc_serve/proto \
    && curl -kL https://github.com/open-traffic-generator/models/releases/download/v${OTG_API_VERSION}/otg.proto> ./grpc_serve/proto
}

gen_py_stubs() {
    echo "Generating python stubs ..." \
    rm -rf grpc_serve/autogen/*.py> /dev/null 2>&1 || true
    python -m grpc_tools.protoc --experimental_allow_proto3_optional -I./grpc_server/proto --python_out=./grpc_server/autogen --grpc_python_out=./grpc_server/autogen ./grpc_server/proto/otg.proto \
    && sed -i "s/import otg_pb2/from . import otg_pb2/g" grpc_server/autogen/*_grpc.py
}

run() {
    python -m ./grpc_server ${@}
}

run_unit_test() {
    python -m pytest -p no:cacheprovider --cov=./grpc_server
    rm -rf ./grpc_server/__pycache__
    rm -rf ./tests/__pycache__
    rm -rf ./tests/.pytest_cache
    rm .coverage
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
	*   )
        $1 || echo "usage: $0 [deps|ext|clean|run|art|unit]"
		;;
esac
