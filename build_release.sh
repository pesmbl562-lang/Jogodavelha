#!/usr/bin/env bash
set -euo pipefail

if ! command -v buildozer >/dev/null 2>&1; then
  echo "Buildozer não encontrado."
  echo "Ative o ambiente virtual e execute: pip install buildozer cython"
  exit 1
fi

echo "Gerando AAB de publicação..."
buildozer -v android release
echo "Concluído. Assine o arquivo da pasta bin/ antes de enviá-lo à Play Store."
