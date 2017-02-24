# Introduction
This directory contains some scripts to pack necessary WebAPI test files.
These WebAPI test files are from three repositories:
* [csswg-test](https://github.com/w3c/csswg-test.git)
* [web-platform-tests](http://github.com/w3c/web-platform-tests.git)
* [crosswalk-test-suite](http://github.com/crosswalk-project/crosswalk-test-suite.git)

# Usage
## Update the repositories
```
$ ./update_repos.sh
```

## Pack all the files
```
$ ./pack.py
```

After this, there should be a zip file named as <strong>nwjs_test_suite.zip</strong>.