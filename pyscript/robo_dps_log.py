# Registra TODAS as mudanças de DP do robô (a cada 3 s) num arquivo, para
# descobrir o que cada DP faz enquanto você usa o app/controle.
# Requer a integração pyscript e o localtuya_bildass. Roda ao carregar o
# pyscript e para sozinho no horário FIM. Grava em /config/robo_dps_log.txt
import datetime, json

ROBO = "SEU_DEVICE_ID"                              # device_id do robô no LocalTuya
FIM = datetime.datetime.now() + datetime.timedelta(hours=4)   # quanto tempo registrar
ARQ = "/config/robo_dps_log.txt"
IGNORAR = ("6",)                                    # DP 6 = bateria (muda o tempo todo)


@pyscript_compile
def _gravar(txt, modo):
    with open(ARQ, modo) as f:
        f.write(txt + "\n")


@time_trigger("startup")
def robo_dps_log():
    dev = hass.data["localtuya_bildass"]["tuya_devices"][ROBO]
    ultimo = dict(dev._status)
    task.executor(_gravar, datetime.datetime.now().strftime("%d %H:%M:%S") + " INICIAL " + json.dumps(ultimo), "w")
    while datetime.datetime.now() < FIM:
        task.sleep(3)
        dev = hass.data["localtuya_bildass"]["tuya_devices"][ROBO]   # pega de novo (o LocalTuya pode recarregar)
        atual = dict(dev._status)
        mud = {k: [ultimo.get(k), v] for k, v in atual.items() if ultimo.get(k) != v and k not in IGNORAR}
        if mud:
            task.executor(_gravar, datetime.datetime.now().strftime("%d %H:%M:%S") + " " + json.dumps(mud), "a")
        ultimo = atual
