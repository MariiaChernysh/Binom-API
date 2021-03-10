cd C:\Users\...\BI2 - CRs
python run_cr.py && python merge.py
gsutil -m cp -r "C:/Users/.../data.csv" gs://bucket/data.csv
PAUSE