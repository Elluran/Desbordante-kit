install: install-Desbordante install-requirements 

install-Desbordante:
	git clone https://github.com/Mstrutov/Desbordante.git
	cd Desbordante/; ./build.sh
install-requirements:
	python3 -m pip install -r requirements.txt 

run:
	sudo python3 main.py