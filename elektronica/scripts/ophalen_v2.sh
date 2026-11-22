#!/bin/sh
# Haalt de resultaten van matcher v2 op uit de tijdelijke opslag (sleutel in $DUMPKEY) naar raw/v2/.
cd "$(dirname "$0")/../raw" && mkdir -p v2 && cd v2
for n in $(curl -s "https://elektrovergelijk.netlify.app/api/dump?k=$DUMPKEY&list=1"); do
  case "$n" in cb_*|mm_*|amz_*|alt_*|az_*|bol_*|mob_*|bcc_*) curl -s "https://elektrovergelijk.netlify.app/api/dump?k=$DUMPKEY&n=$n" > "$n.json";; esac
done
ls -la | wc -l
