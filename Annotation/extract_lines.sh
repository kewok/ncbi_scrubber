# https://unix.stackexchange.com/a/47424/230574
X=940418
Y=940494
tail -n "+$X" My_Discrepency_Report.dr | head -n "$((Y-X+1))"

