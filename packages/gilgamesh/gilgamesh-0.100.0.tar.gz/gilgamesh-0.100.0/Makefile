dist:
	python3 setup.py sdist bdist_wheel
dist-testupload: clean dist
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
dist-upload: clean dist
	python3 -m twine upload dist/*
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf gilgamesh.egg-info/
