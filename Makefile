test:
	python3 src/test.py

setup:
	[ -e build.zip ] && rm build.zip ; echo "No build yet"
	python3 src/setup.py build
	zip -r build.zip build


