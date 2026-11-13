# AGENTS.md

## Projeto

NAES/SorriSys e um sistema Django para gestao de prontuario odontologico, com modulos de pacientes, tratamentos e documentos.

## Regras obrigatorias

- Preserve o isolamento por usuario: registros devem ser filtrados por `request.user` em listagem, detalhe, alteracao e exclusao.
- Use a app `ia` como unica porta de entrada para provedores de inteligencia artificial. Chamadas devem passar por `chamar_ia`.
- Nunca envie segredos, senhas, tokens ou dados de pacientes para o provedor sem necessidade explicita.
- Valide entradas, use CSRF em requisicoes mutaveis e sanitize Markdown antes de renderizar HTML.
- Toda alteracao deve ter validacao executavel: teste Django, `manage.py check` ou verificacao equivalente.
- Nao ative `DEBUG` em producao.

## Convencoes

- Idioma da interface: portugues do Brasil.
- HTML usa Bootstrap existente e templates Django.
- Views genericas devem reutilizar os mixins de `website.mixins`.
- Commits seguem a skill `commit-message`.
