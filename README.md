# Multiagent Lab

Protótipo de orquestração de agentes com supervisor e acesso a arquivos limitado a um workspace. Não é uma plataforma de agentes pronta para produção.

## Executar sem custo de API

Python 3.11+. Execute `python main.py` e escolha **fake** quando o modo for solicitado. Escreva uma tarefa pequena. O modo fake não chama modelos externos.

Ollama é opcional. O provedor OpenAI é opcional e pode consumir créditos quando configurado e escolhido; a publicação não executa esse modo. Credenciais ficam em variáveis de ambiente, nunca no código.

## Limites

Faltam testes de integração de provedores, cancelamento, orçamento e revisão da política de escrita para uso com dados reais. O workspace contém somente arquivos de demonstração criados pelo usuário após executar.

## English

An experimental multi-agent supervisor with file access scoped to a workspace. Start with `python main.py` and select `fake` for a no-API demo. Real providers are optional; this prototype is not production-ready.
