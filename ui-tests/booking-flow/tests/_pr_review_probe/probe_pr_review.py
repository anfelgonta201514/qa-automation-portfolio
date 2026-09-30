# ARCHIVO DE PRUEBA TEMPORAL — nunca se mergea a master.
# Sirve para verificar que la routine de review automático de PRs se
# dispara y detecta violaciones reales del checklist de CLAUDE.md.
# No empieza con test_, así que pytest no lo recolecta.
import time


def probe_login_waits_with_sleep(page):
    page.locator("//div[@class='login']//input[1]").fill("admin")
    time.sleep(2)  # violación intencional: CLAUDE.md prohíbe time.sleep()
