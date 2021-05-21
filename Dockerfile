# Python - gNMI docker image

FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get -y install --no-install-recommends python3-pip 

WORKDIR /home/otg-grpc

COPY . /home/otg-grpc/

RUN python3 -m pip install --upgrade -r requirements.txt

ENTRYPOINT [ "python3", "-m", "otg_grpc" ]

# default server port
EXPOSE 40051

# sudo docker build -t otg-grpc-server:latest .
# sudo docker run -p 40051:40051 --rm --name otg-grpc-server-instance otg-grpc-server:latest \
#		--server-port 40051 --app-mode ixnetwork \
#  		--target-host 10.72.46.133 --target-port 443
# sudo docker exec -it otg-grpc-server-instance sh

