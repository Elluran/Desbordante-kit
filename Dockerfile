FROM debian:bookworm-slim as stage1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    cmake python3 python3-pip git dmidecode cmake libboost-container1.74-dev libboost-program-options1.74-dev libboost-thread1.74-dev; \
    rm -rf /var/lib/apt/lists/* 
RUN git clone https://github.com/Mstrutov/Desbordante.git
WORKDIR /app/Desbordante
RUN ./build.sh; rm -rv datasets build/target/inputData build/src/libfdtester_lib.a

FROM python:3.9-slim-bullseye
WORKDIR /app
RUN apt-get update && apt-get install -y \
    dmidecode   
COPY --from=stage1 /app/Desbordante/build/target/fdtester_run /app/Desbordante/build/target/fdtester_run
WORKDIR /
COPY requirements.txt requirements.txt 
RUN python3 -m pip install -r requirements.txt 
COPY . .
WORKDIR /app
CMD python3 main.py