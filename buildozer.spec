[app]
title = Media Downloader
package.name = mediadownloader
package.domain = org.manus.mediadownloader
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.1,kivymd==1.2.0,yt-dlp,certifi,urllib3,idna,charset-normalizer,requests

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

# Android specific
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# UI
android.presplash_color = #FFFFFF
android.window_softinput_mode = adjustResize

[buildozer]
log_level = 2
warn_on_root = 1
