#!/bin/bash
echo '🚀 CyberSec Club Setup'
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements/dev.txt
cd frontend && npm install && cd ..
echo '✅ Setup tamamlandı!'
