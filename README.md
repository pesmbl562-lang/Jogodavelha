# Jogo da Velha Offline — Python/Kivy

Projeto completo de um jogo da velha para Android, feito em Python.

## Recursos incluídos

- Partida para duas pessoas no mesmo celular.
- Partida contra o computador.
- Dificuldade fácil.
- Dificuldade difícil com algoritmo Minimax.
- Placar salvo no próprio aparelho.
- Funcionamento totalmente offline.
- Sem anúncios, cadastro, internet ou permissões sensíveis.
- Projeto preparado para gerar APK de teste e AAB para a Play Store.

## Estrutura

- `main.py`: regras do jogo e inteligência do computador.
- `jogodavelha.kv`: interface visual editável.
- `buildozer.spec`: configuração Android.
- `assets/`: ícone e tela de abertura.
- `playstore/`: textos e artes iniciais para a ficha da loja.

## Testar no computador

Abra um terminal dentro da pasta do projeto:

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements-desktop.txt
python main.py
```

No Linux:

```bash
source .venv/bin/activate
pip install -r requirements-desktop.txt
python main.py
```

## Gerar Android no Windows com WSL

O Buildozer compila Android em Linux ou macOS. No Windows, use o WSL com Ubuntu.

No PowerShell como administrador:

```powershell
wsl --install -d Ubuntu
```

Reinicie o computador, abra o Ubuntu e instale os pacotes:

```bash
sudo apt update
sudo apt install -y \
  git zip unzip openjdk-17-jdk python3-pip python3-venv \
  autoconf automake libtool pkg-config cmake \
  zlib1g-dev libncurses5-dev libncursesw5-dev \
  libffi-dev libssl-dev
```

Entre na pasta do projeto pelo WSL. Exemplo:

```bash
cd /mnt/c/Users/SEU_USUARIO/Downloads/jogo_da_velha_offline
```

Crie o ambiente e instale o Buildozer:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython
```

### APK para testar no celular

```bash
buildozer -v android debug
```

O APK aparecerá na pasta `bin/`.

### AAB para enviar à Play Store

```bash
buildozer -v android release
```

O AAB aparecerá na pasta `bin/`.

## Assinar o AAB

Antes do primeiro envio, crie uma chave de upload e guarde-a em local seguro:

```bash
keytool -genkeypair -v \
  -keystore upload-keystore.jks \
  -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
```

Assine o arquivo gerado, substituindo o nome pelo arquivo real da pasta `bin/`:

```bash
jarsigner -verbose \
  -sigalg SHA256withRSA \
  -digestalg SHA-256 \
  -keystore upload-keystore.jks \
  bin/jogodavelhaoffline-1.0.0-arm64-v8a_armeabi-v7a-release.aab \
  upload
```

Confira a assinatura:

```bash
jarsigner -verify -verbose -certs \
  bin/jogodavelhaoffline-1.0.0-arm64-v8a_armeabi-v7a-release.aab
```

Nunca publique nem envie a outras pessoas:
- `upload-keystore.jks`
- a senha da chave
- o alias e senhas em arquivos públicos

## Alterações importantes antes de publicar

No `buildozer.spec`, confira:

```ini
package.domain = br.com.emanoelviana
package.name = jogodavelhaoffline
```

O identificador completo será:

```text
br.com.emanoelviana.jogodavelhaoffline
```

Escolha o identificador definitivo antes da primeira publicação. Depois de publicado, ele não deve ser alterado.

Para cada atualização:

```ini
version = 1.0.1
android.numeric_version = 2
```

O `android.numeric_version` precisa sempre aumentar.

## Checklist da Play Store

1. Criar uma conta no Google Play Console.
2. Criar o aplicativo com o idioma principal em português do Brasil.
3. Preencher nome, descrição curta e descrição completa.
4. Enviar ícone, capturas de tela e gráfico de recurso.
5. Informar que o aplicativo não coleta nem compartilha dados.
6. Preencher classificação de conteúdo.
7. Definir público-alvo.
8. Criar um teste interno ou fechado.
9. Enviar o arquivo `.aab` assinado.
10. Corrigir qualquer aviso apresentado pelo Play Console antes de produção.

## Observação técnica

A configuração usa API 36 e NDK r28c. Isso ajuda a atender às regras anunciadas
para Android 16 e à compatibilidade com páginas de memória de 16 KB. Como o
ecossistema Android muda, confirme os avisos exibidos pelo Play Console no momento
do envio.

## Gerar APK sem instalar ferramentas no computador

O projeto inclui uma automação do GitHub Actions em
`.github/workflows/gerar-apk.yml`. Consulte `GERAR_APK_PELO_GITHUB.md`.
