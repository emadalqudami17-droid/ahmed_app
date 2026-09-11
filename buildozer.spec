[app]
title = Ahmed App
package.name = ahmedapp
package.domain = org.ahmed

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,ttf,mp3
source.exclude_dirs = bin,.buildozer,images/raw,audio/raw

version = 1.0.0

requirements = python3,kivy==2.1.0,arabic-reshaper,python-bidi,pyjnius

orientation = portrait
fullscreen = 1
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True
android.permissions = INTERNET
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0