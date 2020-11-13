#!/bin/bash
for grm in ./DataForFLCourse/*/grammars/*
do
    sed -i "s/ | eps/?/g" $grm
    sed -i "s/eps//g" $grm
done
