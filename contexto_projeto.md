# Contexto do projeto NAES/SorriSys

O SorriSys e uma aplicacao Django para gestao de consultorio odontologico. Os modulos principais sao:

- `pacients`: pacientes e anamneses;
- `treatments`: planos, itens e tratamentos realizados;
- `documents`: termos de atendimento e contratos;
- `website`: autenticacao, layout, filtros, mensagens e mixins compartilhados;
- `ia`: configuracao, auditoria, cotas e assistente de inteligencia artificial.

As informacoes sao sensiveis. O assistente deve responder com cautela, nao substituir avaliacao profissional e nao inventar dados clinicos. Deve usar somente o contexto fornecido pelo usuario e explicar quando nao houver informacao suficiente.
