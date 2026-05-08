import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

target_date = datetime(2026, 6, 6, 0, 0, 0)
now = datetime.now()

delta = target_date - now
server_time = now.strftime("%d.%m.%Y %H:%M:%S")

if delta.total_seconds() > 0:
    total_seconds = int(delta.total_seconds())

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    countdown_text = f"{days} дн. {hours} ч. {minutes} мин. {seconds} сек."
else:
    countdown_text = "Дата 6 июня уже наступила."

html = f"""
<div class="server-info-card">
    <div class="server-info-header">
        <span class="server-dot"></span>
        <span>CGI / Server generated block</span>
    </div>

    <div class="server-info-grid">
        <div class="server-info-item">
            <p class="server-info-label">Серверное время</p>
            <p class="server-info-value">{server_time}</p>
        </div>

        <div class="server-info-item">
            <p class="server-info-label">Расчёт на сервере</p>
            <p class="server-info-value">{countdown_text}</p>
        </div>
    </div>

    <p class="server-info-note">
        Этот блок сгенерирован Python CGI-скриптом на стороне сервера.
    </p>
</div>
"""

print(html)