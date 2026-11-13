---
name: security-review
description: "Use when reviewing authentication, authorization, CSRF, secrets, Markdown sanitization, audit logs, or external AI integrations in this project."
---

# Revisao de seguranca

Verifique sempre:

- autenticacao e ownership por usuario;
- CSRF em POST/AJAX;
- segredos vindos de ambiente ou armazenamento protegido;
- limites de cota e abuso por usuario;
- Markdown sanitizado com allowlist;
- logs sem prompts, respostas ou dados pessoais completos;
- respostas externas tratadas como nao confiaveis.
