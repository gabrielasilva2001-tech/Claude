#!/bin/bash
# aplica bokeh em todos os cortes já renderizados (render2/segs) -> render2/segs_bokeh
W=$1; S=$W/scripts/bokeh.py; I=$W/render2/segs; O=$W/render2/segs_bokeh; mkdir -p $O; : > $O/list.txt
for f in $I/s*.mkv; do b=$(basename $f); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)
  python3 -I $S $f 0 $d $O/$b 30 1.0 2>&1 | grep -E "^ok" | sed "s/^/$b /"
  echo "file '$O/$b'" >> $O/list.txt; done
echo FIM
