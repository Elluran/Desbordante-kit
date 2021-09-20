FROM debian:bookworm-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3 python3-dev python3-pip git libboost-all-dev dmidecode cmake
RUN git clone https://github.com/Mstrutov/Desbordante.git
WORKDIR /app/Desbordante
RUN ./build.sh
WORKDIR /
COPY requirements.txt requirements.txt 
RUN python3 -m pip install -r requirements.txt 
COPY . .
WORKDIR /app
CMD python3 main.py