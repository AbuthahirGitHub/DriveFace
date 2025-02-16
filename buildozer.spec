[app]
title = DriveFace
package.name = driverface
package.domain = org.driverface
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements
requirements = python3,kivy,kivymd,pillow,numpy,opencv,dlib,face_recognition

# Android specific
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 21
android.minapi = 21
android.ndk = 23b
android.sdk = 33
android.presplash.filename = %(source.dir)s/assets/presplash.png
android.icon.filename = %(source.dir)s/assets/icon.png

# Enable androidx
android.enable_androidx = True

# Enable OpenCV
android.enable_opencv = True

# Python for Android specific
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1 