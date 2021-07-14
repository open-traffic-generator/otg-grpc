# Python - gRPC docker image

FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get -y install --no-install-recommends python3-pip 

WORKDIR /home/otg-grpc

COPY . /home/otg-grpc/

RUN python3 -m pip install --upgrade -r requirements.txt

ENTRYPOINT [ "python3", "-m", "grpc_server" ]

# default server port
EXPOSE 40051

# sudo docker build -t otg-grpc-server:latest .

# run in athena mode
# sudo docker run -p 40051:40051 --rm --name otg-grpc-server-instance otg-grpc-server:latest \
#       --app-mode athena --target-host <host_ip> --target-port 443 \
#       --log-stdout --log-debug

# run in ixnetwork mode
# sudo docker run -p 40051:40051 --rm --name otg-grpc-server-instance otg-grpc-server:latest \
#       --app-mode ixnetwork --target-host <host_ip> --target-port 11009 \
#       --log-stdout --log-debug

# enter into docker container
# sudo docker exec -it otg-grpc-server-instance sh

# run dummy protocol_server
# python3 -m protocol_server --server-port 40041 --log-stdout --log-debug

# run test_client
# python3 -m test_client --target-port 40041 --app-mode athena --config-mode default --log-stdout --log-debug

