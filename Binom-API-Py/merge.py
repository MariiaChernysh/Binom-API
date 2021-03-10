import os
import glob
import pandas as pd

os.chdir("./csv/")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv(path_or_buf="../merged/flex.csv", index=False, encoding='utf-8')