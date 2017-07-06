#!/usr/bin/env bash
wget -O step-12768-submissions.csv.gz "https://drive.google.com/uc?export=download&id=0B6udzTbX1EFPYUptYmN1VTg2b2c"
find . -name 'step-12768-submissions.csv.gz' -exec gzip -d {} \;