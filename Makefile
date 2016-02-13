# To run invidual test, try:
# 	make TEST_FLAGS=ft/db/test_issue_27.py test_py2
PY=python3

package:
	# For development only
	$(PY) setup.py sdist

release:
	$(PY) setup.py sdist upload

release-wheel:
	$(PY) setup.py sdist bdist_wheel upload

doc: clean
	cd docs && make clean && make html

doc-update:
	cd docs && make html

test-local: reset-mongodb
	nosetests -x -w . ./test/ut/db ./test/ft/db

install_test_package:
	python setup_for_test_only.py install --compile

reset-mongodb:
	mongo t3test --eval 'db.dropDatabase()' > /dev/null

install:
	$(PY) setup.py install --compile

clean:
	rm -Rf MANIFEST build dist docs/build/* || echo "Nothing to clean"
	find . -name *.pyc -exec rm {} \;
	find . -name __pycache__ -exec rm -Rf {} \;
	find . -name .DS_Store -exec rm {} \;
	find . -name ._* -exec rm {} \;
