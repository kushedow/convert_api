pkill -f uvicorn
git pull
nohup uvicorn main:app --host 0.0.0.0 --port 10000 &
