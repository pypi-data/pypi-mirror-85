#!/usr/bin/env python

import sys
import os

import annot

INSTRUCTIONS="""To open the annot in a web browser:
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
  page = annot.load('path/to/.annot')
  page.add_dataframe(df)
  page.add_plot(matplotlib.pyplot.gca())
  page.add_markdown('# Results')
  page.add_html('<img src="http://abc.com/img.png">')

To continuously monitor for changes:
  > annot monitor
"""

def main(args=None):
    """Entry point for command line

    Keyword Arguments:

      args (list) - list of str in form of sys.argv
    """

    if not args:
        args = sys.argv
        this = os.path.basename(args.pop(0))

    has_annot_dir = os.path.exists(annot.DEFAULT_ANNOT_DIR)

    # init
    if args and args[0] == 'init':
        force = '-f' in args
        if has_annot_dir:
            if not force:
                return ('Already an .annot directory here. '
                        'Use -f to overwrite it.')
            print('Deleting existing .annot directory')
            shutil.rmtree(DEFAULT_ANNOT_DIR)
            annot.setup_page(demo=False)
            print('---\n')
            print(INSTRUCTIONS)
        return

    # if there isn't an .annot directory here, ask if it should be
    # created
    if not has_annot_dir:        
        if args:
            return ('No .annot directory here. '
                    'Run without arguments to create one.')
        
        # prompt user if they want to create an .annot instance
        yn = input('No .annot directory here. '
                   'Want to create one? [y]/n: ')
        if yn.lower() not in ('', 'y', 'yes'):
            return
        
        annot.setup_page(demo=True)
        print('---\n')
        print(INSTRUCTIONS)
        return

    # .annot/ here, but user didn't provide arguments, show
    # instructions and return
    if not args:
        print('I see an .annot directory here.\n')
        print(INSTRUCTIONS)
        return

    page=annot.Page(annot.DEFAULT_ANNOT_DIR)

    # open page
    if args[0] == 'open':
        page.open()
        return

    # render HTML
    if args[0] == 'render':
        print('(hint: add ''-o'' to open in web browser)')
        page.render()
        if '-o' in args:
            page.open()
        return

    if args[0] == 'monitor':
        page.monitor()
        return              

    if args[0] == 'add':
        print('(hints for add: --full (show 10 rows by default), --datatables')
        args.pop(0)
        kwargs={}
        if '--full' in args:
            kwargs['rows']=None
            args.remove('--full')
        if '--datatables' in args:
            args.remove('--datatables')
            kwargs['datatables']=True
        if not args:
            return 'Provide path to csv'

        csv_path = args.pop(0)
        if not os.path.exists(csv_path):
            return 'File does not exist: {}'.format(csv_path)

        page.add_csv(csv_path, **kwargs)
        return

    if args[0] in ['markdown', 'md']:
        args.pop(0)
        if not args:
            return 'Provide text arguments to add to index.md'
        md = " ".join(args)
        page.add_markdown(md)
        return

    return 'Unrecognized args: {}'.format(args)

if __name__=='__main__':
    sys.exit(main())
