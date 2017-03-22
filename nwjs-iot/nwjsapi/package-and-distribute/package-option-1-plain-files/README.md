Purpose: Put the files of your app in the same folder of NW.js binaries and can execute app successfully. 
Test Steps:
           1.copy 'index.html' and 'package.json' to  folder of NW.js binaries.
             etc: cp index.html package.json ~/NW/nwjs-sdk-v0.20.1-linux-x64/ 
           2.Execute command 'nw .' under NW.js binaries path.
           3.This case will pass if app run and display "success".
