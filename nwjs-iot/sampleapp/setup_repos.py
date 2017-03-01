#!/usr/bin/env python
#
# Copyright (c) 2016 Intel Corporation.
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
#         Jiang, Xiuqi<xiuqix.jiang@intel.com>

import os
import sys
import random
import commands

SCRIPT_PATH = os.path.realpath(__file__)
CONST_PATH = os.path.dirname(SCRIPT_PATH)
submodule_cmd = "git submodule update --init --recursive"

#Clone projects and create package.json files
def clone_projects():
    #[project_url, save_url, [[create_file_path1, create_file_content1], [create_file_path2, create_file_content2]]]
    hexgl = ['https://github.com/BKcore/HexGL.git',
             'HexGL',
             [
             ['HexGL', '{"name": "HexGL", \n "main": "index.html"}']
             ],
             'plainrepo'
            ]
    samples = ['https://github.com/crosswalk-project/crosswalk-samples.git',
               'samples',
               [
               ['samples/simd-mandelbrot', '{"name": "SIMD", \n "main": "index.html"}'],
               ['samples/space-dodge-game/base', '{"name": "SpaceDodge", \n "main": "index.html"}'],
               ['samples/webgl', '{"name": "WebGLSample", \n "main": "index.html"}'],
               ],
               'plainrepo'
              ]
    demos = ['https://github.com/crosswalk-project/crosswalk-demos.git',
             'demos',
             [
             ['demos/MemoryGame/src', '{"name": "MemoryGame", \n "main": "app/index.html"}']
             ],
             'recursiverepo'
            ]
    projects = [hexgl, samples, demos]

    for project in projects:
        repo_dir = os.path.join(CONST_PATH, project[1])
        # print(repo_dir)
        if os.path.exists(repo_dir):
            print('Repository %s already exists, update it.' % project[1])
            os.chdir(repo_dir)
            if project[3] == 'plainrepo':
                update_cmd = 'git pull'
            else:
                update_cmd = 'git submodule update'
            os.system(update_cmd)
        else:
            print('Repository %s not found, clone it.' % project[1])
            print("Clone into %s." %  project[1])
            status = commands.getstatusoutput("git clone %s %s" % (project[0], project[1]))
            if status[0] == 0:
                print("Clone into submodule repos.")
                os.chdir(project[1])
                tpstatus = commands.getstatusoutput(submodule_cmd)
                if tpstatus[0] == 0:
                    os.chdir(CONST_PATH)
                    print("Clone into %s done." % project[1])
                else:
                    print("Clone into %s failed." % project[1])
                    print(tpstatus[1])
                    sys.exit(1)
            else:
                print("Clone into %s failed." % project[1])
                print(status[1])
                sys.exit(1)
        
        os.chdir(CONST_PATH)   
        print(os.getcwd())
        for sample in project[2]:
            print("Create %s/package.json." % sample[0])
            create_pkg_file(sample[0], sample[1])        
     
def create_pkg_file(path, cmd):
    try:

        f=open("%s/package.json" % path, "w")
        f.write(cmd)
        f.close()

        print("Create %s/package.json done." % path)
    except Exception as e:
        print(e)
        print("Create %s/package.json failed." % path)
        sys.exit(1)

def main():
    os.chdir(CONST_PATH)
    clone_projects()

if __name__ == '__main__':
    main()
