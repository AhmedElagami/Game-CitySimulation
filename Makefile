test: 
	python3 src/tests/graph_test.py
	python3 src/tests/game_test.py
	python3 src/tests/city_test.py

setup:
	rm build.zip
	python3 src/setup.py build
	zip -r build.zip build


