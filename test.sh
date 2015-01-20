#!/bin/bash

y=0;
m=0;
e=0;
q=0;
DIR="$1/*"
for f in $DIR 
    do 
        z="$(python file.py ""$f"" 2>/dev/null | tail -1)"
        p="${#1}"
        s="$((p+5))"
        r="${f:s:1}"
        if [ "$z" == "S" ]; then
            ((q++));
            echo "$f : SAME"
            continue
        fi
        if [ "$r" == "$z" ]; then 
            ((y++));
            echo "$f : OK"
        elif [ "$r" != "$z" ]; then 
            ((n++));
            echo "$f : WRONG";
        else
            ((e++));
            echo "$f : ERR";
        fi
    done

echo -e "OK: \t$y ($(((100*y)/(y+n+q)))%)";
echo -e "WRONG: \t$n ($(((100*n)/(y+n+q)))%)";
echo -e "SAME: \t$q ($(((100*q)/(y+n+q)))%)"; 
echo -e "ERR: \t$e"; 
