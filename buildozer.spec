[app]

title = Jogo da Velha Offline
package.name = jogodavelhaoffline
package.domain = br.com.emanoelviana

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,txt,json,md
source.exclude_dirs = .git,.venv,venv,__pycache__,bin,.buildozer,playstore

version = 1.0.0

requirements = python3,kivy==2.3.1

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait
fullscreen = 0

# API 36 atende à exigência anunciada pelo Google Play para novos apps
# a partir de 31 de agosto de 2026.
android.api = 36
android.minapi = 24
android.ndk_api = 24

# NDK r28+ gera bibliotecas alinhadas para páginas de memória de 16 KB.
android.ndk = 28c

android.archs = arm64-v8a, armeabi-v7a
android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True

# O jogo não precisa de internet, câmera, localização ou outros acessos.
android.permissions =

android.debug_artifact = apk
android.release_artifact = aab

# Precisa aumentar em toda atualização enviada à Play Store.
android.numeric_version = 1

[buildozer]

log_level = 2
warn_on_root = 1
