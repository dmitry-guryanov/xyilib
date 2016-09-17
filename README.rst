Library for Xiaomi YI action camera manipulation
================================================

The goal of this project is to provide convenient way to control
Xiaomi YI action camera from PC.

----
This camera has built-on Wi-Fi and acts like access point by
default. But with some effort it can connect to Wi-Fi access
point. It's required to control several cameras from one
computer, for example.

The main API entry point is <camera ip>:7878. The protocol is
JSON-based and asyncronous. That means that you're getting JSON
objects from read-end of the socket, which could be a response
to your request and a message with information of some event,
like changing battelry level or pressing button on a camera.
