# Используем официальный образ Python
FROM python:3.13-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY app .

# Штука для ssh
RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

# Запускаем бота
#CMD ["python", "-m", "app.main"]
CMD ["watch", "ls"]
