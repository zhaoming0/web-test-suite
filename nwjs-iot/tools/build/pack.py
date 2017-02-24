#!/usr/bin/env python
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

import os
import json
import shutil

build_dir = os.path.dirname(os.path.abspath(__file__))
nwjs_iot_dir = os.path.dirname(os.path.dirname(build_dir))
nwjs_test_suite = 'nwjs_test_suite'
nwjs_test_suite_dir = os.path.join(build_dir, nwjs_test_suite)

# print(build_dir)
# print(nwjs_iot_dir)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def pack_webapi_tests(package_list_file):
    '''Collect all the WebAPI test case files and copy to the webapi directory.
    '''
    global build_dir
    global nwjs_iot_dir
    global nwjs_test_suite
    global nwjs_test_suite_dir

    nwjs_test_suite_zip = nwjs_test_suite_dir + '.zip'
    if os.path.exists(nwjs_test_suite_zip):
        print('removing ' + nwjs_test_suite_zip)
        os.remove(nwjs_test_suite_zip)
    if os.path.exists(nwjs_test_suite_dir):
        print('removing ' + nwjs_test_suite_dir)
        shutil.rmtree(nwjs_test_suite_dir)

    webapi_dir = os.path.join(nwjs_iot_dir, 'webapi')
    nwjs_webapi_dir = os.path.join(nwjs_test_suite_dir, 'webapi')
    shutil.copytree(webapi_dir, nwjs_webapi_dir)

    csswg_cp_dirs = ('support', 'reference')
    web_platform_cp_dirs = ('common', 'images', 'media', 'resources')
    for cp_dir in csswg_cp_dirs:
        print('copying csswg-test/{0} to {1}/{0}'.format(cp_dir, nwjs_webapi_dir, cp_dir))
        shutil.copytree('csswg-test/{0}'.format(cp_dir), 
                        '{0}/{1}'.format(nwjs_webapi_dir, cp_dir))
    for cp_dir in web_platform_cp_dirs:
        print('copying web-platform-tests/{0} to {1}/{0}'.format(cp_dir, nwjs_webapi_dir, cp_dir))
        shutil.copytree('web-platform-tests/{0}'.format(cp_dir), 
                        '{0}/{1}'.format(nwjs_webapi_dir, cp_dir))

    with open(package_list_file) as fp:
        package_list = json.load(fp)
    for folder_name in sorted(package_list.get('package_list')):
        spec = None
        spec_file = os.path.join(nwjs_webapi_dir, folder_name, 'spec.json')
        if not os.path.exists(spec_file):
            print(spec_file + ' does not exist!')
            continue

        with open(spec_file) as fp:
            spec = json.load(fp)

        if not spec:
            print('Failed to get spec json object from {0}'.format(spec_file))
            continue

        from_repo_urls = spec.get('test_origin')
        for from_url in from_repo_urls:
            from_dir = ''
            if from_url.startswith('https://github.com/w3c/csswg-test'):
                from_dir = from_url.replace('https://github.com/w3c/csswg-test/tree/master',
                                            'csswg-test')
            elif from_url.startswith('https://github.com/w3c/web-platform-tests'):
                from_dir = from_url.replace('https://github.com/w3c/web-platform-tests/tree/master',
                                            'web-platform-tests')
            else:
                from_dir = os.path.join('crosswalk-test-suite', 'webapi', from_url, folder_name)
                if not os.path.exists(from_dir) and 'htmlsvg' in from_dir:
                    from_dir = from_dir.replace('htmlsvg', 'svg')
            print('copying {0} to {1}'.format(from_dir, nwjs_webapi_dir))
            if not from_dir.startswith('crosswalk-test-suite'):
                if len(from_repo_urls) == 1:
                    copytree(from_dir, '{0}/{1}'.format(nwjs_webapi_dir, folder_name))
                else:
                    last_part = from_dir.split('/')[-1]
                    shutil.copytree(from_dir, '{0}/{1}/{2}'.format(nwjs_webapi_dir, folder_name, last_part))


def pack_nwjs_tests():
    '''
    Copy nw.js/tests to nwjs_test_suite/
    '''
    global build_dir
    global nwjs_test_suite_dir
    assert os.path.exists(nwjs_test_suite_dir), 'nwjs_test_suite directory does not exist!'
    
    nwjs_upstream_test_dir = os.path.join(build_dir, 'nw.js', 'test')    
    upstream_dir = os.path.join(nwjs_test_suite_dir, 'nwjsapi', 'upstream')
    if not os.path.exists(upstream_dir):
        os.makedirs(upstream_dir)

    print('copying nw.js upstream test')
    shutil.copytree(nwjs_upstream_test_dir, 
                    os.path.join(upstream_dir, 'test'))


def pack_webqa_tests():
    '''
    Copy WebQA tests(usecase and samplepp) to nwjs_test_suite
    '''
    global nwjs_iot_dir
    global nwjs_test_suite_dir
    assert os.path.exists(nwjs_test_suite_dir), 'nwjs_test_suite directory does not exist!'

    usecase_dir = os.path.join(nwjs_iot_dir, 'usecase')
    sampleapp_dir = os.path.join(nwjs_iot_dir, 'sampleapp')

    print('copying usecase test suite')
    shutil.copytree(usecase_dir, 
                    os.path.join(nwjs_test_suite_dir, 'usecase'))
    print('copying sampleapp test suite')
    shutil.copytree(sampleapp_dir, 
                    os.path.join(nwjs_test_suite_dir, 'sampleapp'))
    os.chdir(build_dir)


if __name__ == '__main__':
    pack_webapi_tests('package_list.json')
    pack_nwjs_tests()
    pack_webqa_tests()

    print('Archiving...')
    shutil.make_archive(nwjs_test_suite, 'zip', nwjs_test_suite_dir)
    print('Done.')