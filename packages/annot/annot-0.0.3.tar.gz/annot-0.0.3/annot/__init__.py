import os
import sys
import argparse
import webbrowser
import time
import shutil
import io
import base64
import collections
import pickle
import shutil

import markdown
import csvtomd

from . import annot_lex

DEFAULT_ANNOT_DIR='annot'

class AnnotException(Exception):
    """TODO Only used by add_dataframe when overwrite is False and pickle
    already exists, not sure this is needed
    """
    pass

def get_default_page():
    """For now, in current directory. Could use something like a user
    setting in ~/.annot to persist a default location across python
    environments. 
    """
    # create annot if not here
    if not os.path.exists(DEFAULT_ANNOT_DIR):
        setup_page()
    return Page()


class AbstractAnnotClass(object):
    """Abstract class that provides the add_xxx() methods
    """

    _render_on=True
    """When False, changes won't be rendered by the .save()
    command. This is used when there are multiple additions
    being made at once, to avoid needlessly rendering each one before
    the final change is added.
    """

    def __init__(self, parent):
        self.parent=parent
        if hasattr(parent, 'dir'):
            self.dir=parent.dir
        else:
            self.dir=None        

    def render_on(self, render_now=True):
        self._render_on=True
        if self.parent:
            self.parent.render_on(render_now=False)
        if render_now:
            self.render()
        return self

    def render_off(self):
        self._render_on=False
        if self.parent:
            self.parent.render_off()
        return self

    def _write(self, s):
        """Save str s to content. This is an abstract method to be implemented
        by subclasses.

        """
        raise NotImplementedError('Must be implemented by subcalss')

    def save(self):
        """Save content to persistent state
        """
        if self.parent:
            self.parent.save()
        else:
            raise NotImplementedError('Neither class or parent implements save')

    def render(self):
        """Generate HTML from annot markdown
        """
        if not self._render_on:
            return
        elif self.parent:
            self.parent.render()
        else:
            raise NotImplementedError('Neither class or parent implements render')
    
    def _internal_path(self, *sub_paths):
        """Get a file path within the annot project, creating
        any necessary parent directories

        Returns:
           (str, str): first string is the absolute path, second
               string is the path relative to annot directory
        """
        full_path = os.path.join(self.dir, *sub_paths)
        dir_name = os.path.dirname(full_path)
        os.makedirs(dir_name, exist_ok=True)
        rel_path=os.path.relpath(full_path, start=self.dir)
        return full_path, rel_path
        
    def add_markdown(self, markdown_str, before='\n\n', end='\n'):
        """Add raw markdown

        Arguments:
            markdown_str (str) - markdown to be added to page

        Keyword arguments:
            before (str) - text to insert into index.md before
                markdown_str. The default '\n\n' ensures an empty line
                exists between markdown_str and the end of any existing
                content, so that markdown_str is interpreted as part of
                previous markdown.
            end (str) - text to insert after markdown_str.
            update (bool) - update() the page after adding to index.md.
        """
        self._write(before + markdown_str + end)
        self.save()
        return self
            
    def add_dataframe(self, df,
                      df_name=None,
                      as_csv=True,
                      row_limit=10,
                      narrow=False,
                      datatables=False,
                      index=True,
                      formatters='',
                      overwrite=True):
        """Add a pandas.DataFrame to index.md

        Arguments:
            df (pandas.DataFrame) - dataframe to be added to index.md

        Keyword arguments:
            df_name (str) - a unique identifier for the dataframe,
                which will be used to save the file. If not provided,
                the file name will be the hash of the file contents.
            as_csv (bool): If True, the dataframe is saved to disk
                as a csv, and annot_csv() is used in the index.md. If
                False, dataframe is pickled and annot_dataframe() is
                used.
            index (bool): If True, include index as columns on the
                rendered HTML page.
            overwrite (book): If False and df_name has already been
                added, raise Exception. If True, overwrite.
            row_limit (int) - number of rows to include, e.g. 10. Used to
                show a sample of the dataframe to keep the markdown/HTML
                from getting too large in file size.
            datatables (bool): If True, table will be decorated with
                DataTables.js when the HTML loads.        
            narrow (bool): If False, the table will take up the full
                HTML page width. If True, only half width. Use for smaller
                tables. (This is admittedly klunky to make the user
                specify this, dynamic width at some point).
            index (bool): If True, include index as columns in rendered
                HTML page.
            formatters (str): Optional formatting for each column.
                Example: "mean={:.1f},description={:10.10s}"
       
        Returns:
            (None)
        """
        
        # pickle the dataframe
        if df_name:
            if as_csv:
                csv_real_path, csv_annot_path=self._internal_path(
                    'data/{}.csv'.format(df_name))
                if not df.index.name:
                    df.index.name='index'
                df.to_csv(csv_real_path, index=index)
            else:
                pickle_path, index_md_path=self._internal_path(
                    'data/{}.pickle'.format(df_name))
                with open(pickle_path, 'wb') as f:
                    pickle.dump(df, f)

        else:
            import tempfile
            import hashlib
            f = tempfile.NamedTemporaryFile(delete=False)            
            if as_csv:
                if not df.index.name:
                    df.index.name='index'                
                df.to_csv(f.name, index=index)
                ext='.csv'
            else:
                pickle.dump(df, f)
                ext='.pickle'
            real_path, annot_path=self._internal_path(
                'data/{}.{}'.format(df_name, ext))
                
            h=hashlib.md5()
            f.seek(0)
            h.update(f.read())
            f.close()
            df_name=h.digest().hex()[:6]
            print(('Saved dataframe with hash name {}. '
                   'Use add_dataframe(..., df_name="my_data") to save '
                   'with descriptive name.').format(df_name))
            if os.path.exists(real_path):
                print('File already exists: {}'.format(real_path))
                os.remove(f.name)
            else:
                shutil.move(f.name, real_path)
                
        arg_list=''
        if row_limit is not None:
            arg_list += ', row_limit={}'.format(row_limit)
        if datatables:
            arg_list += ', datatables=True'
        if narrow:
            arg_list += ', narrow=True'
        if not index:
            arg_list += ', index=False'
        if formatters:
            arg_list += ', formatters="{}"'.format(formatters)

        if as_csv:
            self._write('\n\nannot_csv("{}"{})\n'.format(
                csv_annot_path, arg_list))
        else:
            self._write('\n\nannot_dataframe("{}"{})\n'.format(
                index_md_path, arg_list))
        self.save()
        return self

    def add_figure(self, fig, img_name, overwrite=True):
        """Add a matplotlib figure to index.md.

        This saves the figure to the images/ directory, and
        adds a custom 'annot_image()' call to index.md. When
        index.html is rendered, the image will be included inline as
        base64.

        Arguments:
            fig (matplotlib.Figure) - figure to be added.
            img_name (str) - File name to use when saving the figure
                to annot/images. Must be different than all other
                images on the page.

        Keyword arguments:
            overwrite (bool) - If False and an image with this name
                has already been added to this page, this will
                raise an KeyError exception.
            update (bool) - update() the page after adding to index.md.

        Returns:
            (None)
        """
        img_path, img_rel_path=self._internal_path(
            'images', img_name + '.png')
        if not overwrite and os.path.exists(img_path):
            raise KeyError(('Already an image file with that '
                            'name: {}, use overwrite=True'
                            ''.format(img_path)))
        fig.savefig(img_path, format='png', bbox_inches='tight')
        self._write('\n\n' + 'annot_image("{}")\n'.format(img_rel_path))
        self.save()
        return self

    def add_csv(self, csv_path,
                copy=True,                
                row_limit=10,
                narrow=False,
                formatters='',
                datatables=False):
        """Add a csv to index.md

        This copies the csv into annot/data/

        Arguments:
          path (str): path to file to add, presumably in annot_dir/data.      
          annot_dir (str): path to annot_dir containing index.md.

        Keyword arguments:
            row_limit (int) - Only include this many rows in the markdown
                table, to keep the HTML file size reasonable. If None,
                include entire csv as table.
            datatables (bool) - If true, include DataTables.js.
            copy (bool) - If True, copy the csv to an internal annot
                directory. If False, Use the live version at csv_path
                each time the markdown is regenerated.
            auto_header (bool) - If true, this creates a header 1
                called 'Auto added' and puts the csv under that.
            narrow (bool): If true, use half width

        
        Returns:
            (none)
        """
        csv_basename=os.path.basename(csv_path)
        
        # copy csv into data/
        if copy:
            dest_path,rel_path=self._internal_path(
                'data', csv_basename)
            if os.path.abspath(csv_path)!=os.path.abspath(dest_path):
                shutil.copy(csv_path, dest_path)
        else:
            rel_path=os.path.relpath(csv_path, start=self.dir)
            markdown_path=csv_path

        # determine if narrow (if average line length below threshold)
        max_read_bytes=2056
        narrow_chars_per_line=80
        with open(csv_path, 'r') as f:
            s = f.readlines(max_read_bytes)
        narrow = len("".join(s))/len(s) < narrow_chars_per_line
            
        # add lines for new file
        csv_line = '\n\nannot_csv("{}"'.format(rel_path)
        if row_limit is not None:
            self._write('\n\nShowing first {} rows.\n'.format(row_limit))
            csv_line += ', row_limit={}'.format(row_limit)
        if datatables:
            csv_line += ', datatables=True'
        if narrow:
            csv_line += ', narrow=True'
        if formatters:
            csv_line += ', formatters="{}"'.format(formatters)            
        csv_line += ')\n'
        self._write(csv_line)
        self.save()
        return self

class Section(AbstractAnnotClass):
    """A Section is a portion of a Page, so that content can be added
    to that section specifically, wherever it falls within the order
    of the Page, rather than to the end of the Page.
    """

    content=''

    def _write(self, s):
        """Helper method that appends a string to content
        """
        self.content += s

    def clear(self):
        self.content=''
        return self

class Page(AbstractAnnotClass):
    """A rendered HTML page, and a directory structure of
    configuration and source data used to rendering it.
    """
    
    def __init__(self, annot_dir=DEFAULT_ANNOT_DIR):
        """
        Keyword arguments:
           annot_dir (str) - path to annot directory. If not
               provided, uses the default of './annot'.
           overwrite (bool) - If True, existing index.md is erased.
        """

        self.parent=None
        
        self.dir=os.path.abspath(annot_dir)
        """Directory containg all files necessary for generating
        the HTML page
        """
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        # copy datatables directory into annot dir
        # disabled, I'm doing inlining instead
        # local_datatables_dir=os.path.join(
        #     self.dir, 'DataTables')
        # if not os.path.exists(local_datatables_dir):
        #     print('Copying datatables to local')            
        #     package_datatables_dir = os.path.join(
        #         os.path.dirname(__file__), 'includes/DataTables')
        #     shutil.copytree(package_datatables_dir,
        #                     local_datatables_dir)
            
        self.index_md=os.path.join(self.dir, 'index.md')
        """The markdown file that specifies the content of the
        rendered .html file. This file contains non-markdown
        directives (e.g. the annot_*() lines) that the annot package
        parses into regular markdown, before passing to a
        markdown->html converter.
        """

        self.index_html=os.path.join(self.dir, 'index.html')
        """The output HTML file rendered from index_md
        """

        self._init_sections()

        if os.path.exists(self.index_html):
            import IPython.display
            IPython.display.display(
                IPython.display.FileLink(os.path.relpath(self.index_html)))        
        line_count=len([line for line in self.content.split('\n')
                        if line])
        if line_count:
            print('Existing index.md has {} lines of content'.format(
                line_count))
        else:
            print('Empty index.md')

    def _init_sections(self, use_disk=True):
        """Set up the Page's sections.

        By default, this will be from the index.md file on disk. If
        that file doesn't exist, or use_disk=False, sections will be
        empty.

        Keyword arguments:
            use_disk (bool) - If True and index.md exists, create
            sections from that. If False, sections will be empty.
        """
        
        self.sections=collections.OrderedDict()
        """The context of the page, broken up into named, ordered
        sections, with each section having its own markdown content
        """

        self.section_active = None
        """The section to which new content is written, if a specific
        section is not otherwise specified. Be default, this is the
        last section of the page.
        """

        # empty page
        if not use_disk or not os.path.exists(self.index_md):
            self.sections['']=Section(self)
            self.section_active = self.sections['']
            return

        # read from disk
        with open(self.index_md, 'r') as f:
            index_md_content=f.readlines()

        # start with default section
        sec = Section(self)
        self.sections[''] = sec
        self.section_active = sec

        # iterate over lines, creating new sections as needed
        for line in index_md_content:
            res = parse_annot_md(line, 'annot_section')
            if res:
                func_name, args, kwargs = res
                section_name = args[0]
                sec = Section(self)
                self.sections[section_name] = sec
                self.section_active = sec
                continue

            sec.content += line

    def __getitem__(self, section_id):
        """Retrieve or create a section
        """
        if not section_id in self.sections:
            self.sections[section_id]=Section(self)
        return self.sections[section_id]


    def _write(self, s):
        """Save str s to content of active section.

        """
        self.section_active.content += s

    def section_active_set(self, section_id):
        self.section_active=self.sections[section_id]

    # def sections_add(self, section_id, after=None, before=None,
    #                  overwrite=True):
    #     """Create and return a new section at the end of the page by
    #     default.

    #     Arguments:
    #         section_id (str): An unique identifier for this section

    #     Keyword arguments:
    #         after (str): If provided, create the new section
    #             immediately after the specified section. Section
    #             create at end of page if both this and before are
    #             None. If both after= and before= are specified. 
    #         before (str): If provided, create new section immediately
    #             before this section. Section created at end of page if
    #             both this and after= are None. If this is True,
    #             section is created at beginning of page.
    #         overwrite (bool): If False and section_id already exists,
    #             raises an exception. If True and section_id already
    #             exists, deletes existing section.

    #     Returns:
    #        (Section): the newly created section

    #     Raises:
    #        (KeyError): If section_id already exists.
    #        (ValueError): if both before= and after= are provided.
    #     """

    #     if not overwrite and section_id in self.sections:
    #         raise KeyError("Already a section with id '{}'. "
    #                        "Use overwrite=True.".format(
    #             section_id))

    #     sec = Section(self)
    #     self.sections[section_id] = sec
    #     self.section_active=sec
    #     return sec

    @property
    def section_auto_add(self):
        """Retrieve the auto-add section, creating it if it does not
        exist

        The auto-add section is just a section named 'auto-add' where
        automatically added content is placed.        
        """
        if 'auto-add' not in self.sections:
            aa = Section(self)
            aa.add_markdown('# Auto-add')
            self.sections['auto-add'] = aa
        return self.sections['auto-add']

    @property
    def content(self):
        """Return combined content from all sections

        Returns:
           (str) a usually multiline string, which joines all of
               self.sections.contents together.
        """
        content = []
        for section_name, section in self.sections.items():
            if section_name:
                content.append("annot_section('{}')\n"
                               "".format(section_name))
            content.append(section.content)
            content.append('\n\n')
        return "".join(content)

    def save(self, verbose=False):
        """Save Page content to index.md and update HTML

        Arguments:
            render (bool): If True, also call render.
        """
        # save content to index.md
        with open(self.index_md, 'w') as f:
            f.write(self.content)

        if self._render_on:
            self.render(verbose=verbose)

    def render(self, verbose=False):
        """Create an HTML page from markdown

        Parses for these markdown customizations specific to annot:
         - annot_csv('data/my.csv' [,rows=10] [,datatables=True])
         - annot_image('images/my.png')

        Keyword Arguments:
            verbose (bool) - Print messages to stdout

        Returns:
            (None)
        """

        if verbose:
            print('Updating {}'.format(self.index_html))
        
        # make annot/temp/ directory
        os.makedirs(os.path.join(self.dir, 'temp'), exist_ok=True)

        # Add links to source files to top of page
        annot_md = (
            '<p><a href="./index.md.txt">index.md</a> '
            '<a href="./temp/render.md.txt">markdown</a></p>')+\
            self.content
            
        # save a copy as index.md.txt, so browser can display for
        # debugging
        with open(self.index_md + '.txt', 'w') as f:
            f.write(annot_md)

        # version 2 has annot-specific markdown translated to regular
        # markdown
        annot_md_2 = []
        for line in annot_md.split("\n"):
            line = line.strip()

            # annot_csv()
            res = parse_annot_md(line, 'annot_csv')
            if res:
                func_name, args, kwargs = res
                path = os.path.join(self.dir, args[0])
                csv_md = annot_csv(path, self.dir, **kwargs)
                annot_md_2.append(csv_md)
                annot_md_2.append("\n")
                continue

            # annot_dataframe()
            res = parse_annot_md(line, 'annot_dataframe')
            if res:
                func_name, args, kwargs = res
                path = os.path.join(self.dir, args[0])
                df_md = annot_dataframe(path, self.dir, **kwargs)
                annot_md_2.append(df_md)
                annot_md_2.append("\n")
                continue

            # annot_image()
            res = parse_annot_md(line, 'annot_image')
            if res:
                func_name, args, kwargs = res
                path = os.path.join(self.dir, args[0])
                img_md = annot_image(path, **kwargs)
                annot_md_2.append(img_md)
                annot_md_2.append("\n")
                continue

            # annot_section()
            res = parse_annot_md(line, 'annot_section')
            if res:
                func_name, args, kwargs = res
                section_name = args[0]
                annot_md_2.append('<!---\n{}\n-->\n'.format(line))
                continue
                
            # pass all other text through as regular markdown
            annot_md_2.append(line)

        # save a copy of the final markdown
        with open(os.path.join(self.dir, 'temp', 'render.md'), 'w') as f:
            f.write("\n".join(annot_md_2))

        # save a copy as render.md.txt, so browser can display for
        # debugging
        with open(os.path.join(self.dir, 'temp', 'render.md.txt'), 'w') as f:
            f.write("\n".join(annot_md_2))

        # generate HTML from regular markdown
        annot_html = markdown.markdown("\n".join(annot_md_2),
                                       extensions=['tables', 'extra'])

        # parse the HTML for annot comments
        annot_html_2 = []
        next_table_is_dt = False
        next_table_is_narrow = False
        for line in annot_html.split('\n'):
            # if datatables comment is found, set flag to catch next
            # table
            if line==DATATABLES_COMMENT:
                next_table_is_dt=True
                continue
            if line==IS_NARROW:
                next_table_is_narrow=True
                continue
            # if table is found and datatables flag is on, add the
            # appropriate classes
            if next_table_is_dt and line=='<table>':
                class_list=['datatables', 'compact']
                if next_table_is_narrow:
                    class_list.append('narrow')
                annot_html_2.append(
                    '<table class="{}">'.format(" ".join(class_list)))
                next_table_is_dt=False
                next_table_is_narrow=False
                continue
            # otherwise add the line
            annot_html_2.append(line)
        annot_html_2 = "\n".join(annot_html_2)
            
        page_html = ""
        page_html += '<!DOCTYPE html>\n'
        page_html += '<head>\n'
        page_html += "<meta charset='utf-8'>\n"
        page_html += '<title>annotate</title>\n'

        
        # datatables css
        page_html += '<style>\n'
        package_dir=os.path.dirname(__file__)
        datatables_css=os.path.join(package_dir, 'includes',
                                    'DataTables',
                                    'datatables.min.css')
        with open(datatables_css, 'r') as f:
            page_html += f.read()
        page_html += '\n</style>\n'            
        """<link rel="stylesheet" type="text/css"
                 href="DataTables/datatables.min.css"/>\n""" #old

        # annot css
        page_html += '<style>\n'
        default_css_path=os.path.join(package_dir, 'includes', 'default.css')
        with open(default_css_path, 'r') as f: 
            page_html += f.read()
            page_html += '\n</style>\n'
        
        # datatales js
        page_html += '<script>\n'
        datatables_js=os.path.join(package_dir, 'includes',
                                    'DataTables', 'datatables.min.js')
        with open(datatables_js, 'r') as f:
            page_html += f.read()
        page_html += '\n</script>\n'            
        """<script type="text/javascript"
                   src="DataTables/datatables.min.js"></script>\n""" #old

        page_html += """
            <script>
              $(document).ready( function () {
              $('.datatables').DataTable({
                "order": []
                });
              } );
            </script>
            """
            
        page_html += '</head>\n'
        page_html += '<body>\n'
        page_html += '''<p>This page is analysis performed in python and 
        rendered with the annot package.</p>''' 
        page_html += annot_html_2
        page_html += '</body>\n'

        # write index.html
        with open(self.index_html, 'w') as f:
            f.write(page_html)

    def clear(self):
        """Make index.md an empty file. Permanently deletes

        Returns:
            (None)
        """
        self._init_sections(use_disk=False)
        return self
        
    def monitor(self):
        """Monitor for file changes in annotation directory and update
        index.html

        Returns:
            (None)
        """

        # create a dictionary of known files, saving the current
        # timestamp as dict values.
        watch_path = os.path.join(self.dir, 'data')
        known_files = [os.path.join(watch_path, file)
                       for file in os.listdir(watch_path)]
        known_files = {file: os.stat(file).st_mtime
                       for file in known_files}
        index_md_time = os.stat(self.index_md).st_mtime
        
        print('{}  Starting monitor on {} files in {}'.format(
            time.ctime(), len(known_files), watch_path))

        # monitoring loop
        while True:
            # if index.md changed, reload content from disk and
            # update HTML
            if index_md_time!=os.stat(self.index_md).st_mtime:
                print(time.ctime(), ' Index.md changed, re-rendering HTML')
                self._init_sections()
                self.render()
                index_md_time=os.stat(self.index_md).st_mtime
                
            # iterate over data files on disk. if new file, add it. If
            # existing file changed, re-render HTML
            cur_files = [os.path.join(watch_path, file)
                         for file in os.listdir(watch_path)]
            need_save = False
            need_render=False
            for file in cur_files:
                st_mtime=os.stat(file).st_mtime                
                if file not in known_files:
                    # if the file is new, add it
                    print('{}  New file: {}'.format(time.ctime(), file))
                    self.section_auto_add.add_csv(file)
                    known_files[file]=st_mtime                    
                    need_save=True
                elif known_files[file]!=st_mtime:
                    # if the file has a different timestamp, do update
                    print('{}  Updated file: {}'.format(time.ctime(), xfile))
                    known_files[file]=st_mtime
                    need_render=True
            if need_save:
                print(time.ctime(), ' Updating index.md and re-rendering HTML')
                self.save()
                index_md_time=os.stat(self.index_md).st_mtime
            elif need_render:
                print(time.ctime(), ' Re-rendering HTML')
                self.render()                
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def open(self):
        """Open HTML page in web browser
        """
        if not os.path.exists(self.index_html):
            self.render()
        if not os.path.exists(self.index_html):
            print('ERROR Failed to generate page after render:',
                  self.index_html)
            return
        webbrowser.open(self.index_html)

            
        
def setup_page(demo=False):
    """Populate an annot directory for a new page

    Keyword arguments:
        demo (bool) - If true, include sample code in index.md
            and sample files.

    Returns:
        (None)
    """

    os.makedirs(DEFAULT_ANNOT_DIR)
    print('Created annot/')

    # index.md
    with open('annot/index.md', 'w') as f:
        if demo:
            f.write(DEFAULT_MD)
        else:
            f.write('# Annot\n')
            print('Created annot/index.md')

    # data/ directory, with optional demo/sample files
    os.makedirs('annot/data')
    if demo:
        with open('annot/data/sample1.csv', 'w') as f:
            f.write(SAMPLE_CSV1)
            print('Created annot/data/sample1.csv')
        with open('annot/data/sample2.csv', 'w') as f:
            f.write('id,value\n')
            for i in range(0,100):
                f.write('{},{}\n'.format(i,i*100))
            print('Created annot/data/sample2.csv')

    # temp/ and DataTables/ directory
    os.makedirs('annot/temp')
    shutil.copytree('DataTables', 'annot/DataTables')
    print('Created annot/DataTables')

    # generate initial HTML page
    page=Page(DEFAULT_ANNOT_DIR)
    page.save(verbose=True)    

    

        
# #####################################################
#
# customized markdown handling specific to annot

DATATABLES_COMMENT = '<!-- annot.py next table is datatables -->'
IS_NARROW='<!-- narrow -->'

def annot_csv(csv_path, annot_dir,
              row_limit=None,
              datatables=False,
              index=None,
              formatters=None,
              narrow=False):
    """Generate markdown table for csv

    Arguments:
        csv_path (str) - path to csv file
        Annot_dir (str) - path to annot directory

    See add_csv() for documentation on keyword arguments

    NOTE The index arg is just here for inter-changeability with
    annot_dataframe and isn't used. 11/10/2020.
        
    Returns:
        (str) markdown string for table of csv 
    """

    if formatters:
        # TODO it's a bit kludgey that I import with pandas if there
        # are formattings and manually if no formattings.
        import pandas as pd
        df=pd.read_csv(csv_path)
        if row_limit:
            df=df.head(row_limit)
        index=False
        table=annot_formatters_helper(df, formatters, index,
                                      data_id=csv_path)

    else:
    
        with open(csv_path, 'r') as f:
            # full file
            if not row_limit:
                table = csvtomd.csv_to_table(f, ',')
            # limited rows
            else:
                sample_csv = io.StringIO()
                for i in range(row_limit+1):
                    sample_csv.write(f.readline())
                sample_csv.seek(0)
                table = csvtomd.csv_to_table(sample_csv, ',')
        
    # convert to markdown
    md = csvtomd.md_table(table)

    # if datatables, prepend a comment to parse later
    if datatables:
        md = DATATABLES_COMMENT + "\n\n" + md
    if narrow:
        md = IS_NARROW + "\n" + md
    
    return md

def annot_formatters_helper(df, formatters, index,
                            data_id=None):
    """Apply {:1f}-style formats to columns of a dataframe

    Arguments:
        df (pandas.DataFrame): Data to be parsed.
        formatters (str): see help in add_dataframe().
        index (bool): If True, index is included in returned values.

    Keyword arguments:
        data_id (str): If an exception is encountered during
           formatting, this str will be included in the exception
           message to make it easier for the user to identify
           where the error is occuring.

    Returns a list of list, where each sub-list is a row of str
    values.
    """
    # get column formatters, if any
    if formatters:
        fmts=annot_lex.parse(formatters)
    else:
        fmts={}
    fmts={col: fmt.format for col,fmt in fmts.items()}
    if '*' not in fmts:
        fmts['*']=str
        
    # convert dataframe to a list of lists. Each sub-list
    # is a column of str values.
    table = []    
    if index:
        table.append([df.index.name]+
                     [str(_) for _ in df.index])
    for col_name, col in df.items():
        fmt=fmts.get(col_name, fmts['*'])
        try:
            table.append([col_name]+list(col.apply(fmt)))
        except ValueError as e:
            if not "Unknown format code" in e.args[0]:
                raise e
            if not data_id:
                data_id='<no data_id>'
            raise ValueError((
                "{} in column '{}' in dataset '{}'. "
                "Formatters: {}").format(
                    e.args[0], col_name, data_id, formatters)) from None

    # transpose the table, from list of cols to list of rows,
    # for csvtomd
    table=[list(_) for _ in zip(*table)]        

    return table


def annot_dataframe(df_pickle_path, annot_dir, row_limit=None, datatables=False,
                    narrow=False, index=True, formatters=''):
    """Generate markdown table for a pickled dataframe

    Arguments:
        df_pickle_path (str) - path to csv file
        annot_dir (str) - path to annot directory

    See add_dataframe() for documentation on keyword arguments
    
    Returns:
        (str) markdown string for table containing dataframe
    """
    md=''
    with open(df_pickle_path, 'rb') as f:
        df = pickle.load(f)
    is_multiindex=df.index.nlevels>1

    if row_limit:
        if row_limit < df.shape[0]:
            md += '\n\nShowing first {} rows of {}.\n'.format(
                row_limit, df.shape[0])
            df=df.head(row_limit)
            
    # ensure an index name, otherwise csvtomd gets confused
    if not df.index.name:
        df.index.name='index'

    # set NaN to empty string (so datatables can sort)
    df=df.fillna('')

    # apply formatting (if any), convert to list of lists
    table=annot_formatters_helper(df, formatters, index,
                                  data_id=df_pickle_path)

    # if formatters:
    #     fmts=annot_lex.parse(formatters)
    # else:
    #     fmts={}
    # fmts={col: fmt.format for col,fmt in fmts.items()}
    # if '*' not in fmts:
    #     fmts['*']=str
                
    # # convert dataframe to a list of lists. Each sub-list
    # # is a column of str values.
    # table = []    
    # if index:
    #     table.append([df.index.name]+
    #                  [str(_) for _ in df.index])
    # for col_name, col in df.items():
    #     fmt=fmts.get(col_name, fmts['*'])
    #     table.append([col_name]+
    #                  list(col.apply(fmt)))

    # # transpose the table, from list of cols to list of rows,
    # # for csvtomd
    # table=[list(_) for _ in zip(*table)]

    # convert table strs to markdown
    md += '\n\n' + csvtomd.md_table(table)

    # if datatables, prepend a comment to parse later
    if datatables:
        md = DATATABLES_COMMENT + "\n" + md
    if narrow:
        md = IS_NARROW + "\n" + md
        
    return md

def annot_image(image_path):
    """Generate markdown for inline image

    Arguments:
        image_path (str) - path to png to include

    Returns:
        (str) - markdown string for inline png
    """
    img_name=os.path.basename(image_path)
    with open(image_path, 'rb') as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode('utf-8')
    img_md='![{}](data:image/png;base64,{})\n'.format(
        img_name, img_base64)
    #img_html = '<img src="data:image/png;base64,{}">'.format(img_base64)
    return img_md
    
# #####################################################
#
# helper functions

def create_sample(path, annot_dir, rows=10):
    """Create a sample csv with first X data rows

    Arguments:
        path (str) - path to csv
        annot_dir (str) - path to annot directory

    Keyword arguments:
        rows (int) - number of data rows to include
    
    Returns:
        (str) path to sample file
    """
    with open(os.path.join(annot_dir, path), 'r') as f:
        lines = f.readlines()[:(rows+1)]
    file_name = os.path.basename(path)
    out_path = os.path.join(annot_dir, 'temp', file_name+'.sample') 
    with open(out_path, 'w') as f:
        f.writelines(lines)
        
    return out_path

# def eval_simple(s):
#     """Evaluate a simple python expression to either str, int or
#     bool.

#     Used for parsing "annot_xxx('a', 10, val=True)"
    
#     >>> eval_simple('"this is a str"')
#     'this is a str'
    
#     >>> eval_simple('10')
#     10

#     >>> eval_simple(False)
#     10
    
#     """
#     # bool
#     if s=='True':
#         return True
#     if s=='False':
#         return False
#     # strings
#     if s[0] in ['"', "'"]:
#         return s.replace('"', '').replace("'",'')
#     # integers
#     else:
#         try:
#             return int(s)
#         except ValueError as e:
#             raise ValueError(
#                 'Failed to parse "{}" as int'.format(s)) from None
            
def parse_annot_md(line, starts_with):
    """Return the positional and keyword arguments from a line of
    annot extended markdown

    >>> parse_annot_md("annot_csv('my.csv', rows=10)")
    ('annot_csv', ['my.csv'], {'rows': 10})

    Arguments:
        line (str): the line to parse.
        starts_with (str): the function name to check for. If the line
           doesn't start with this, None is returned

    Returns:
        (str, list, dict) - The first element of the tuple is the
           function name. Second is list of positional arguments. The
           third is the dict keyword arguments. 
    """
    if not line.startswith(starts_with):
        return None
    
    return annot_lex.parse(line)
    
    # args = []
    # kwargs = {}

    # # remove function name and parens (no subexpressions handled)
    # # parse arguments on commas (no enclosed allowed)
    # args_str = line[len(starts_with):]\
    #            .replace('(', '').replace(')', '')
    # if args_str=='':
    #     return args, kwargs

    # # parse for args
    # args_list = [_.strip() for _ in args_str.split(',')]    
    # for arg_str in args_list:        
    #     # positional arguments
    #     if '=' not in arg_str:
    #         try:
    #             args.append(eval_simple(arg_str))
    #         except ValueError as e:
    #             raise ValueError(
    #                 "Failed to parse '{}' in \n {}".format(
    #                     arg_str, line, e.args[0]))            
    #     # keyword arguments
    #     else:
    #         i=arg_str.index('=')
    #         k=arg_str[:i].strip()
    #         v=arg_str[i+1:].strip()
    #         try:
    #             kwargs[k.strip()] = eval_simple(v.strip())
    #         except ValueError as e:
    #             raise ValueError(
    #                 "Failed to parse '{}' in \n {}".format(
    #                      arg_str, line, e.args[0]))        
    # return args, kwargs
                
DEFAULT_MD="""
# Default annot page

You are viewing an HTML page generated by annot.py.

This HTML page is generated from a markdown file located at
annot/index.md. To change the content of this HTML, you need to
modified index.md, either by directly editing it or by using the
annoy.py command line.

## Including data

This is a link to a sample csv: [./data/sample1.csv](./data/sample1.csv)

annot_csv('./data/sample1.csv')

## Limiting rows from data

If your csv is large, you may only want to include a sample
of rows so that the annot HTML page doesn't become a large file:

annot_csv('./data/sample2.csv', rows=10)

## annot/data directory

The annot/data directory contains csv files that you want to include
in your page. You can either copy files into this directory or create
symlinks in the data/ directory to files elsewhere, which will allow
the annot page to update when your csv changes.

You can delete the sample .csvs in data/.

## Including an image

TODO: include image

## Markdown reminders

This is __bold__

This is _italics_

This is a bullet list:

* with one
* two
* three items


TODO Below is code:

    this is code
    (because indented 4 spaces)

"""

SAMPLE_CSV1="""id,value,category
1,123,up
2,549,down
3,493,middle
"""



