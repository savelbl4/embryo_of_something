import psutil
from datetime import datetime
import platform
from app.utils.text import replace
from app.config import PUBLIC_IP

def get_server_stats():
    """Возвращает статистику сервера в виде строки"""
    try:
        # CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        # Память
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 ** 3), 2)
        memory_used = round(memory.used / (1024 ** 3), 2)
        memory_percent = memory.percent

        # Диск
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_used = round(disk.used / (1024 ** 3), 2)
        disk_percent = disk.percent

        # Загрузка системы
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time

        # Формируем сообщение
        message = f"📊 *{replace('Статистика сервера'.lower())}*\n\n"
        message += f"🖥️ *CPU*: {cpu_usage}% ({cpu_count} ядер)\n"
        message += f"💾 *Память*: {memory_used}GB / {memory_total}GB ({memory_percent}%)\n"
        message += f"💿 *Диск*: {disk_used}GB / {disk_total}GB ({disk_percent}%)\n"
        message += f"⏰ *Аптайм*: {str(uptime).split('.')[0]}\n"
        message += f"🖥️ *ОС*: {platform.system()} {platform.release()}\n"
        message += f"⏱️ *Время*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += f"💌 *IP*: {PUBLIC_IP}"

        return message

    except Exception as e:
        return f"❌ Ошибка получения статистики: {e}"
