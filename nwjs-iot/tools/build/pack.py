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
    pwd = os.getcwd()
    top_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    webapi_dir = os.path.join(top_dir, 'webapi')
    with open(package_list_file) as fp:
        package_list = json.load(fp)

    test_suite_dir = 'nwjs_test_suite'
    test_suite_zip = test_suite_dir + '.zip'
    nwjs_webapi_dir = os.path.join(test_suite_dir, 'webapi')

    if os.path.exists(test_suite_zip):
        os.remove(test_suite_zip)

    if os.path.exists(test_suite_dir):
        shutil.rmtree(test_suite_dir)

    shutil.copytree(webapi_dir, '{0}/{1}'.format(pwd, nwjs_webapi_dir))

    csswg_cp_dirs = ('support', 'reference')
    web_platform_cp_dirs = ('common', 'images', 'media', 'resources')

    for cp_dir in csswg_cp_dirs:
        shutil.copytree('csswg-test/{0}'.format(cp_dir), 
                        '{0}/{1}'.format(nwjs_webapi_dir, cp_dir))

    for cp_dir in web_platform_cp_dirs:
        shutil.copytree('web-platform-tests/{0}'.format(cp_dir), 
                        '{0}/{1}'.format(nwjs_webapi_dir, cp_dir))

    for folder_name in sorted(package_list.get('package_list')):
        print('#' * 80)
        print('#' + folder_name)

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

            if not from_dir.startswith('crosswalk-test-suite'):
                if len(from_repo_urls) == 1:
                    copytree(from_dir, '{0}/{1}'.format(nwjs_webapi_dir, folder_name))
                else:
                    last_part = from_dir.split('/')[-1]
                    shutil.copytree(from_dir, '{0}/{1}/{2}'.format(nwjs_webapi_dir, folder_name, last_part))

        print('#' * 80)
    shutil.make_archive(test_suite_dir, 'zip', test_suite_dir)


if __name__ == '__main__':
    pack_webapi_tests('package_list.json')
