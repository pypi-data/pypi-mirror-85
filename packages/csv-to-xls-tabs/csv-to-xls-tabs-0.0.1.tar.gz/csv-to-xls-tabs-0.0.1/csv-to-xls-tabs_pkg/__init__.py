import os, sys, glob, argparse, random
import pandas as pd

parser = argparse.ArgumentParser(description='Merge CSV files into XLSX Spreadsheet with multiple tabs')
parser.add_argument("path", help='Path to directory containing the CSV files')
parser.add_argument("-n", "--nrows", help='Number of rows to fetch from each file (default: 5000)', default=5000, type=int)
parser.add_argument("-o", "--output", help='Path for the creation of output XLSX file (default: same as input folder)')

args = parser.parse_args()

PATH = args.path
NROWS = args.nrows or 5000
OUTPUT = args.output or os.path.join(PATH, 'mergedCSVs.xlsx')

all_files = glob.glob(os.path.join(PATH, "*.csv"))

print('Fetching {} lines from \n-> {} \n Merged output file: {}'.format(NROWS, '\n-> '.join(all_files), OUTPUT))

writer = pd.ExcelWriter(OUTPUT, engine='xlsxwriter')

for f in all_files:
    df = pd.read_csv(f, nrows=NROWS)
    df.to_excel(writer, sheet_name=os.path.splitext(os.path.basename(f))[0], index=False)

writer.save()