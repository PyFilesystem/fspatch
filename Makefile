
.PHONY: release
release:
	rm dist/*.whl dist/*.tar.gz
	python3 setup.py sdist bdist_wheel
	twine upload dist/*.whl dist/*.tar.gz

.PHONY: docs
docs:
	cd docs && make html
	python -c "import os, webbrowser; webbrowser.open('file://' + os.path.abspath('./docs/build/html/index.html'))"

.PHONY: typecheck
typecheck:
	mypy -p fs --config setup.cfg
