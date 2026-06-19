# kali-ai-assistant

Substituto open-source do Gemini CLI para o Kali Linux, com suporte a conversação, execução de comandos e histórico persistente.

---

## Instalação

### Passo 1 — Baixar os arquivos

Coloque os arquivos `kali-ai-assistant.py` e `install.sh` na mesma pasta e execute:

```bash
chmod +x install.sh
sudo ./install.sh
```

### Passo 2 — Configurar a API Key

```bash
kali-ai-assistant --setup
```

Você precisará de uma **API Key** de um provedor compatível com OpenAI. Opções recomendadas:

| Provedor | Modelos | Custo | Link |
|---|---|---|---|
| OpenAI | GPT-4o, GPT-4 | Pago | https://platform.openai.com |
| Groq | LLaMA 3, Mixtral | Gratuito (com limites) | https://console.groq.com |
| OpenRouter | Vários (incluindo gratuitos) | Gratuito/Pago | https://openrouter.ai |

---

## Uso

### Modo interativo (chat)

```bash
kali-ai-assistant
```

### Modo headless (prompt único)

```bash
kali-ai-assistant -p "Explique como usar o nmap para escanear uma rede"
```

### Limpar histórico

```bash
kali-ai-assistant --clear
```

---

## Comandos dentro do chat

| Comando | Descrição |
|---|---|
| `/clear` | Limpa o histórico da sessão atual |
| `/exit` | Sai do assistente |

---

## Execução de Comandos

Quando o assistente sugerir um comando, ele aparecerá destacado e você será perguntado se deseja executá-lo:

```
O assistente sugeriu executar o comando:
sudo apt update && sudo apt upgrade -y
Deseja executar este comando? (s/N):
```

---

## Configuração com Groq (gratuito)

1. Acesse https://console.groq.com e crie uma conta
2. Gere uma API Key
3. Execute `kali-ai-assistant --setup`
4. Cole sua API Key
5. Em **Base URL**, coloque: `https://api.groq.com/openai/v1`
6. Em **Modelo**, coloque: `llama3-70b-8192`

---

## Configuração com OpenRouter (modelos gratuitos)

1. Acesse https://openrouter.ai e crie uma conta
2. Gere uma API Key
3. Execute `kali-ai-assistant --setup`
4. Cole sua API Key
5. Em **Base URL**, coloque: `https://openrouter.ai/api/v1`
6. Em **Modelo**, coloque: `meta-llama/llama-3.1-8b-instruct:free`
