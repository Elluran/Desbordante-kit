dmidecoderes = $(shell sudo dmidecode --type=17 | grep -m 1 'Configured Memory Speed')

build:
	docker image build -t desbordante-kit .
force-build:
	docker image build --no-cache -t desbordante-kit .
run:
	docker run -it --rm \
	--mount type=bind,source="/dev/mem",target="/dev/mem" \
	--mount type=bind,source="$(PWD)/inputData",target="/app/inputData" \
	--mount type=bind,source="$(PWD)/config.json",target="/app/config.json" \
	desbordante-kit "$(dmidecoderes)"
	
