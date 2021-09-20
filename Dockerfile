FROM ubuntu:20.04
WORKDIR /app
ENV TZ=Europe/Moscow
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3 python3-dev python3-pip git
RUN git clone https://github.com/Mstrutov/Desbordante.git
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    cmake wget dmidecode
RUN wget -P /boost https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/boost_1_77_0.tar.gz
WORKDIR /boost
RUN tar xzvf boost_1_77_0.tar.gz
WORKDIR /boost/boost_1_77_0
RUN ./bootstrap.sh --prefix=/usr/
RUN ./b2
RUN ./b2 install

WORKDIR /app/Desbordante
RUN ./build.sh

WORKDIR /
COPY requirements.txt requirements.txt 
RUN python3 -m pip install -r requirements.txt 


COPY . .
WORKDIR /app
CMD python3 main.py