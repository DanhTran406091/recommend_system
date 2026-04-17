# CourseAI — Hệ thống Gợi ý Khóa học

## Chạy local

```bash
pip install fastapi uvicorn
python app.py
```

Mở trình duyệt: http://localhost:8000
Swagger UI:     http://localhost:8000/docs
ReDoc:          http://localhost:8000/redoc

---

## Deploy lên Render (miễn phí)

1. Push code lên GitHub (chỉ cần `app.py` + `requirements.txt`)
2. Vào https://render.com → New → Web Service
3. Kết nối repo GitHub
4. Điền cấu hình:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Click Deploy → đợi ~2 phút → nhận link public

---

## Deploy lên Railway

```bash
# Cài Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

---

## Cấu trúc file

```
app.py              ← Toàn bộ backend + frontend (1 file duy nhất)
requirements.txt    ← Dependencies
```

## API Endpoints

| Method | Path        | Mô tả                        |
|--------|-------------|------------------------------|
| GET    | /           | Giao diện web                |
| GET    | /docs       | Swagger UI (test API)        |
| GET    | /redoc      | ReDoc documentation          |
| GET    | /skills     | Danh sách kỹ năng            |
| GET    | /goals      | Danh sách mục tiêu nghề      |
| POST   | /recommend  | Gợi ý khóa học               |

## Ví dụ gọi API

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Frontend Developer",
    "skills": ["html", "css"],
    "level": 1,
    "available_time": 20
  }'
```
