#
# Testing
#
# run all test cases with all debug message 
test:
	@pytest tests/ -k 'not playground' --pdb
test-debug:
	@pytest tests/ -k 'not playground' --pdb --log-cli-level DEBUG
test-parallel:
	@pytest tests/ -k 'not playground' --workers auto --verbose

#
# Typecheck
#
# generally, do these check before each major commit
typecheck:
	@mypy --strict avdl
typecheck-test:
	@mypy tests 
typecheck-everything: typecheck typecheck-test

#
# All
#
# test and check everything possible
test-and-typecheck: test typecheck typecheck-test
test-parallel-and-typecheck: test-parallel typecheck typecheck-test
typecheck-and-test: typecheck typecheck-test test
typecheck-and-test-parallel: typecheck typecheck-test test-parallel


#
# Pip requirements gen
#
# scan for project requirements
requirements:
	@pipreqs ./trbox --savepath ./requirements.txt 
	@echo; echo 'requirements.txt:'; cat ./requirements.txt
requirements-print:
	@pipreqs ./trbox --print

