#!/bin/bash

ASSETS_DIR="/home/$HTC_USER/assets"

pip3 install -r ./assets/requirements.txt

bash ./assets/compile.sh

python3 api.py  --bin-dir "$ASSETS_DIR/binary" \
                --config "$ASSETS_DIR/config.json" \
                --log-file "$ASSETS_DIR/error.log" \
                --timezone "Asia/Kolkata" \
                --host "htcapp" \
                --port "$HTC_API_PORT" \
                --max-rate "$MAX_REQ_RATE"
