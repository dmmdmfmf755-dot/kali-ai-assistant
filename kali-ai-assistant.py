#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
import readline
import argparse
from pathlib import Path

# Importações para OpenAI-compatible APIs
try:
    from openai import OpenAI
except ImportError:
    print("Erro: A biblioteca 'openai' não está instalada.")
    print("Instale com: pip3 install openai")
    sys.exit(1)

# Importações para Google OAuth2 e Gemini API
try:
    import google.generativeai as genai
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    # Não é um erro fatal, pois o usuário pode não querer usar Google OAuth
    genai = None
    Credentials = None
    InstalledAppFlow = None
    Request = None

CONFIG_DIR = Path.home() / ".kali-ai-assistant"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
TOKEN_FILE = CONFIG_DIR / "token.json" # Para Google OAuth
CLIENT_SECRET_FILE = CONFIG_DIR / "client_secret.json" # Para Google OAuth

DEFAULT_MODEL = "gpt-4.1-mini" # Modelo padrão para OpenAI-compatible
DEFAULT_GEMINI_MODEL = "gemini-pro" # Modelo padrão para Google Gemini API

DEFAULT_SYSTEM_PROMPT = """Você é o kali-ai-assistant, um assistente de IA projetado para rodar no terminal do Kali Linux.
Seu objetivo é ajudar o usuário com tarefas de terminal, pentest, administração de sistemas, programação e uso geral.
Você é um substituto direto do descontinuado Gemini CLI.

Quando o usuário pedir para executar um comando no terminal, você DEVE usar a seguinte sintaxe exata:
[COMMAND: comando_a_ser_executado]

Exemplo:
[COMMAND: ls -la]

Se você sugerir um comando, o script wrapper perguntará ao usuário se ele deseja executá-lo.
Sempre seja direto, técnico e útil."""

SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

def load_config():
    if not CONFIG_FILE.exists():
        return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def clear_history():
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    print("Histórico limpo com sucesso.")

def get_google_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                print(f"Erro: {CLIENT_SECRET_FILE} não encontrado.")
                print("Por favor, baixe o 'client_secret.json' do seu projeto Google Cloud e coloque-o em {CONFIG_DIR}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token: # Salva as credenciais para reuso
            token.write(creds.to_json())
    return creds

def setup():
    print("=== Configuração do kali-ai-assistant ===")
    print("Escolha o método de autenticação:")
    print("1. API Key (OpenAI, Groq, OpenRouter, etc.)")
    print("2. Google OAuth2 (para Gemini API oficial)")
    auth_choice = input("Digite 1 ou 2: ").strip()

    config = load_config()

    if auth_choice == '2':
        if not genai or not InstalledAppFlow:
            print("Erro: Bibliotecas 'google-generativeai' e 'google-auth-oauthlib' não instaladas.")
            print("Instale com: pip3 install google-generativeai google-auth-oauthlib")
            sys.exit(1)
        config["auth_method"] = "google_oauth"
        print("\nPara Google OAuth2, você precisará de um arquivo 'client_secret.json'.")
        print(f"Por favor, baixe-o do seu projeto Google Cloud (tipo 'Desktop app') e coloque-o em {CONFIG_DIR}/")
        print("Após isso, execute o assistente para iniciar o fluxo de autenticação no navegador.")
        # As credenciais serão geradas na primeira execução
    else:
        config["auth_method"] = "api_key"
        api_key = input("Digite sua API Key (OpenAI, Groq, OpenRouter, etc.): ").strip()
        api_base = input("Digite a Base URL (deixe em branco para o padrão da OpenAI): ").strip()
        model = input(f"Digite o modelo a usar (padrão: {DEFAULT_MODEL}): ").strip()

        if api_key:
            config["api_key"] = api_key
        if api_base:
            config["api_base"] = api_base
        if model:
            config["model"] = model
        elif "model" not in config:
            config["model"] = DEFAULT_MODEL

    save_config(config)
    print(f"\nConfiguração salva em {CONFIG_FILE}")
    print("Agora execute 'kali-ai-assistant' para iniciar o chat.")

def get_client(config):
    auth_method = config.get("auth_method", "api_key")

    if auth_method == "google_oauth":
        if not genai:
            print("Erro: Bibliotecas do Google Generative AI não instaladas para Google OAuth.")
            sys.exit(1)
        creds = get_google_credentials()
        genai.configure(credentials=creds)
        return genai # Retorna o módulo genai para usar suas funções
    else:
        api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Erro: API Key não configurada.")
            print("Execute 'kali-ai-assistant --setup' para configurar ou defina a variável OPENAI_API_KEY.")
            sys.exit(1)

        api_base = config.get("api_base") or os.environ.get("OPENAI_API_BASE") or None

        client_args = {"api_key": api_key}
        if api_base:
            client_args["base_url"] = api_base

        return OpenAI(**client_args)

def extract_and_run_commands(text):
    """Processa o texto da resposta, exibe e oferece execução de comandos sugeridos."""
    pattern = r"\[COMMAND:\s*(.*?)\]"
    matches = list(re.finditer(pattern, text))

    clean_text = text
    commands_to_run = []

    for match in matches:
        cmd = match.group(1).strip()
        commands_to_run.append(cmd)
        clean_text = clean_text.replace(match.group(0), f"\n\033[93m[Comando sugerido: {cmd}]\033[0m\n")

    print(clean_text)

    for cmd in commands_to_run:
        print(f"\n\033[93mComando sugerido:\033[0m {cmd}")
        choice = input("Deseja executar este comando? (s/N): ").strip().lower()
        if choice in ("s", "y", "sim", "yes"):
            print(f"\033[90mExecutando: {cmd}\033[0m")
            try:
                subprocess.run(cmd, shell=True)
            except Exception as e:
                print(f"Erro ao executar o comando: {e}")

def chat_session(config):
    client_or_genai_module = get_client(config)
    auth_method = config.get("auth_method", "api_key")

    if auth_method == "google_oauth":
        model_name = config.get("model", DEFAULT_GEMINI_MODEL)
        model = client_or_genai_module.GenerativeModel(model_name)
    else:
        model = config.get("model", DEFAULT_MODEL)

    history = load_history()
    if not history:
        history = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}]

    print(f"\033[95m=== kali-ai-assistant iniciado (Modelo: {model_name if auth_method == 'google_oauth' else model}) ===\033[0m")
    print("Digite sua mensagem. Comandos especiais:")
    print("  /clear  - Limpa o histórico da conversa")
    print("  /exit   - Sai do assistente")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n\033[92mVocê:\033[0m ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                print("Até logo!")
                break
            elif user_input.lower() == "/clear":
                history = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}]
                save_history(history)
                print("Histórico da sessão limpo.")
                continue

            # Adaptação do histórico para o formato do Google Generative AI se for Google OAuth
            messages_for_api = []
            if auth_method == "google_oauth":
                # O SDK do Google Generative AI espera um formato ligeiramente diferente para o histórico
                # e não aceita 'system' role diretamente no chat. O prompt do sistema é passado na inicialização do modelo.
                # Para simplificar, vamos passar o system prompt como a primeira mensagem do usuário para o modelo.
                # Isso pode ser refinado para usar o 'start_chat' com 'history' pré-definido se necessário.
                # Por enquanto, para manter a compatibilidade com o histórico existente, vamos adaptar.
                # Se o primeiro item for o system prompt, ele é ignorado aqui e o conteúdo é pré-pendido ao primeiro user_input.
                initial_content = ""
                if history and history[0]["role"] == "system":
                    initial_content = history[0]["content"] + "\n\n"
                    temp_history = history[1:]
                else:
                    temp_history = history

                for msg in temp_history:
                    if msg["role"] == "user":
                        messages_for_api.append({"role": "user", "parts": [msg["content"]]})
                    elif msg["role"] == "assistant":
                        messages_for_api.append({"role": "model", "parts": [msg["content"]]})
                messages_for_api.append({"role": "user", "parts": [initial_content + user_input]})
            else:
                messages_for_api = history + [{"role": "user", "content": user_input}]

            print("\n\033[96mAssistente:\033[0m ", end="", flush=True)

            if auth_method == "google_oauth":
                # Para Google Generative AI, o histórico é gerenciado pelo chat.send_message
                # e o modelo é instanciado com o system_instruction
                chat = model.start_chat(history=[]) # Inicia um novo chat para cada turno para evitar complexidade com histórico
                response = chat.send_message(messages_for_api[-1]["parts"][0]) # Envia apenas a última mensagem do usuário
                reply = response.text
            else:
                response = client_or_genai_module.chat.completions.create(
                    model=model,
                    messages=messages_for_api,
                    stream=False
                )

                if not response.choices:
                    error_msg = getattr(response, "error", "Resposta vazia da API")
                    print(f"\nErro da API: {error_msg}")
                    history.pop()
                    continue
                reply = response.choices[0].message.content

            extract_and_run_commands(reply)

            history.append({"role": "user", "content": user_input}) # Adiciona o user_input ao histórico para salvar
            history.append({"role": "assistant", "content": reply})
            save_history(history)

        except KeyboardInterrupt:
            print("\nUse /exit para sair.")
        except EOFError:
            break
        except Exception as e:
            print(f"\nErro de comunicação com a API: {e}")

def single_prompt(config, prompt):
    """Executa um prompt único sem entrar no modo interativo (modo headless)."""
    client_or_genai_module = get_client(config)
    auth_method = config.get("auth_method", "api_key")

    if auth_method == "google_oauth":
        model_name = config.get("model", DEFAULT_GEMINI_MODEL)
        model = client_or_genai_module.GenerativeModel(model_name, system_instruction=DEFAULT_SYSTEM_PROMPT)
        messages = [{"role": "user", "parts": [prompt]}]
    else:
        model = config.get("model", DEFAULT_MODEL)
        messages = [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

    try:
        if auth_method == "google_oauth":
            response = model.generate_content(messages)
            reply = response.text
        else:
            response = client_or_genai_module.chat.completions.create(
                model=model,
                messages=messages,
                stream=False
            )
            if not response.choices:
                error_msg = getattr(response, "error", "Resposta vazia da API")
                print(f"Erro da API: {error_msg}")
                return
            reply = response.choices[0].message.content

        extract_and_run_commands(reply)
    except Exception as e:
        print(f"Erro de comunicação com a API: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="kali-ai-assistant - Substituto do Gemini CLI para Kali Linux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  kali-ai-assistant                          # Inicia o chat interativo
  kali-ai-assistant -p "Como usar o nmap?"  # Prompt único
  kali-ai-assistant --setup                  # Configura API Key e modelo
  kali-ai-assistant --clear                  # Limpa o histórico
        """
    )
    parser.add_argument("-p", "--prompt", type=str, help="Executa um prompt único sem entrar no modo interativo")
    parser.add_argument("--setup", action="store_true", help="Configura a API Key e o modelo")
    parser.add_argument("--clear", action="store_true", help="Limpa o histórico de conversas")

    args = parser.parse_args()

    if args.setup:
        setup()
        return

    if args.clear:
        clear_history()
        return

    config = load_config()

    if args.prompt:
        single_prompt(config, args.prompt)
    else:
        chat_session(config)


if __name__ == "__main__":
    main()
