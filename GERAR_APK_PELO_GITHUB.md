# Gerar o APK automaticamente pelo GitHub

Este projeto contém o arquivo:

`.github/workflows/gerar-apk.yml`

Ele configura um computador Linux do GitHub, instala o Android SDK/NDK por meio
do Buildozer, compila o aplicativo e disponibiliza o APK para download.

## Passos

1. Entre em `github.com` e crie uma conta gratuita, caso ainda não tenha.
2. Crie um repositório novo.
3. Descompacte este projeto no computador.
4. Envie todas as pastas e arquivos para o repositório, incluindo a pasta oculta
   `.github`.
5. Abra a guia **Actions** do repositório.
6. Selecione **Gerar APK Android**.
7. Clique em **Run workflow**.
8. Quando a execução terminar, abra a execução concluída.
9. Na seção **Artifacts**, baixe:
   `jogo-da-velha-offline-apk`.
10. Descompacte o arquivo baixado para encontrar o APK instalável.

## Importante

- O arquivo gerado por esse fluxo é um APK de teste, adequado para instalar no
  celular e experimentar o jogo.
- Para publicar na Play Store, gere e assine um AAB de lançamento.
- A primeira compilação baixa ferramentas grandes do Android e pode utilizar
  boa parte do espaço temporário fornecido pelo GitHub.
