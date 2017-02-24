## Introduction

This test suite is for testing sample app on NW.js for IoT Linux

## Precondition

1. $ git clone https://github.com/crosswalk-project/crosswalk-samples.git ./samples
   $ echo -e '{"name": "SIMD", \n "main": "index.html"}' > ./samples/simd-mandelbrot/package.json
   $ echo -e '{"name": "SpaceDodge", \n "main": "index.html"}' > ./samples/space-dodge-game/base/package.json
   $ echo -e '{"name": "WebGLSample", \n "main": "index.html"}' > ./samples/webgl/package.json

2. $ git clone https://github.com/crosswalk-project/crosswalk-demos.git ./demos
   $ echo -e '{"name": "MemoryGame", \n "main": "app/index.html"}' > ./demos/MemoryGame/src/package.json

3. $ git clone https://github.com/BKcore/HexGL.git ./HexGL
   $ echo -e '{"name": "HexGL", \n "main": "index.html"}' > ./HexGL/package.json

## Test Method

1. Hosted Website Test
  
   Open terminal command window and launch hosted websites below one by one with command like followings,
   and validate if the page layout, display and the basic function successfully.
  
   $ nw hosted-website/amazon/.
   $ nw hosted-website/baidu/.
   $ nw hosted-website/baidu-map/.
   $ nw hosted-website/bbc/.
   $ nw hosted-website/bing/.
   $ nw hosted-website/collegeconfidential/.
   $ nw hosted-website/facebook/.
   $ nw hosted-website/google/.
   $ nw hosted-website/microsoft/.
   $ nw hosted-website/msn/.
   $ nw hosted-website/netflix/.
   $ nw hosted-website/reddit/.
   $ nw hosted-website/sina/.
   $ nw hosted-website/snopes/.
   $ nw hosted-website/tencent/.
   $ nw hosted-website/weibo/.
   $ nw hosted-website/wikipedia/.
   $ nw hosted-website/wordpress/.
   $ nw hosted-website/yandex/.
   $ nw hosted-website/youtube/.

2. HangOnMan

   Open terminal command window to run the following command, and test if all buttons and function work well.

   $ demos/HangOnMan/src/.

3. hello-world

   Open terminal command window to run the following command, and test if all the information is a correct display.

   $ hello-world/.

4. HexGL

   Open terminal command window to run the following command, and test if all buttons and function work well.

   $ HexGL/.

5. HexGl Presentation

   Setup the test environment about how to make the test device can mirror onto the monitor screen, for example
   using Netgear and test device. Connect the Netgear to the display monitor (the HDMI converter may be needed
   here), then remember the adaptor name of the display monitor. On test device, select "Settings" -> 
   "Wireless & neworks" -> PlayTo, a search dialog will be opened, if everything goes well you can see the
   "MyBox(adaptor name)" available. Then you can connect it and run the HexGL demo with "Remote Display: On".
   Test if it display well onto the monitor screen, and play the game well, no crash, no blank screen.

5. MemoryGame

   Open terminal command window to run the following command, and test if all buttons and function work well.

   $ demos/MemoryGame/src/.


6. simd-mandelbrot

   Open terminal command window to run the following command. Click the "Start", wait a minute and remember the changing
   number, click "Turn On SIMD", Re-click "Turn Off SIMD", then click "Stop". Check if the button value from
   "Turn On SIMD" changes to "Turn Off SIMD", and current number is 1.5 times or more after click "Turn On SIMD".

   $ samples/simd-mandelbrot/.


7. space-dodge-game

   Open terminal command window to run the following command, and test if all buttons and function work well.

   $ samples/space-dodge-game/base/.

8. webgl

   Open terminal command window to run the following command, and test if display a 3D box is rotating.

   $ samples/webgl/.

## Authors:

* Jiang, Xiuqi <xiuqix.jiang@intel.com>

## LICENSE

Copyright (c) 2016 Intel Corporation.
Except as noted, this software is licensed under BSD-3-Clause License.
Please see the COPYING file for the BSD-3-Clause License.
