"""
Filename: vdannot.py
Version: 0.0.0
Last updated: 2020-08-28
Home: 
Author: Mike Claffey

# Usage

Save sheets into an annot.py HTML report

## Commands

- `annot-save` saves the sheet to an .annot directory

"""

__version__ = "0.0.0"

import os

import visidata

import annot

@visidata.asyncthread
def _save_table(sheet, path):
    """This is the asynchronous, final step once the user has
    confirmed the command. It is passed a visidata Sheet and Path
    instance.

    Argument:
        sheet (visidata.Sheet)
        path (str): the path to save csv, already within .annot/data
            folder in current directory.
    """
    visidata.status(f"saving to {path}")

    # get data from visidata: a list of rows, each row a list of
    # values, starting with a heading
    headers = [ col.name for col in sheet.visibleCols ]
    def get_row_values(row):
        return [ col.getDisplayValue(row) for col in sheet.visibleCols ]
    data = map(get_row_values, visidata.Progress(sheet.rows))
    
    # write the csv
    with open(path, 'w') as f:
        for row in data:
            f.write(",".join(row) + '\n')

    # add csv to page
    page = annot.get_default_page()
    page.add_csv(path)
    page.open()

    visidata.status("saved")


def annot_csv(sheet, givenpath, confirm_overwrite = True):
    """This is the non-asynchronous command that is called directly by
    visidata when the user enteres the command. It takes a visidata
    Sheet and Path instance, confirms with user is necessary, and then
    passes to the asynchronous _save table.
    """
    # adjust path to be inside .annot/data
    csv_name = os.path.basename(str(givenpath))
    if not csv_name.endswith('.csv'):
        csv_name += '.csv'
    csv_path = os.path.join('.annot', 'data', csv_name)

    if os.path.exists(csv_path):
        if confirm_overwrite:
            visidata.confirm(f"{csv_path} already exists. overwrite? ")

    _save_table(sheet, csv_path)

def annot_markdown(sheet, markdown):
    annot.get_default_page().add_markdown(markdown)

visidata.Sheet.annot_csv = annot_csv
visidata.Sheet.annot_markdown = annot_markdown

visidata.Sheet.addCommand(None, "annot-csv", "vd.sheet.annot_csv(inputFilename('save to: ', value = (sheet.name.strip('.'))), confirm_overwrite = options.confirm_overwrite)")

visidata.Sheet.addCommand(None, "annot-markdown", "vd.sheet.annot_markdown(input('Markdown: '))")

visidata.addGlobals({
    "annot_csv": annot_csv,
    "annot_markdown": annot_markdown
})
