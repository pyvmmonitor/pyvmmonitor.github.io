'''
@author: Fabio
'''
import os
import shutil
import pyodict

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
<h1 class="header_liclipse">PyVMMonitor</h1>
<!--<p>Profiling Python</p>-->
<ul class="top1">
    <!-- <li><a href="http://???">Get It <strong>Download</strong></a></li> -->
    <li><a href="https://groups.google.com/forum/#!forum/pyvmmonitor">Googlegroups <strong>Forum</strong></a></li>
    <li><a href="http://pyvmmonitor.blogspot.com.br/">View <strong>Blog</strong></a></li>
    <li><a href="https://sw-brainwy.rhcloud.com/tracker/PyVMMonitor/">PyVMMonitor<strong>Tracker</strong></a></li>
</ul>
<ul class="top2">
    <li class="lifull"><a href="download.html">Get it<strong>Download</strong></a></li>
</ul>

<!--
<ul class="top3">
    <li class="lifull">
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=NJW4VEJQZ36GJ">Help to make better<strong>Buy Single User</strong></a>
    </li>
</ul>

<ul class="top4">
    <li class="lifull">
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=G5APKLQNXK7DL">For Organizations<strong>Buy Multi User</strong></a>
    </li>
</ul>

Pricing: A PyVMMonitor license is US$ ?? TBD<br><br><br>
-->
<p><small>Copyright 2014 - Brainwy Software Ltda.<br/>Hosted on GitHub Pages - Theme by <a href="https://github.com/orderedlist">orderedlist</a></small></p>
'''

#===================================================================================================
# apply_to
#===================================================================================================
def apply_to(filename, header=None):
    with open(filename, 'r') as stream:
        contents = stream.read()
        body = extract(contents, 'body')
        apply_to_contents(contents, os.path.basename(filename), body, header or HEADER)


#===================================================================================================
# apply_to_contents
#===================================================================================================
def apply_to_contents(contents, basename, body, header):

    contents = template_contents % {'body': body, 'header': header}

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


#===================================================================================================
# main
#===================================================================================================
def main():
    apply_to(os.path.join(this_file_dir, 'index.html'))
    apply_to(os.path.join(this_file_dir, 'history.html'))
    apply_to(os.path.join(this_file_dir, 'download.html'))
    apply_to(os.path.join(this_file_dir, 'license.html'))
    apply_to(os.path.join(this_file_dir, 'faq.html'))


if __name__ == '__main__':
    main()
    print 'Generation finished'
