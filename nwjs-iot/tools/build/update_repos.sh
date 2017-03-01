#!/bin/bash
#
# Copyright (c) 2017 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Qiu Zhong <zhongx.qiu@intel.com>


TOP_DIR=$(pwd)

CTS="crosswalk-test-suite"
CTS_URL="http://github.com/crosswalk-project/crosswalk-test-suite.git"
CSSWG_TEST="csswg-test"
CSSWG_TEST_URL="https://github.com/w3c/csswg-test.git"
WEB_PLATFORM_TESTS="web-platform-tests"
WEB_PLATFORM_TESTS_URL="http://github.com/w3c/web-platform-tests.git"
NWJS="nw.js"
NWJS_URL="http://github.com/nwjs/nw.js.git"

DEMOS="demos"
DEMOS_URL="https://github.com/crosswalk-project/crosswalk-demos.git"
HEXGL="HexGL"
HEXGL_URL="https://github.com/BKcore/HexGL.git"
SAMPLES="samples"
SAMPLES_URL="http://github.com/crosswalk-project/crosswalk-samples.git"

function update_recursive_repo {
    repo=$1
    url=$2

    if [ ! -d $repo ]; then
        git clone --rescursive --depth 1 --single-branch --branch master $url
    else
        cd $repo
        git pull
        git submodule update
        cd $TOP_DIR
    fi
}

function update_plain_repo {
    repo=$1
    url=$2

    if [ ! -d $repo ]; then
        git clone --rescursive --depth 1 --single-branch --branch master $url
    else
        cd $repo
        git pull
        cd $TOP_DIR
    fi
}

function update_sampleapp() {
    cd $TOP_DIR/../../sampleapp
    python setup_repos.py
    cd $TOP_DIR
}

update_recursive_repo $CSSWG_TEST $CSSWG_TEST_URL
update_recursive_repo $WEB_PLATFORM_TESTS $WEB_PLATFORM_TESTS_URL
update_plain_repo $CTS $CTS_URL
update_plain_repo $NWJS $NWJS_URL

update_sampleapp