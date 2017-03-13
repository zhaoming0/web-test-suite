#!/usr/bin/env python
'''
Copyright (c) 2016 Intel Corporation.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of works must retain the original copyright notice, this list
  of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the original copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of Intel Corporation nor the names of its contributors
  may be used to endorse or promote products derived from this work without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
#-*- coding: utf-8 -*-

#Version: 0.0.2
#Created: 2015-06-16
#Changed: 2015-06-18: For non-auto tests, there are no name attribute (it's related to the Test Case column),so we fill the column with test id.
#2015-06-18: Add the feature case coverage summary for statistics
#2015-06-18: One line about output the feature converage has some issue and fix it.
#2015-06-29: The runner-results.json file add a test case type field(that is there are three type:
#auto, ref, manual, so we change the stratergy to judge the type of the test case.)
#2017-03-04: Add feature argument in order to update feature section in the csv file.


import os
import sys
import json
import csv
import codecs
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'zhangxiaoyu'
__version__ = '0.0.6'


def fill_csv_file_head():
    '''
    Fill the csv file head and make it easy to extend.
    :param csv_head:
    :return:
    '''
    head = []

    # the columns that are determined at present
    head.append('Feature')
    head.append('Case Id')
    head.append('Test Case')
    head.append('Pass')
    head.append('Fail')
    head.append('N/A')

    # If you want to extend other column, add here.
    head.append('Measured')
    head.append('Comment')
    head.append('Measurement Name')
    head.append('Value')
    head.append('Unit')
    head.append('Target')
    head.append('Failure')
    head.append('Execution Type')
    head.append('Suite Name')
 
    return head


def parse_test_html_path(html,case_feature):
    '''
    Parse the path and return the [1] and [2:], example:
    /tests/2dtransforms/2dtransform_property_exist.html
    :param html:
    :return:
    '''
    html=case_feature+html 
    html_list = html.lstrip('/').split('/')
    feature = html_list[0]
    if case_feature.find('nwjs')!=-1:
        test_id = html_list[-1]
        suite_name=html_list[1]
    else:
        test_id = '/'+'/'.join(html_list[:len(html_list)-1])+'/'+html_list[-1].split('.')[0] 
        suite_name=html_list[2]
    print test_id,suite_name
    return (feature, test_id,suite_name)

def get_suite_name(str_suite):
    try:
        with open('../resources/test_list.json') as f:
            test_list_dic=json.load(f)
    except Exception,e:
        print 'Read test_list.json fail:%s' % e
    for suite_name_key,suite_name_detail in test_list_dic.iteritems():
        if suite_name_key.find(str_suite)!=-1:
            return suite_name_key
        

def json2martrix(json_file,case_feature):
    '''
    Conver the json format file to csv format file.
    :param json_file:
    :param csv_file:
    :return:
    '''
    print 'case_feature=%s' % case_feature 
    json_data = None
    results = None
    csv_data = []

    # statistics column: pass, fail, block
    statistics_data = {
        'auto': [0, 0, 0],
        'manual': [0, 0, 0],
        'ref': [0, 0, 0]
    }
    feature_checkpoints = {}

    csv_head = fill_csv_file_head()
    head_len = len(csv_head)
    csv_data.append(csv_head)


    with open(json_file) as f:
        json_data = json.load(f, encoding = 'utf8')

    if json_data:
        results = json_data.get('results')

    test_num = 0
    feature = None
    test_id = None
    for test in results:
        # process subtests keyword
        test_type = test.get('type')
        subtests = test.get('subtests')
        if test_type == 'auto':
            # There are several sub tests in the current test case.
            # process test keyword
            # START Fixed when test is a list by yunfei [2015.11.16]
            #if isinstance(test.get('test'),list):
            #    html = test.get('test')[0]
            #    print html
            #else:
            #    html = test.get('test')
            #    print html
            # END Fixed when test is a list by yunfei [2015.11.16]
            html = test.get('test')
            if html:
                (feature, test_id,suite_name) = parse_test_html_path(html,case_feature)
            if not feature in feature_checkpoints:
                feature_checkpoints[feature] = [0, 0, 0]
                  
            if subtests:
                if len(subtests)>1:
                    for index, subtest in enumerate(subtests):
                        print index,subtest
                        # Initialize the status row with the head length
                        csv_data_row = ['' for i in xrange(head_len)]
                        subtest_name = subtest.get('name')
                        subtest_status = subtest.get('status').upper()
                        csv_data_row[0] = feature
                        tmp_subtest_name=subtest_name.strip('')
                        csv_data_row[1] = '%s/%d'% (test_id,index+1)
                        csv_data_row[2] = tmp_subtest_name
                        if subtest_status == 'PASS' or subtest_status == 'OK':
                            csv_data_row[3] = '1'
                            statistics_data['auto'][0] += 1
                        elif subtest_status == 'FAIL':
                            csv_data_row[4] = '1'
                            statistics_data['auto'][1] += 1
                        elif subtest_status == 'BLOCK':
                            csv_data_row[5] = '1'
                            statistics_data['auto'][2] += 1
                        csv_data_row[13] = test_type
                        csv_data_row[14] = suite_name
                        feature_checkpoints[feature][0] += 1
                        # Now append the sub test row to the csv data
                        csv_data.append(csv_data_row)
                else: 
                    # Initialize the status row with the head length
                    for index,subtest in enumerate(subtests):
                        csv_data_row = ['' for i in xrange(head_len)]
                        subtest_name = subtest.get('name').strip(' ')
                        subtest_status = subtest.get('status').upper()
                        csv_data_row[0] = feature
                        csv_data_row[1] = test_id 
                        csv_data_row[2] = subtest_name

                        if subtest_status == 'PASS' or subtest_status == 'OK':
                            csv_data_row[3] = '1'
                            statistics_data['auto'][0] += 1
                        elif subtest_status == 'FAIL':
                            csv_data_row[4] = '1'
                            statistics_data['auto'][1] += 1
                        elif subtest_status == 'BLOCK':
                            csv_data_row[5] = '1'
                            statistics_data['auto'][2] += 1
                        csv_data_row[13] = test_type
                        csv_data_row[14] = suite_name
                        feature_checkpoints[feature][0] += 1
                        # Now append the sub test row to the csv data
                        csv_data.append(csv_data_row)
            else:
                # In this suitation, the subtests is empty(that is []), then
                # we can only consider it as one test.
                csv_data_row = ['' for i in xrange(head_len)]

                status = test.get('status').upper()
                csv_data_row[0] = feature
                csv_data_row[1] = test_id 
                csv_data_row[2] = test_id 

                if status == 'PASS' or status == 'OK':
                    csv_data_row[3] = '1'
                    statistics_data['auto'][0] += 1
                elif status == 'FAIL':
                    csv_data_row[4] = '1'
                    statistics_data['auto'][1] += 1
                elif status == 'BLOCK':
                    csv_data_row[5] = '1'
                    statistics_data['auto'][2] += 1
                csv_data_row[13] = test_type
                csv_data_row[14] = suite_name 
                feature_checkpoints[feature][0] += 1
                csv_data.append(csv_data_row)
                print csv_data
                
        else:
            # There are no subtests for the test case. These suituation mainly
            # contains two kinds of cases: manual and reference.

            # process the test keyword
            csv_data_row = ['' for i in xrange(head_len)]
            html = test.get('test')
            status = test.get('status').upper()
            if isinstance(html, basestring) and test_type == 'manual':
                (feature, test_id) = parse_test_html_path(html)
                if not feature in feature_checkpoints:
                    feature_checkpoints[feature] = [0, 0, 0]

                (name_part, ext) = os.path.splitext(test_id)
                if True:
                    # It's a manual test
                    if status == 'PASS' or status == 'OK':
                        csv_data_row[3] = '1'
                        statistics_data['manual'][0] += 1
                    elif status == 'FAIL':
                        csv_data_row[4] = '1'
                        statistics_data['manual'][1] += 1
                    elif status == 'BLOCK':
                        csv_data_row[5] = '1'
                        statistics_data['manual'][2] += 1
                    csv_data_row[13] = test_type
                    csv_data_row[14] = suite_name 
                    feature_checkpoints[feature][2] += 1
            elif isinstance(html, list) and test_type == 'reference':
                (feature, test_id) = parse_test_html_path(html[0])
                suite_name=html.lstrip('/').split('/')[1]
                if not feature in feature_checkpoints:
                    feature_checkpoints[feature] = [0, 0, 0]

                if status == 'PASS' or status == 'OK':
                    csv_data_row[3] = '1'
                    statistics_data['ref'][0] += 1
                elif status == 'FAIL':
                    csv_data_row[4] = '1'
                    statistics_data['ref'][1] += 1
                elif status == 'BLOCK':
                    csv_data_row[5] = '1'
                    statistics_data['ref'][2] += 1
                csv_data_row[13] = test_type
                csv_data_row[14] = suite_name
                feature_checkpoints[feature][1] += 1

            csv_data_row[0] = feature
            csv_data_row[1] = test_id

            name = test.get('name')
            if name:
                csv_data_row[2] = name
            else:
                csv_data_row[1] = test_id

            csv_data.append(csv_data_row)

    return (csv_data, statistics_data, feature_checkpoints)


def write_csv_file(csv_data, csv_file):
    '''
    Since parse is finished, now we dump the csv_data to the csv file
    '''

    with open(csv_file, 'wb') as csvfobj:
        csvfobj.write(codecs.BOM_UTF8)
        csv_writer=csv.writer(csvfobj)
        for row in csv_data:
             print row
             csv_writer.writerow([str(val).encode('utf8') for val in row])


def write_feature_summary(feature_checkpoints, csv_file):
    '''
    Write the feature case coverage summary.
    :param feature_checkpoints:
    :param csv_file:
    :return:
    '''
    with open(csv_file, 'wb') as csvfobj:
        csv_writer = csv.writer(csvfobj, delimiter = ',')

        head = ['Category', 'Suite Name', 'Spec', 'Total', 'Total_auto',
                    'Total_Ref', 'Total_manual']
        csv_writer.writerow(head)

        for feature, info_list in feature_checkpoints.iteritems():
            data_row = []
            data_row.append('Web Testing Service')
            data_row.append('wts-test')
            data_row.append(feature)
            data_row.append(sum(info_list))
            data_row.append(info_list[0])
            data_row.append(info_list[1])
            data_row.append(info_list[2])

            csv_writer.writerow(data_row)




def print_statistics_info(statistics_data):
    '''
    Print the statistics information.
    :param statistics_Data:
    :return:
    '''
    all_pass = 0
    all_fail = 0
    all_block = 0
    for test_type, info in statistics_data.iteritems():
        print test_type.capitalize()
        print '\tPASS: %-10dFAIL: %-10dBLOCK: %-10d' % (info[0], info[1], info[2])
        all_pass += info[0]
        all_fail += info[1]
        all_block += info[2]
    else:
        print 'All'
        print '\tPASS: %-10dFAIL: %-10dBLOCK: %-10d' % (all_pass, all_fail, all_block)

def main():
    usage = 'Usage: ./json2csv.py -i runner-results.json -f case-feature [-o runner-results.csv] [-s feature_summary.csv]'
    opt_parser = OptionParser(usage = usage)
    opt_parser.add_option('-i', '--input', dest = 'jsonfile',
                          help = 'The input json file of runner resuls')
    opt_parser.add_option('-o', '--output', dest = 'csvfile',
                          help = 'The output csv file parsed from the json file (optional)')
    opt_parser.add_option('-s', '--summary', dest = 'feature_sum',
                          help = 'The output csv file that contains feature case coverage summary information.')
    opt_parser.add_option('-f','--feature',dest = 'casefeature',
                          help = 'The input case feature')

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    (options, args) = opt_parser.parse_args()

    if options.jsonfile:
        (data, statistics, feature_data) = json2martrix(options.jsonfile,options.casefeature)
        
        if options.csvfile:
            write_csv_file(data, options.csvfile)
        else:
            write_csv_file(data, options.jsonfile.replace('json', 'csv'))
        '''
        if options.feature_sum:
            write_feature_summary(feature_data, options.feature_sum)
        else:
            write_feature_summary(feature_data, options.jsonfile.rstrip('.json') + '-feature-summary.csv')
        '''
        print_statistics_info(statistics)
    else:
        sys.stderr.write('Input json file must be specified!\n')
        sys.exit(1)
       


if __name__ == '__main__':
   main()
   print 'test done'
