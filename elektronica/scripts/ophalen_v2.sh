#!/bin/sh
# Haalt de resultaten van matcher v2 op uit de tijdelijke opslag (sleutel in $DUMPKEY) naar raw/v2/.
# Een leeg antwoord (tijdelijke storing) overschrijft nooit een bestaand bestand.
cd "$(dirname "$0")/../raw" && mkdir -p v2 && cd v2
for n in $(curl -s "https://elektrovergelijk.netlify.app/api/dump?k=$DUMPKEY&list=1"); do
  case "$n" in cb_*|mm_*|amz_*|alt_*|az_*|mob_*|bcc_*|ep_*|ps_*|inf_*|cnu_*)
    for poging in 1 2 3; do
      curl -s "https://elektrovergelijk.netlify.app/api/dump?k=$DUMPKEY&n=$n" > "/tmp/_$n.json"
      [ -s "/tmp/_$n.json" ] && { mv "/tmp/_$n.json" "$n.json"; break; }
      sleep 2
    done;;
  esac
done
ls | wc -l
