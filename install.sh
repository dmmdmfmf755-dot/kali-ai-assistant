#!/bin/bash

# kali-ai-assistant - Instalador PEP 668 Compliant
# Instala em /opt/kali-ai-assistant usando venv

set -e

INSTALL_DIR="/opt/kali-ai-assistant"
BIN_PATH="/usr/local/bin/kali-ai-assistant"

echo "----------------------------------------------------"
echo "   Instalando kali-ai-assistant (Zero Config)"
echo "----------------------------------------------------"

if [ "$EUID" -ne 0 ]; then
  echo "Erro: Execute como root (sudo ./install.sh)"
  exit 1
fi

# 1. Dependências do Sistema
echo "[*] Instalando python3-venv..."
apt-get update -y -q > /dev/null
apt-get install -y -q python3-venv > /dev/null

# 2. Diretório e Venv
echo "[*] Criando ambiente isolado em $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
python3 -m venv "$INSTALL_DIR/venv"

# 3. Dependências Python (Apenas OpenAI para o motor Zero Config)
echo "[*] Instalando bibliotecas necessárias..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install openai -q

# 4. Arquivos do Projeto
echo "[*] Configurando executáveis..."
cp kali-ai-assistant.py "$INSTALL_DIR/kali-ai-assistant.py"
chmod +x "$INSTALL_DIR/kali-ai-assistant.py"

# 5. Wrapper Global
cat <<EOF > "$BIN_PATH"
#!/bin/bash
# Wrapper para o kali-ai-assistant
source "$INSTALL_DIR/venv/bin/activate"
python3 "$INSTALL_DIR/kali-ai-assistant.py" "\$@"
EOF

chmod +x "$BIN_PATH"

echo "----------------------------------------------------"
echo "   Instalação concluída!"
echo "----------------------------------------------------"
echo "Basta digitar: kali-ai-assistant"
echo "----------------------------------------------------"
