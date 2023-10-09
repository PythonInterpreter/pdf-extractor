import pdfplumber
import csv
import sys
import os

def is_mostly_empty(table, threshold=0.8):
    total_cells = len(table) * len(table[0])
    empty_cells = sum(cell is None or cell == "" for row in table for cell in row)
    empty_ratio = empty_cells / total_cells
    return empty_ratio >= threshold

def extract_text_and_tables_to_md(pdf_path):
    output_md_file = "output.md"  # Fixed output file name

    output_path = "output.md"

    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"File '{output_path}' has been removed.")
    else:
        print(f"File '{output_path}' does not exist.")

    with pdfplumber.open(pdf_path) as pdf:
        with open(output_md_file, 'w', encoding='utf-8') as md:
            for page_num, page in enumerate(pdf.pages, start=1):
                md.write(f'## Page {page_num}\n\n')
                md.write(page.extract_text())
                md.write('\n\n')

                tables = page.extract_tables()
                print(tables)
                # print("tables is found")
                if tables:
                    md.write('### Tables\n\n')
                    for table_num, table in enumerate(tables, start=0):
                        if is_mostly_empty(table) or len(table) < 2:
                            continue
                        md.write(f'#### Table {table_num}\n\n')
                        for row in table:
                            if row:
                                md.write('|'.join(str(cell) for cell in row) + '\n')
                        md.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_pdf_to_md.py <input_pdf_file>")
    else:
        input_pdf_file = sys.argv[1]
        extract_text_and_tables_to_md(input_pdf_file)