---
name: django-ai
description: "Use when implementing or reviewing the Django IA app, chamar_ia service, quotas, audit logs, assistant history, or AI configuration."
---

# Django IA

- A unica entrada para provedores e `ia.services.chamar_ia`.
- Leia configuracao ativa do banco e registre cada chamada, sucesso, erro e tokens.
- Aplique a cota mensal antes de chamar o provedor.
- Filtre historico por usuario e envie somente a janela de cinco mensagens.
- Nao exponha a chave da API em templates, logs ou respostas.
- Teste quota, isolamento e falha do provedor.
