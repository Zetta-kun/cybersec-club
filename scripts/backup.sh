#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="database/backups/$DATE"
mkdir -p $BACKUP_DIR
docker exec cybersec_db pg_dump -U cybersec_user cybersec_club > $BACKUP_DIR/database.sql
echo '✅ Backup yaradıldı'
