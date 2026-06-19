# kali-ai-assistant

Substituto open-source do Gemini CLI para o Kali Linux, com suporte a conversação, execução de comandos e histórico persistente, além de autenticação Google OAuth2.

---

## Instalação (Compatível com Kali Linux / PEP 668)

A instalação agora utiliza um **Ambiente Virtual (venv)** isolado para cumprir as políticas de segurança do Kali Linux moderno, garantindo que as dependências não interfiram no sistema global.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/dmmdmfmf755-dot/kali-ai-assistant.git
cd kali-ai-assistant
```

### Passo 2 — Executar o script de instalação automática

O instalador criará um ambiente virtual em `/opt/kali-ai-assistant` e um atalho global em `/usr/local/bin/`.

```bash
chmod +x install.sh
sudo ./install.sh
```

### Passo 3 — Configurar a autenticação

```bash
kali-ai-assistant --setup
```

Você terá duas opções de autenticação:

1.  **API Key (OpenAI, Groq, OpenRouter, etc.)**: Para provedores compatíveis com a API da OpenAI. Você precisará de uma chave de API e, opcionalmente, uma Base URL e o nome do modelo.
2.  **Google OAuth2 (para Gemini API oficial)**: Para usar sua conta Google diretamente com a API Gemini. Você precisará baixar um arquivo `client_secret.json` do seu projeto Google Cloud (tipo 'Desktop app') e colocá-lo na pasta `~/.kali-ai-assistant/`. Na primeira execução, um navegador será aberto para você autorizar o acesso.

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

## Configuração de Provedores de API

### Google OAuth2 (para Gemini API oficial)

1.  Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2.  Habilite a **Google Generative Language API**.
3.  Configure a tela de consentimento OAuth e adicione-se como usuário de teste.
4.  Crie credenciais de **ID do cliente OAuth** do tipo **Aplicativo de desktop**.
5.  Baixe o arquivo `client_secret.json` e coloque-o na pasta `~/.kali-ai-assistant/`.
6.  Execute `kali-ai-assistant --setup` e escolha a opção `2` (Google OAuth2).
7.  Na primeira execução do `kali-ai-assistant`, um navegador será aberto para você autorizar o acesso com sua conta Google.

### Outros Provedores (via API Key)

| Provedor | Custo | Base URL (exemplo) | Modelo (exemplo) |
|---|---|---|---|
| **OpenAI** | Pago | `https://api.openai.com/v1` (padrão) | `gpt-4o` |
| **Groq** | Gratuito (com limites) | `https://api.groq.com/openai/v1` | `llama3-70b-8192` |
| **OpenRouter** | Vários (incluindo gratuitos) | `https://openrouter.ai/api/v1` | `meta-llama/llama-3.1-8b-instruct:free` |

Para configurar, execute `kali-ai-assistant --setup`, escolha a opção `1` (API Key) e forneça as informações solicitadas. O modelo padrão será `gpt-4.1-mini` se não for especificado.
