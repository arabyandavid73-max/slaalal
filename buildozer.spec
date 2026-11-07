[app]
title = MVD OSINT
package.name = mvdosint
package.domain = org.mvd
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.skip_update = False
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
