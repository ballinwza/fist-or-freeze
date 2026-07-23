# --- Stage 1: Build dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# บิวด์ wheel ออกมาเก็บไว้ในโฟลเดอร์
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# --- Stage 2: Final Runtime ---
FROM python:3.11-slim

WORKDIR /app

# เอาเฉพาะ wheel ที่บิวด์เสร็จแล้วมาจากสเตจแรก มาติดตั้งแบบไม่ต้องคอมไพล์ใหม่
COPY --from=builder /app/wheels /workspace/wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /workspace/wheels/*

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000", "--workers", "1"]