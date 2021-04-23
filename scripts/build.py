'''
@author: Fabio
'''
import os
import shutil
import pyodict

DOWNLOAD_REPLACEMENTS = {
    'pyvmmonitor_version': '2.0.1',
    'all_versions_url': 'https://www.mediafire.com/folder/mz3sakuqdul90/PyVmMonitor',
}

DOWNLOADS = '''
https://www.mediafire.com/file/47f58gtybhdmle4/pyvmmonitor_2.0.1_win32.x86_64.exe
https://www.mediafire.com/file/q03boa9ftngy16p/pyvmmonitor_2.0.1_linux.x86_64.tar.gz
https://www.mediafire.com/folder/k8c8ka3fwzpgi/PyVmMonitor_2.0.1
'''

for line in DOWNLOADS.splitlines():
    line = line.strip()
    if not line:
        continue
    if line.endswith('LICENSE.TXT'):
        DOWNLOAD_REPLACEMENTS['license_url'] = line

    elif line.endswith('win32.x86_64.exe'):
        DOWNLOAD_REPLACEMENTS['win64_url'] = line

    elif line.endswith('win32.x86.exe'):
        DOWNLOAD_REPLACEMENTS['win32_url'] = line

    elif line.endswith('macosx.cocoa.x86_64.dmg'):
        DOWNLOAD_REPLACEMENTS['macos_url'] = line

    elif line.endswith('.zip') and ('UPDATE_SITE' in line) or ('UPDATE%20SITE' in line):
        DOWNLOAD_REPLACEMENTS['update_site_url'] = line

    elif line.endswith('linux.x86_64.tar.gz'):
        DOWNLOAD_REPLACEMENTS['linux64_url'] = line

    elif line.endswith('linux.x86.tar.gz'):
        DOWNLOAD_REPLACEMENTS['linux32_url'] = line

    elif 'PyVmMonitor_' in line:
        DOWNLOAD_REPLACEMENTS['folder_url'] = line

    else:
        raise AssertionError('Unexpected line: %s' % (line,))


#===================================================================================================
# copytree
#===================================================================================================
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)


template_contents = open(os.path.join(os.path.dirname(__file__), 'template.html'), 'r').read()
this_file_dir = os.path.dirname(__file__)
page_dir = os.path.dirname(this_file_dir)

HEADER = '''
<h1 class="header_liclipse">PyVmMonitor</h1>
<!--<p>Profiling Python</p>-->
<ul class="top1">
    <li><a href="https://groups.google.com/forum/#!forum/pyvmmonitor">Googlegroups <strong>Forum</strong></a></li>
    <!--<li><a href="http://pyvmmonitor.blogspot.com.br/">View <strong>Blog</strong></a></li>-->
    <li><a href="https://www.brainwy.com/tracker/PyVmMonitor/">PyVmMonitor<strong>Tracker</strong></a></li>
</ul>
<ul class="top2">
    <li class="lifull"><a href="download.html">Get it<strong>Download</strong></a></li>
</ul>

<ul class="top3">
    <li class="lifull"><a href="buy.html">Help to make it better<strong>Buy</strong></a></li>
</ul>

<p><small>Copyright 2014-2021 - Brainwy Software Ltda.<br/>Hosted on GitHub Pages - Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
'''


#===================================================================================================
# apply_to
#===================================================================================================
def apply_to(filename, header=None, additional=None):
    if additional is None:
        additional = {}
    with open(filename, 'r') as stream:
        contents = stream.read()
        body = extract(contents, 'body')
        apply_to_contents(contents, os.path.basename(filename), body, header or HEADER, additional)


def template_replace(contents, kwargs):
    to_replace = set()
    to_replace.update(list(kwargs.keys()))

    for r in to_replace:
        c = kwargs.get(r, '')
        contents = contents.replace('%(' + r + ')s', c)
    return contents

#===================================================================================================
# apply_to_contents
#===================================================================================================
def apply_to_contents(contents, basename, body, header, additional=None):
    if additional is None:
        additional = {}
    additional = additional.copy()
    contents = template_contents % {'body': body, 'header': header}
    contents = template_replace(contents, additional)

    with open(os.path.join(page_dir, basename), 'w') as out_stream:
        out_stream.write(contents)


#===================================================================================================
# extract
#===================================================================================================
def extract(contents, tag):
    i = contents.index('<%s>' % tag)
    j = contents.rindex('</%s>' % tag)
    return contents[i + len(tag) + 2:j]


class Info:

    def __init__(self, title):
        self.title = title
        self.filename = None


FILE_TO_INFO = pyodict.odict([
    ('attach_to.html', Info('Attach to running CPython program and use Yappi to do a profile session')),
    ('command_line.html', Info('Command line parameters for PyVmMonitor')),
    ('public_api.html', Info('API to use PyVmMonitor programatically')),
    ('preferences.html', Info('PyVmMonitor preferences (theme, listening port, editor font, etc.)')),
    ('profile_on_different_machine.html', Info('Profile on another machine')),
    ('pydev_integration.html', Info('PyDev integration')),
    ('pycharm_integration.html', Info('PyCharm integration')),
])

help_location = os.path.join(os.path.dirname(__file__), 'manual')

if os.path.exists(help_location):
    for f in os.listdir(help_location):
        if not f.endswith('.html'):
            continue
        if f not in FILE_TO_INFO:
            raise ValueError('Not expecting: %s' % (f,))
        FILE_TO_INFO[f].filename = os.path.join(help_location, f)
else:
    print(('Dir: %s does not exist (unable to generate related pages)' % help_location))


#===================================================================================================
# create_manual_header
#===================================================================================================
def create_manual_header():
    lis = []
    for file_basename, file_info in FILE_TO_INFO.items():
        lis.append('<p><a href="%s">%s</a></p>' % (
            os.path.basename(file_info.filename),
            file_info.title
        ))

    return '''
%(li)s<br><br><br>
<p><small>Copyright 2014-2021 - Brainwy Software Ltda.<br/>Hosted on GitHub Pages - Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
''' % {'li': '\n'.join(lis)}


if os.path.exists(help_location):
    MANUAL_HEADER = create_manual_header()


#===================================================================================================
# create_manual_page
#===================================================================================================
def create_manual_page():

    manual_body = '''
<h3>Choose the topic you're interested in...</h3>
<img src="images/arrow_left.png" />
'''
    apply_to_contents(manual_body, 'manual.html', manual_body, MANUAL_HEADER)


#===================================================================================================
# main
#===================================================================================================
def main():
    # Manual
    if os.path.exists(help_location):
        create_manual_page()
        for info in FILE_TO_INFO.values():
            apply_to(info.filename, header=MANUAL_HEADER)

    apply_to(os.path.join(this_file_dir, 'index.html'))
    apply_to(os.path.join(this_file_dir, 'history.html'))
    apply_to(os.path.join(this_file_dir, 'download.html'), additional=DOWNLOAD_REPLACEMENTS)
    apply_to(os.path.join(this_file_dir, 'license.html'))
    apply_to(os.path.join(this_file_dir, 'faq.html'))
    apply_to(os.path.join(this_file_dir, 'buy.html'))
    apply_to(os.path.join(this_file_dir, 'contact.html'))


if __name__ == '__main__':
    main()
    print('Generation finished')
