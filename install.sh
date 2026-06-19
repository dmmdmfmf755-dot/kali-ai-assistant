#!/bin/bash

# Script de instalação do kali-ai-assistant
# Substituto do Gemini CLI para Kali Linux

echo "=========================================="
echo " Instalando o kali-ai-assistant"
echo "=========================================="

# Instala as dependências Python
echo "[*] Instalando dependências Python..."
pip3 install openai google-generativeai google-auth-oauthlib --break-system-packages 2>/dev/null || pip3 install openai google-generativeai google-auth-oauthlib || sudo pip3 install openai google-generativeai google-auth-oauthlib

# Copia o script para /usr/local/bin com o nome correto
echo "[*] Copiando executável para /usr/local/bin/kali-ai-assistant..."
sudo cp kali-ai-assistant.py /usr/local/bin/kali-ai-assistant
sudo chmod +x /usr/local/bin/kali-ai-assistant

echo ""
echo "=========================================="
echo " Instalação concluída com sucesso!"
echo "=========================================="
echo ""
echo "PRÓXIMO PASSO — Configure sua API Key ou Google OAuth:"
echo ""
echo "  kali-ai-assistant --setup"
echo ""
echo "Depois, use assim:"
echo ""
echo "  kali-ai-assistant                        # Chat interativo"
echo "  kali-ai-assistant -p \"Sua pergunta\"      # Prompt único"
echo "  kali-ai-assistant --clear                # Limpa histórico"
echo ""
echo "Provedores de API compatíveis (gratuitos ou pagos):"
echo "  - Google OAuth2 (para Gemini API oficial)"
echo "  - OpenAI:      https://platform.openai.com"
echo "  - Groq:        https://console.groq.com  (gratuito)"
echo "  - OpenRouter:  https://openrouter.ai     (tem modelos gratuitos)"
echo ""
