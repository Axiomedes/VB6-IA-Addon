import time



r_health = httpx.get("http://127.0.0.1:8765/api/v1/health", timeout=3.0)



r_start = httpx.post("http://127.0.0.1:8765/api/v1/chat/start", json={

    "provider": "ollama",

}, timeout=5.0)

job_id = r_start.json().get("job_id")

# Poll for results

    time.sleep(1.0)

    data = r_job.json()

    text = data.get("text", "")

    if data.get("is_completed"):

        print(text)

