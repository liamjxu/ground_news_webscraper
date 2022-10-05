#!/bin/bash
for i in {0..14}
do
   python main.py --rank $i &
done