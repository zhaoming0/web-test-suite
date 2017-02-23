/*
Copyright (c) 2013 Intel Corporation.

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

Authors:
        Xin, liu <xinx.liu@intel.com>

*/

var notification;
var button_Flag = false;

jQuery(document).ready(function() {
  $("#showNotification").attr('disabled', button_Flag);
  $("#closeNotification").attr('disabled', !button_Flag);
});


function showNotification() {
  if (Notification.permission === "granted") {
    notification = typeof Notification != "undefined" ? new Notification("New Email Received", {
      body: "Room 101",
      tag: "tom"
    })
    : window.webkitNotifications.createNotification("New Email Received", {
      body: "Room 101",
      tag: "tom"
    });
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      if (!('permission' in Notification)) {
        Notification.permission = permission;
      }
      if (permission === "granted") {
        notification = typeof Notification != "undefined" ? new Notification("New Email Received", {
          body: "Room 101",
          tag: "tom"
        })
        : window.webkitNotifications.createNotification("New Email Received", {
          body: "Room 101",
          tag: "tom"
        });
      }
    });
  }

  button_Flag = true;
  changeButtionState(button_Flag);
}

function closeNotification() {
  notification.close();

  button_Flag = false;
  changeButtionState(button_Flag);
}

function changeButtionState(flag){
  $("#showNotification").attr('disabled', flag);
  $("#closeNotification").attr('disabled', !flag);
}
