FROM debian:bullseye-20211011-slim as stage1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    cmake python3 python3-pip git cmake libboost-container1.74-dev libboost-program-options1.74-dev libboost-thread1.74-dev
RUN git clone https://github.com/Mstrutov/Desbordante.git
WORKDIR /app/Desbordante
RUN ./build.sh


FROM python:3.9-slim-bullseye as buildPythonRequirements
COPY requirements.txt requirements.txt 
RUN python3 -m pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt 


FROM python:3.9-slim-bullseye
RUN apt-get update && apt-get install -y \
    dmidecode   
WORKDIR /
COPY --from=stage1 /app/Desbordante/build/target/Desbordante_run /app/Desbordante/build/target/Desbordante_run
COPY --from=buildPythonRequirements /wheels /app/wheels
RUN python3 -m pip install /app/wheels/*
COPY . .
WORKDIR /app
ENTRYPOINT ["python3", "main.py"]
CMD ["dmidecode"]