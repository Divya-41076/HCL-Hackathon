import os
import shutil

base = "."

folders = {
    "backend/app/routes": ["auth.py", "accounts.py", "transactions.py", "requests.py", "insights.py"],
    "backend/app": ["models.py", "database.py"],
    "backend": ["main.py", "seed.py", "requirements.txt"],
    "frontend/pages": ["dashboard.py", "accounts.py", "transfer.py", "transactions.py", "requests.py", "insights.py"],
    "frontend/utils": ["api.py"],
    "frontend": ["app.py", "login.py"]
}

for folder, files in folders.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        if os.path.exists(file):
            shutil.move(file, os.path.join(folder, file))

print("✅ Files organized successfully!")