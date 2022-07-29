import sys
import os
from cudatext import *
from io import StringIO

# on Unix user must install libs by "pip3 install ....."
# on Win: plugin uses local libs
if os.name=='nt':
    sys.path.append(os.path.dirname(__file__))

from lxml import etree
from lxml import cssselect

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_css_inspector.ini')
fn_icon = os.path.join(os.path.dirname(__file__), 'icon.png')

TITLE = 'CSS Inspector'
ui = app_proc(PROC_THEME_UI_DICT_GET, '')
PANEL_COLOR_BG = ui['EdTextBg']['color']
PANEL_COLOR_FONT = ui['EdTextFont']['color']

class Command:

    def __init__(self):
        self.panel = dlg_proc(0, DLG_CREATE)
        dlg_proc(self.panel, DLG_PROP_SET, prop={
            'color': PANEL_COLOR_BG,
        })
        n = dlg_proc(self.panel, DLG_CTL_ADD, 'listbox_ex')
        dlg_proc(self.panel, DLG_CTL_PROP_SET, index=n, prop={
            'align': ALIGN_CLIENT,
        })
        self.listbox = dlg_proc(self.panel, DLG_CTL_HANDLE, index=n)
        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (TITLE, self.panel, fn_icon) )

    def show_panel(self):
        app_proc(PROC_SIDEPANEL_ACTIVATE, TITLE)

    def config(self):
        file_open(fn_config)

    def on_caret(self, ed_self):

        listbox_proc(self.listbox, LISTBOX_DELETE_ALL)

        # get text until closing >
        x, y, x1, y1 = ed_self.get_carets()[0]
        text = ed_self.get_text_substr(0, 0, 0, y)
        s = ed_self.get_text_line(y)
        while x<len(s) and s[x]!='>':
            x+=1
        text += '\n'+s[:x+1]

        tree=etree.parse(StringIO(text),etree.HTMLParser())
        if not tree:
            return
        roots=tree.getroot()
        if roots is None or len(roots)==0:
            return

        root=roots[-1]
        while(len(root.getchildren())>0):
            root=root.getchildren()[-1]
        if not isinstance(root.tag, str):
            return

        csscode=''
        css=cssselect.CSSSelector('style')(tree)
        for i in css:
            csscode+=i.text

        css_links=[]
        linkedcss=cssselect.CSSSelector('link')(tree)
        for i in linkedcss:
            if i.attrib['rel']=='stylesheet':
                css_links.append(i.attrib['href'])

        dir_ed = os.path.dirname(ed.get_filename())
        for fn in css_links:
            fn = os.path.join(dir_ed, fn)
            if os.path.isfile(fn):
                csscode += '\n'+open(fn, encoding='utf8', errors='replace').read()+'\n'

        csscodeold=csscode
        csscode=''
        for i in csscodeold:
            if i in ['\t']:
                pass
            else:
                csscode+=(i)

        csscodeold=csscode
        csscode=''
        for i in csscodeold.split('\n'):
            while len(i)>0:
                if i[0]==' ':
                    i=i[1:]
                elif i[-1]==' ':
                    i=i[:-1]
                else:
                    break
            csscode=csscode+i

        cssarr=csscode.split('}')[:-1]
        for i in range(len(cssarr)):
            _x = cssarr[i].split('{')
            if len(_x)>1:
                cssarr[i]=[_x[0].split(' '),_x[1]]

        res=''
        for i in cssarr:
            if len(i)>1:
                if 'class' in root.attrib and '.'+root.attrib['class'] in i[0]:
                    res+=i[1]
                elif 'id' in root.attrib  and '#'+root.attrib['id'] in i[0]:
                    res+=i[1]
                elif root.tag in i[0]:
                    res+=i[1]
        if 'style' in root.attrib:
            res+=root.attrib['style']

        listbox_proc(self.listbox, LISTBOX_ADD, index=-1, text='<'+root.tag+'>')
        for s in res.split(';'):
            listbox_proc(self.listbox, LISTBOX_ADD, index=-1, text=s)
