]# annot

Annotate data analysis

## Command line usage

Start in a directory with some data:

  > ls
  faa-wildlife.csv

To create an annot project:

  > annot
  No .annot directory here. Want to create one? [y]/n: y
  Created .annot
  Created .annot/index.rst
  Created .annot/index.html
  Created .annot/DataTables/
  Created .annot/data
  Created .annot/temp

To open the annot in a web browser:

  > annot open

To add a datasets to the page:

  > annot add my.csv

To add comments to the page:

  > annot markdown '# Background'
  > annot markdown 'This csv has my data'
  -or-
  # edit .annot/index.rst in a text editor, then
  > annot render

To add content to the page from Jupyter:

  import annot
  page = annot.Page('path/to/.annot')
  page.add_dataframe(df)
  page.add_plot(matplotlib.pyplot.gca())
  page.add_markdown('# Results')
  page.add_html('<img src="http://abc.com/img.png">')

## Use from Visidata

To save visidata sheets directly to page:

  Using vdannot:

    Setup:
      PYTHONPATH=dir/with/annot.py
      export PYTHONPATH
      ~/.visidata/vdannot.py # exists
      ~/.visidatarc contains 'import vdannot'

    When you have a sheet to save:
      SPACE annot-csv ENTER my_freq_table ENTER

  Without using vdannot:

    Start this long-running process:
    > annot monitor

    In a different shell, open visidata. When you create a new sheet you
    want to save, such as after creating a frequency table, save the
    sheet as csv in the .annot/data directory
     - Ctrl-S
     - Path: .annot/data/my_freq_table.csv

To add a markdown comment:

  SPACE annot-markdown ENTER This is interesting data ENTER
  