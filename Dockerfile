# STAGE 1 (DEVELOPMENT)
FROM ubuntu:20.04 AS dev
LABEL OTG_API_Version="0.4.10"
ENV SRC_ROOT=/home/keysight/ixia-c/otg-grpc
RUN mkdir -p ${SRC_ROOT}
# Get project source, install dependencies and build it
COPY . ${SRC_ROOT}/
RUN cd ${SRC_ROOT} && chmod +x ./do.sh && ./do.sh deps && ./do.sh art 2>&1
# Ports to be published
EXPOSE 40051
WORKDIR ${SRC_ROOT}
CMD ["/bin/bash"]

# STAGE 2 (PRODUCTION)
FROM ubuntu:20.04 as prod
LABEL OTG_API_Version="0.4.10"
# Ports to be published
ENV SRC_ROOT=/home/keysight/ixia-c/otg-grpc
EXPOSE 40051
RUN mkdir -p ${SRC_ROOT}/grpc_server
COPY --from=dev ${SRC_ROOT}/grpc_server ${SRC_ROOT}/grpc_server/
COPY --from=dev ${SRC_ROOT}/setup.py ${SRC_ROOT}/
COPY --from=dev ${SRC_ROOT}/do.sh ${SRC_ROOT}/
COPY --from=dev ${SRC_ROOT}/requirements.txt ${SRC_ROOT}/
RUN cd ${SRC_ROOT} && chmod +x ./do.sh && ./do.sh deps 2>&1 && rm ./do.sh && rm ./requirements.txt
WORKDIR ${SRC_ROOT}
ENTRYPOINT ["python", "-m", "grpc_server"]
