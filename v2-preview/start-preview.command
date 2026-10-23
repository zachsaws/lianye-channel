#!/bin/zsh
cd "$(dirname "$0")"
print "联野 V2 本机预览：http://127.0.0.1:8818/"
print "完整交付材料：http://127.0.0.1:8818/review.html"
python3 -m http.server 8818 --bind 127.0.0.1
