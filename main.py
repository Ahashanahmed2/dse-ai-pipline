# main.py

import sys
import subprocess

scripts = [
    "scripts/generate_features.py",
    "scripts/train_model.py",
    "scripts/predict_signal.py",
    "scripts/generate_signals.py",
    "scripts/backtest_signals.py",
    "reports/generate_pdf.py",
    "scripts/send_email.py"
]

for script in scripts:
    print(f"🚀 Running: {script}")
    try:
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}: {e}")
        break