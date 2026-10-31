# WAP W1000 no Home Assistant (100% local, sem nuvem)

Integração do **robô aspirador WAP W1000** com o Home Assistant pela rede local,
usando o [LocalTuya (fork localtuya_bildass)](https://github.com/bildass/localtuya).
Nada passa pela nuvem Tuya depois de configurado.

> 🇬🇧 *Local Home Assistant integration for the WAP W1000 robot vacuum (a Tuya-based
> robot sold in Brazil) via LocalTuya: full DP map, LocalTuya config, template
> sensors and automations. Docs in Portuguese; the DP table below is language-neutral.*

Tudo aqui foi descoberto e testado num W1000 real (comprado na Havan em out/2026),
registrando cada DP enquanto o robô limpava e comparando com o app Smart Life.

## O que tem neste repositório

| Pasta | O que é |
|---|---|
| [`localtuya/robo_w1000_localtuya.json`](localtuya/robo_w1000_localtuya.json) | Configuração das entidades no LocalTuya (DPs, opções e nomes) |
| [`packages/robo_aspirador.yaml`](packages/robo_aspirador.yaml) | Package do HA: ajudantes e sensores (tempo/área da última limpeza, "está com mop?") |
| [`automations/robo_w1000.yaml`](automations/robo_w1000.yaml) | Automações: limpeza diária, aviso de volta à base com motivo, erros, peças e robô perdido |
| [`pyscript/robo_dps_log.py`](pyscript/robo_dps_log.py) | Script para registrar todas as mudanças de DP (para descobrir DPs novos) |
| [`docs/exemplo_status.json`](docs/exemplo_status.json) | Exemplo real do status completo do robô |

## Mapa de DPs

| DP | Tipo | Valores | O que é | Entidade |
|---|---|---|---|---|
| 2 | bool | `true` / `false` | Liga/para a limpeza | vacuum (powergo) |
| 3 | enum | `smart`, `wall_follow`, `spiral`, `chargego` | Modo de limpeza / voltar à base | vacuum (modo) |
| 4 | enum | `forward`, … | Direção (controle manual) | — |
| 5 | enum | `standby`, `charging`, `charge_done`, `goto_charge`, `paused`, … | Estado do robô | vacuum (status) |
| 6 | int | 0–100 | Bateria (%) | sensor |
| 7 | int | 0–100 | Vida da escova lateral (%) | sensor |
| 8 | int | 0–100 | Vida da escova central (%) | sensor |
| 9 | int | 0–100 | Vida do filtro (%) | sensor |
| 10, 11, 12 | bool | | Provavelmente zerar contadores das peças *(não confirmado)* | — |
| 13 | bool | | Procurar robô (apito) | switch |
| 14 | enum | `low`, `middle`, `high` | Potência de aspiração (Silencioso / Normal / Forte) | select |
| 15 | string | ex.: `01200900015` | Registro da última limpeza (ver abaixo) | sensor |
| 16 | int | m² | Área limpa na limpeza atual | vacuum (clean_area) |
| 17 | int | min | Tempo da limpeza atual | vacuum (clean_time) |
| 18 | bitmap | | Código de falha (ver abaixo) | vacuum (fault) |
| 28 | int | 0–100 | Volume da voz | number |
| 101 | enum | `close`, `low`, `mid`, `high` | Água do mop (Sem água / Baixo / Médio / Alto) | select |
| 102 | int | | *(desconhecido, sempre 0)* | — |
| 103 | bool | | Mudo (sem voz) | switch |
| 104 | bool | | *(desconhecido)* | — |

### DP 15 — registro da última limpeza
Texto de 11 dígitos `TTTAAANNNNN`:
- `TTT` = minutos de limpeza
- `AAA` = área em m²
- `NNNNN` = número do registro

Ex.: `01200900015` → 12 min, 9 m², registro nº 15. Conferido com o histórico do app.
Os sensores `Robô última limpeza tempo` e `Robô última limpeza área` do package fazem essa separação.

### DP 18 — falhas (bits)
| Bit | Significado |
|---|---|
| 2 | Roda travada/presa |
| 4 | Sensor de queda (degrau) sujo ou bloqueado |
| 8 | Escova central enroscada |
| 16 | Escova lateral enroscada |
| 32 | Sem reservatório (água ou poeira) |
| 512 | Sensor/para-choque da frente travado |

Pode vir mais de um bit junto (ex.: `24` = escova central + lateral).

### Detectar se está com o mop
Sem o reservatório de água/mop o robô trava o DP 101 em `close` ("Sem água") e não
deixa mudar. O binary_sensor `Robô com mop` do package usa isso.

## Instalação

1. **Pegar o `device_id` e a `local_key`** do robô (por exemplo com o add-on
   *Tuya Local Key* ou o `tinytuya wizard`). Pareie o robô no app Smart Life antes.
2. **Fixar o IP** do robô no roteador (reserva de DHCP).
3. **Adicionar no LocalTuya (localtuya_bildass)**: protocolo **3.5**, marcar
   *forçar adicionar* e *pular teste de conexão* (o robô dorme na base e às vezes
   não responde). Criar as entidades como em
   [`localtuya/robo_w1000_localtuya.json`](localtuya/robo_w1000_localtuya.json).
   Os nomes das entidades no HA vão ficar como `vacuum.robo_w1000`,
   `sensor.robo_w1000_robo_bateria` etc. Se usar outros nomes, ajuste os arquivos.
4. **Package**: copiar `packages/robo_aspirador.yaml` para a pasta `packages/` do HA
   (com `homeassistant: packages: !include_dir_named packages` no `configuration.yaml`)
   e reiniciar.
5. **Automações**: colar o conteúdo de `automations/robo_w1000.yaml` no seu
   `automations.yaml` (ou criar pela interface) e trocar `notify.SEU_CELULAR` pelo
   seu serviço de notificação.

## Automações incluídas

- **Limpeza diária às 9h**, ou antes se a casa ficar vazia por 10 min (entre 8h e 19h).
  Aspiração *Forte* com a casa vazia, *Normal* com gente em casa. Uma vez por dia,
  só com o robô na base e bateria acima de 60%. Liga/desliga em
  `input_boolean.robo_limpeza_auto`.
- **Aviso de volta à base com o motivo**: erro, comando do HA, bateria baixa, comando
  do app/controle ou fim da limpeza, com tempo, área e bateria.
- **Aviso de erro** com a falha traduzida (DP 18).
- **Peças**: avisa às 10h se escova lateral, central ou filtro estiver abaixo de 10%.
- **Robô perdido**: parado/pausado fora da base por 30 min, ou "limpando" por mais de 2h30.

## Descobrindo DPs novos
O [`pyscript/robo_dps_log.py`](pyscript/robo_dps_log.py) (precisa da integração
[pyscript](https://github.com/custom-components/pyscript)) grava num arquivo cada DP
que muda, a cada 3 s. Mexa no app e veja o que mudou. Se descobrir o significado
dos DPs 4, 10–12, 102 ou 104, abra uma issue ou PR!

## Licença
MIT — use à vontade.
