# kali-ai-assistant (Zero Config) 🚀

O substituto definitivo para o Gemini CLI no Kali Linux. Sem chaves de API, sem Google Cloud, sem complicação. **Instale e use.**

---

## Instalação Rápida

Abra seu terminal no Kali e cole os comandos abaixo:

```bash
# 1. Clone o projeto
git clone https://github.com/dmmdmfmf755-dot/kali-ai-assistant.git
cd kali-ai-assistant

# 2. Instale (compatível com Kali moderno/PEP 668)
chmod +x install.sh
sudo ./install.sh
```

---

## Como Usar

Agora você pode chamar a IA de qualquer lugar do terminal:

```bash
kali-ai-assistant
```

### Exemplos de uso:
- `> Como atualizar todas as ferramentas do Kali?`
- `> Explique o comando nmap -sV`
- `> Crie um script em python para escanear portas`

---

## Comandos Úteis

| Comando | Descrição |
|---|---|
| `kali-ai-assistant` | Abre o chat interativo |
| `kali-ai-assistant -p "pergunta"` | Resposta rápida (modo comando) |
| `kali-ai-assistant --clear` | Limpa o histórico de conversas |
| `/exit` | Sai do chat |
| `/clear` | Limpa a conversa atual |

---

## Por que usar?
- **Zero Configuração**: Não precisa de API Key nem login Google.
- **Execução de Comandos**: A IA sugere comandos e você autoriza a execução na hora.
- **Isolado e Seguro**: Instalado em um ambiente virtual (`venv`) para não quebrar seu Python do sistema.
