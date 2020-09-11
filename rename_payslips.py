import PyPDF2
import re
import datetime
import os
import glob
import fnmatch

def open_pdf(file_path):
    pdfFileObj = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj,strict=False)

    pages = pdfReader.numPages
    print(f"{pages=}")
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()
    return text

def get_date(text):
    match = re.search(r'Date\s?(\d{2})\/(\d{2})\/(\d{4})', text)
    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)

    else:
        raise ValueError("Date not found in text")
        print(f"{text=}")
    return datetime.datetime(int(year), int(month), int(day))

def is_bonus(text):
    match = re.search(r'Bonus', text)
    if match:
        return True
    else:
        return False


def fix_file(input_filepath):
    print(f"{input_filepath=}")


    text = open_pdf(input_filepath)
    print(f"{text=}")

    payslip_date = get_date(text).strftime("%Y%m%d")
    bonus_text = ""
    if is_bonus(text):
        bonus_text = " - bonus"

    output_filepath = "data/Payslip - {}{}.pdf".format(payslip_date, bonus_text)
    print("Input file path: {}".format(input_filepath))
    print("Output file path: {}".format(output_filepath))


    if input_filepath != output_filepath:
        print("Renaming file")
        os.rename(input_filepath, output_filepath)

def main():
    input_files = glob.glob("data/*.pdf")
    input_files.extend(glob.glob("data/*.PDF"))
    print(input_files)

    for filepath in input_files:
        fix_file(filepath)
if __name__ == "__main__":
    main()
