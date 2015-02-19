TEST_FLAGS=""

package:
	# For development only
	python setup.py sdist

release:
	python setup.py sdist upload

wheel_release:
	python setup.py sdist bdist_wheel upload

doc: clean
	cd docs && make clean && make html

doc_update:
	cd docs && make html

test: test_py2

test_py2: cache_clean
	nosetests -c nose.cfg $(TEST_FLAGS)

test_py3: cache_clean
	nosetests-3.3 -c nose.cfg $(TEST_FLAGS) || nosetests-3.4 -c nose.cfg

test_ci: cache_clean install_test_package reset_mongodb
	nosetests -c nose.cfg ut/db
	nosetests -c nose.cfg ft/db
	#nosetests -c nose.cfg

install_test_package:
	python setup_for_test_only.py install --optimize 2 --compile

reset_mongodb:
	mongo t3test --eval 'db.dropDatabase()' > /dev/null

install:
	python setup.py install --optimize 2 --compile

cache_clean:
	find . -name *.pyc -exec rm {} \;

clean: cache_clean
	rm -Rf MANIFEST build dist docs/build/*
	find . -name __pycache__ -exec rm -Rf {} \;
	find . -name .DS_Store -exec rm {} \;
	find . -name ._* -exec rm {} \;
