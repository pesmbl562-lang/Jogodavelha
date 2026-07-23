#!/usr/bin/env bash
set -euo pipefail

if ! command -v buildozer >/dev/null 2>&1; then
  echo "Buildozer não encontrado."
  echo "Ative o ambiente virtual e execute: pip install buildozer cython"
  exit 1
fi

echo "Gerando APK de teste..."
buildozer -v android debug
echo "Concluído. Verifique a pasta bin/."
