#!/bin/bash

OTG_API_VERSION=0.4.10


get_model_api() {
    DOWNLOAD_DIR=download/v${OTG_API_VERSION}
    echo -e "\nFetching Model API, version : ${OTG_API_VERSION} ...\n" \
    && mkdir -p ${DOWNLOAD_DIR} \
    && cd ${DOWNLOAD_DIR} \
    && curl -kLO https://github.com/open-traffic-generator/models/releases/download/v${OTG_API_VERSION}/otg.proto \
    && cd ../.. \
    && mkdir -p grpc_server/proto \
    && cp ${DOWNLOAD_DIR}/*.proto grpc_server/proto/ \
    && rm -rf download/v${OTG_API_VERSION} \
    && echo "OTG API Version: ${OTG_API_VERSION}" > version.info
}

gen_model_stubs() {
    echo -e "\nGenerating stubs ...\n" \
    && mkdir -p grpc_server/autogen \
    && python -m grpc_tools.protoc --experimental_allow_proto3_optional -I./grpc_server/proto --python_out=./grpc_server/autogen --grpc_python_out=./grpc_server/autogen ./grpc_server/proto/otg.proto \
    && sed -i "s/import otg_pb2/from . import otg_pb2/g" grpc_server/autogen/*_grpc.py
}

upddate_code() {
    echo -e "\nUpdating Model version info in source code ...\n" \
    && sed -i "s/^OTG_API_Version.*$/OTG_API_Version=\"${OTG_API_VERSION}\"/" grpc_server/__main__.py \
    && sed -i "s/^LABEL .*$/LABEL OTG_API_Version=\"${OTG_API_VERSION}\"/" Dockerfile
}

update_model() {
    # Get model API and generate stubs
    get_model_api    \
    && gen_model_stubs \
    && upddate_code
}

case $1 in

    update     )
        update_model
        ;;

	*		)
        $1 || echo "usage: $0 [update]"
		;;
esac
