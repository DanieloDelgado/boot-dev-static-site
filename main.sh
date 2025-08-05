#!/bin/bash
python3 src/gen_static_site/main.py
cd public && python3 -m http.server 8888
