import camelot
import csv
import sys

def is_mostly_empty(table, threshold=0.8):
    total_cells = len(table.df) * len(table.df.columns)
    empty_cells = table.df.isna().sum().sum()
    empty_ratio = empty_cells / total_cells
    return empty_ratio >= threshold

def extract_text_and_tables_to_md(pdf_path):
    output_md_file = "output.md"  # Fixed output file name
    tables = camelot.read_pdf(pdf_path, flavor='stream')

    with open(output_md_file, 'w', encoding='utf-8') as md:
        for table_num, table in enumerate(tables, start=1):
            if is_mostly_empty(table):
                continue
            md.write(f'### Table {table_num}\n\n')
            md.write(table.df.to_markdown(index=False))
            md.write('\n\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_pdf_to_md.py <input_pdf_file>")
    else:
        input_pdf_file = sys.argv[1]
        extract_text_and_tables_to_md(input_pdf_file)