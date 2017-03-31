Purpose: Check whether window transparency is effective. 
Test Steps:
           1.Execute command 'nw .' and window displays normally.
           2.Update 'frame' and 'transparent' value in the package.json.The following is:
             "window": {
               "frame": false,
               "transparent": true
             }
           3.Execute command 'nw .' once again.
           4.Test passes if window is transparent.
