Purpose: Put pack app in the same folder of NW.js binaries and can execute app successfully. 
Test Steps:
           1.Pack current all the files into a zip file
             etc: zip -r package-option-2-zip-file.zip ../package-option-2-zip-file/
           2.Copy package-option-2-zip-file.zip to folder of NW.js binaries              
             etc: cp package-option-2-zip-file.zip ~/NW/nwjs-sdk-v0.20.1-linux-x64/ 
           3.Execute command 'nw .' under the NW.js binaries path.
           4.This case will pass if app run and display "success".
