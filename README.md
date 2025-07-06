# Self-hosted Office Docs to Pdf Converter and Merger Api

Based on Fastapi, Libreoffice, pypdf

### Установка приложения

```
git clone https://github.com/kushedow/convert_api.git
cd convert_api
pip install -r requirements.txt --break-system-packages
sudo apt install libreoffice
```

### Обновление приложения

```
pkill -f uvicorn
git pull
pip install -r requirements.txt --break-system-packages
```

### Запуск приложения

```
cd convert_api
nohup uvicorn main:app --host 0.0.0.0 --port 10000 &
```

### Остановка приложения

```pkill -f uvicorn```
