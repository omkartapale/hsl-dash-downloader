# MPEG - DASH, HSL Stream Downloader
Provides ease to save MPEG DASH and HLS fragmented videos. Currently this package outputs ffmpeg command for provided m3u8 url, so that you can download it using your command prompt or terminal.

The another main feature is this allows you to select video resolution if m3u8 supports multiple play streams.

## Pre-requisites and Dependencies
- Python
- M3U8 Parser
```
$ pip3 install m3u8
```
- FFMPEG
```
$ sudo apt install ffmpeg
```
For more reference on how to install FFMPEG, visit here https://www.ffmpeg.org/download.html


### TODO's
- Currently only supports m3u8, add dash parser
- Enable user to provide desired format extension
