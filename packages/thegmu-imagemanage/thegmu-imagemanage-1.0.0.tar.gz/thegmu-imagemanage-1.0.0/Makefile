###
# The GMU PyPi Template project Makefile
###

#----------------------------------------------------------------------------------------
### USER REQUIRED CONFIGURATION 

# Edit and load configuration prior to running make using a separete file:
# . bin/activate-thegmu_owncloud_tools
# Example . bin/activate-fun-stuff


#----------------------------------------------------------------------------------------
### DEFAULT/DERIVED CONFIGURATION

### INFORMATION

### FILES/DIRECTORIES
DISTCLEANOBJS:=build dist *.egg-info
DOCSCLEANOBJS:=docs/_*
TOXCLEANOBJS:=.tox
READMEFILE:=README.rst
PYLINTDIRS:=${PYPIPROJECTDIRBASENAME} test
PEP8FILES=$(foreach dir,${PYLINTDIRS},$(wildcard $(dir)/*.py))
VENVACTIVATEFILE:=${PYPIVENVDIR}/bin/activate
SPHINXTHEMEDIR:=$(shell ls -d ${PYPIVENVDIR}/lib/python*/site-packages/sphinx_rtd_theme 2>/dev/null)

### COMMANDS
VENVPYTHONVENV:=${PYPIVENVPYTHON} -m venv
VENVPYTHONPIP:=${PYPIVENVPYTHON} -m pip
VENVACTIVATE:=. ${VENVACTIVATEFILE}
TWINE:=${PYPIVENVDIR}/bin/twine

### TARGETS

.PHONY: _default destroy-docs _require_activation clean clean-dist clean-docs clean-pyc clean-tox deactivate dist docs help init install pep8 project-init publish publish-test pylint test test-dist tox-init

_default: help

_require_activation:
ifeq (${PYPIPROJECTNAME},)
	@echo ""
	@echo "$@ FAILED: please activate the Makefile environment before running 'make'."
	@echo ""
	@echo "Example 'fun-stuff' PYPI environment installed with thegmu-pypi-template:"
	@echo ""
	@echo ". bin/activate-fun-stuff"
	@echo ""
	@false
endif


${VENVDIR}: _require_activation
	@echo "${VENVPYTHONVENV} ${VENVDIR}"
	${VENVPYTHONVENV} ${VENVDIR}

backup-docs:
	bckdir=`mktemp -u`; bckdir=`basename $$bckdir`; bckdir="docs.$$bckdir"; echo $$bckdir; mkdir $bckdir; rsync -av docs/ $$bckdir/; echo "Documents copied to $$bckdir."

clean: clean-pyc clean-tox

clean-dist:
	@echo "Removing package files."
	/bin/rm -rf ${DISTCLEANOBJS}

clean-docs:
	@echo "Removing documentation files."
	/bin/rm -rf ${DOCSCLEANOBJS}

clean-pyc:
	@echo "Removing Python run files."
	for i in $$(find . | grep -E -e"\.pytest_cache|pycache|\.pyc"); do echo $$i; /bin/rm -rf $$i; done

clean-tox: 
	@echo "Removing tox package test files."
	/bin/rm -rf ${TOXCLEANOBJS}

deactivate:
	@echo ""
	@echo "It is not possible to deactivate within the Makefile itself."
	@echo ""
	@echo "To decactivate then source the deactivate-pypi shell script."
	@echo ""
	@echo ". bin/deactivate-pypi"
	@echo ""

dist: _require_activation clean-dist requirements test-dist
	${VENVACTIVATE}; ${VENVPYTHONPIP} install wheel
	${VENVACTIVATE}; ${PYPIVENVPYTHON} setup.py sdist bdist_wheel

docs/sphinx-quickstart-run:
	${VENVACTIVATE}; ${VENVPYTHONPIP} install sphinx sphinx_rtd_theme
	${VENVACTIVATE}; cd docs; sphinx-quickstart
	sed -r -i 's/^#\s*import os/import os/' docs/conf.py
	sed -r -i 's/^#\s*import sys/import sys/' docs/conf.py
	sed -r -i "s/^#\s*sys.path.*/sys.path.insert(0, os.path.abspath('..'))/" docs/conf.py
	sed -r -i "s/^html_theme = .*/html_theme = 'sphinx_rtd_theme'\nhtml_theme_path = ['_themes', ]/" docs/conf.py
	mkdir docs/_themes
	ln -s  ${SPHINXTHEMEDIR} docs/_themes/
	${VENVACTIVATE}; cd docs; sphinx-apidoc -o . ../${PYPIPROJECTDIRBASENAME}
	cd docs;  sed -r -i 's/^exclude_patterns = \[([^]]+)\]/exclude_patterns = [\1, "modules.rst", ]/' conf.py
	cd docs; touch sphinx-quickstart-run

destroy-docs: clean-docs
	@echo ""
	@echo "!!! WARNING !!! This will destroy all manually edited document files."
	@echo ""
	@echo "* Run 'make backup-docs' to back up before destroying. "
	@echo "* If this is a git project then run 'git checkout docs' to recover."
	@echo ""
	/bin/rm -ir docs/*

docs: _require_activation docs/sphinx-quickstart-run
	cp *.rst docs/
	${VENVACTIVATE}; cd docs; make html
	${VENVACTIVATE}; cd docs; grep ${PYPIPROJECTDIRBASENAME} index.rst > /dev/null || (sed -r -i 's/Contents:$$/Contents:\n    \n   ${PYPIPROJECTDIRBASENAME}/' index.rst && (cd docs; make html))

init: requirements project-init

install: dist
	${VENVACTIVATE}; ${VENVPYTHONPIP} install ~/workspace/thegmu/thegmu_imagemanage/dist/*.tar.gz

pep8: _require_activation
	${VENVACTIVATE}; for i in ${PEP8FILES}; do autopep8 -i -a -a -a $$i; done

project-init: _require_activation tox-init
	@echo "Moving project directory"
	@if [ -d "${PYPIPROJECTDIRBASENAME}" ]; then echo "${PYPIPROJECTDIRBASENAME} already exists."; else mv thegmu_pypi_template ${PYPIPROJECTDIRBASENAME}; echo "${PYPIPROJECTDIRBASENAME} created"; fi
	@echo ""
	@echo "Setting 'SCRIPTS' in setup.py to empty."
	@if grep -q '^SCRIPTS = \[\] ' setup.py; then echo "SCRIPTS already disabled." ; else sed -i 's/^SCRIPTS =.*/SCRIPTS = \[\]/g' setup.py; fi
	@echo "Setting 'NAME' in setup.py to ${PYPIPROJECTNAME}."
	@sed -i 's/^NAME =.*/NAME = \"${PYPIPROJECTNAME}\"/g' setup.py;
	@echo "Setting AUTHOR, AUTHOR_EMAIL, DESCRIPTION, and URL blank in setup.py"
	@sed -i 's/^AUTHOR =.*/AUTHOR = \"\"/g' setup.py;
	@sed -i 's/^AUTHOR_EMAIL =.*/AUTHOR_EMAIL = \"\"/g' setup.py;
	@sed -i 's/^DESCRIPTION =.*/DESCRIPTION = \"\"/g' setup.py;
	@sed -i 's/^URL =.*/URL = \"\"/g' setup.py;
	@echo ""
	@echo "Updating test/sample.py with this project name for import."
	@sed -ir 's/from .*/from ${PYPIPROJECTDIRBASENAME}.sample import Sample/g' test/sample_test.py
	@grep 'from ' test/sample_test.py
	@echo ""

publish: _require_activation ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload dist/*

publish-test: _require_activation ${TWINE} dist
	${VENVACTIVATE}; ${TWINE} upload --repository-url https://test.pypi.org/legacy/ dist/*

pylint: _require_activation
	${VENVACTIVATE}; pylint ${PYLINTDIRS} || true

requirements: _require_activation ${VENVDIR} requirements.txt
	${VENVACTIVATE}; ${VENVPYTHONPIP} install --upgrade pip setuptools
	${VENVACTIVATE}; ${VENVPYTHONPIP} install --upgrade -r requirements.txt
	${VENVACTIVATE}; ${VENVPYTHONPIP} freeze

tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

test: _require_activation requirements
	${VENVACTIVATE}; export PYTHONPATH=${PWD}; pytest --verbose --verbosity=2 test

test-dist: _require_activation
	${VENVACTIVATE}; unset PYTHONPATH;  tox

tox-init: _require_activation
	@echo "Updating tox.ini, envlist."
	@sed -i 's/envlist .*/envlist = ${PYPIVENVTOXLIST}/g' tox.ini
	@grep -H envlist tox.ini
	@echo ""

upgrade: _require_activation requirements
	${VENVACTIVATE}; ${VENVPYTHONPIP} list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 ${VENVPYTHONPIP} install -U


help:
	/bin/cat ${READMEFILE}

