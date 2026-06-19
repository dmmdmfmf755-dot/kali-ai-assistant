#!/bin/bash

# kali-ai-assistant - Instalador Robusto (Compatível com PEP 668)
# Este script instala a ferramenta em um ambiente virtual isolado em /opt/kali-ai-assistant

set -e # Encerra o script em caso de erro

INSTALL_DIR="/opt/kali-ai-assistant"
BIN_PATH="/usr/local/bin/kali-ai-assistant"

echo "===================================================="
echo "   Instalando kali-ai-assistant (Compatível com Kali)"
echo "===================================================="

# Verifica se é root
if [ "$EUID" -ne 0 ]; then
  echo "Erro: Por favor, execute como root (sudo ./install.sh)."
  exit 1
fi

# Instala dependências do sistema necessárias
echo "[*] Verificando dependências do sistema (python3-venv)..."
apt-get update -y -q > /dev/null
apt-get install -y -q python3-venv python3-pip > /dev/null

# Cria o diretório de instalação
echo "[*] Criando diretório de instalação em $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Cria o ambiente virtual
echo "[*] Criando ambiente virtual Python..."
python3 -m venv "$INSTALL_DIR/venv"

# Instala as dependências dentro do venv
echo "[*] Instalando dependências Python no ambiente isolado..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install openai google-generativeai google-auth-oauthlib -q

# Copia o script Python para o diretório de instalação
echo "[*] Copiando arquivos do projeto..."
cp kali-ai-assistant.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/kali-ai-assistant.py"

# Cria o script de wrapper em /usr/local/bin
echo "[*] Criando script de atalho em $BIN_PATH..."
cat <<EOF > "$BIN_PATH"
#!/bin/bash
# Wrapper para executar o kali-ai-assistant usando o ambiente virtual correto
source "$INSTALL_DIR/venv/bin/activate"
python3 "$INSTALL_DIR/kali-ai-assistant.py" "\$@"
EOF

chmod +x "$BIN_PATH"

echo ""
echo "===================================================="
echo "   Instalação concluída com sucesso!"
echo "===================================================="
echo ""
echo "A ferramenta foi instalada em um ambiente isolado para evitar conflitos."
echo "Agora você pode usar o comando globalmente:"
echo ""
echo "  kali-ai-assistant --setup"
echo ""
echo "Depois, basta digitar 'kali-ai-assistant' para iniciar o chat."
echo ""
