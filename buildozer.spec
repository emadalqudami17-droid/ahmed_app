[app]

# (str) Title of your application
title = Ahmed App

# (str) Package name
package.name = ahmedapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ahmed

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include all extensions)
source.include_exts = py,png,jpg,ttf,wav,mp3,ogg

# (list) List of directory to exclude (skip web/cache folders)
source.exclude_dirs = tests, bin, venv, .git, .github

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,plyer

# (str) Icon of the application
icon.filename = %(source.dir)s/app_icon.png

# (str) Presplash / Splash screen image
presplash.filename = %(source.dir)s/app_icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions needed by the app
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE

# (int) Target Android API, should be as high as possible
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept NDK license automatically
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable Android logcat filter
android.logcat_filters = *:S python:D

# (bool) Copy library directly into APK instead of extracting on boot
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable)
warn_on_root = 0
