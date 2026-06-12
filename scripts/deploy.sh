#!/bin/bash
cd frontend && npm run build && cd ..
docker-compose up -d --build
echo '✅ Deploy tamamlandı!'
