# Como contribuir

Toda ajuda é bem-vinda, principalmente para **descobrir os DPs que ainda faltam**
(4, 10, 11, 12, 102 e 104) e para confirmar se outros modelos parecidos funcionam igual.

## Descobriu o que um DP faz?
1. Rode o [`pyscript/robo_dps_log.py`](pyscript/robo_dps_log.py) (troque o `ROBO`
   pelo device_id do seu robô).
2. Mexa na função pelo app Smart Life ou pelo controle e anote o horário.
3. Abra uma issue **"Novo DP descoberto"** com o trecho do log e o que você fez.

## Funciona no seu robô (outro modelo/versão)?
Abra uma issue contando o modelo, a versão do firmware (no app) e o que funcionou
ou não. Isso ajuda a manter a lista de compatibilidade.

## Mudanças nos arquivos (pull request)
1. Faça um fork e crie um branch.
2. Mantenha os arquivos no mesmo formato (YAML do Home Assistant, nomes de entidade
   `robo_w1000_*`).
3. **Nunca inclua** sua `local_key`, device_id, IP ou nomes de pessoas. Use os
   marcadores `SEU_DEVICE_ID`, `SEU_IP`, `SUA_LOCAL_KEY`, `notify.SEU_CELULAR`.
4. Teste no seu Home Assistant antes de mandar.
5. Abra o PR explicando o que mudou e por quê.

Pode escrever em português ou inglês.
