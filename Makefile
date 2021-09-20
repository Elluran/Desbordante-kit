build:
	docker image build -t desbordante-kit .
run:
	docker run -it --privileged \
	--mount type=bind,source="/dev/mem",target="/dev/mem" \
	--mount type=bind,source="$(PWD)/inputData",target="/app/inputData" \
	--mount type=bind,source="$(PWD)/config.json",target="/app/config.json" \
	desbordante-kit
