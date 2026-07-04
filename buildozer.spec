[app]
# (str) Title of your application
title = PK10助手

# (str) Package name
package.name = pk10helper

# (str) Package domain (needed for android/ios)
package.domain = com.pk10

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching (let empty to include all the files)
#source.include_patterns = assets/*,images/*.png

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
version.code = 1

# (list) Application requirements
# python3,kivy,requests,json,os,threading
requirements = python3,kivy,requests,charset-normalizer,idna,urllib3,certifi

# (str) Custom source folder for requirements (if None, then there is no custom folder)
#source.dir = requirements

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 24

# (str) Android NDK version to use
android.ndk = 23b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library instead of creating one (will copy glut library)
android.copy_libs = 1

# (str) The Android arch to build for
android.arch = armeabi-v7a

# (bool) enables Android advanced graphics mode
android.graphics = 1

# (bool) Enable BB10 compilation
bb10 = 0

# (str) Path to the additional BlackBerry NDK
bb10.ndk = ~/bb10/ndk

# (str)compilation mode
build.mode = debug

# (bool) Clean on build
build.clean = 0

# (bool) Clean all on build
build.clean_all = 0

# (bool) Compile with cython
build.cython = 0

# (bool) Use the build pretend server
build.pretend = 0

# (str) Build output directory
build.dir = /tmp/build

# (bool) Ignore build errors
build.ignore_error = 0

# (bool) Ignore build warnings
build.ignore_warning = 0

# (bool) Use the build force server
build.force = 0

# (bool) Build for iOS
ios = 0

# (str) iOS SDK version
ios.sdk = 13.2

# (str) iOS minimum version
ios.min_ios_version = 9.0

# (str) iOS frameworks
ios.frameworks = UIKit,Foundation,AVFoundation,CoreGraphics,CoreLocation,CoreTelephony,CoreMedia,CoreVideo,Security,SystemConfiguration

# (bool) iOS bitcode
ios.bitcode = 0

# (str) iOS plist template
ios.plist = ~/ios/plist

# (str) iOS codesign key
ios.codesign.key = ~/ios/codesign

# (str) iOS codesign cert
ios.codesign.cert = ~/ios/codesign

# (str) iOS codesign identity
ios.codesign.identity = ~/ios/codesign

# (str) iOS provisioning profile
ios.provisioning_profile = ~/ios/provisioning

# (bool) iOS packager
ios.packager = 0

# (bool) iOS skip code signing
ios.skip_code_signing = 0

# (bool) iOS use simulator
ios.use_simulator = 0

# (bool) iOS validate code signing
ios.validate_code_signing = 0

[buildozer]
# (int) Log level (0 = quiet, 1 = info, 2 = debug)
log_level = 2

# (str) Path to build artifact
bin_dir = bin
