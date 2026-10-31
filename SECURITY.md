# Segurança

Este repositório só tem configurações e automações do Home Assistant; ele não
roda nenhum serviço na internet. Mesmo assim, alguns cuidados:

- **Nunca publique a `local_key` do seu robô** (nem em issues, prints ou logs).
  Com ela, qualquer pessoa na sua rede consegue controlar o aparelho. Se você
  publicou sem querer, remova o robô do app Smart Life e pareie de novo para
  gerar uma chave nova.
- Também não publique device_id, IP, nome da sua rede Wi-Fi ou dados da sua conta Tuya.

## Encontrou um problema de segurança?
Se encontrar algo que exponha dados ou permita controlar o robô de fora da rede
local, **não abra uma issue pública**. Use o
[relato privado de vulnerabilidade do GitHub](https://github.com/brunogalvaoquick/wap-w1000-home-assistant/security/advisories/new)
deste repositório. A resposta é feita assim que possível (projeto mantido por hobby).
