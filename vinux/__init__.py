__author__ = 'vin@misday.com'

import wx, webbrowser
from vincore import Callbacks

(IDX_LABEL, IDX_HELP, IDX_ID, IDX_BITMAP, IDX_KIND, IDX_HANDLER, IDX_ID2) = range(0, 7)

def createMenubar(wnd, menuDef):
    '''menuDef = [('FILE', (
                            ('Open', 'Open a file', MainWindow.ID_MENUITEM_OPEN, self.menuOpen),
                            )
                  )]'''
    menuBar = wx.MenuBar()
    for eachMenu in menuDef:
        label = eachMenu[IDX_LABEL]
        items = eachMenu[1]
        menuBar.Append(createMenuItems(wnd, items), label)
    wnd.SetMenuBar(menuBar)
    return menuBar

def createMenuItems(wnd, menuData):
    menu = wx.Menu()
    for item in menuData:
        if len(item) == 2:
            label = item[IDX_LABEL]
            subMenu = wnd.createMenuItems(item[1])
            menu.AppendMenu(wx.ID_ANY, label, subMenu)
        else:
            label = item[IDX_LABEL]
            help = item[IDX_HELP]
            id = item[IDX_ID]
            handler = item[IDX_HANDLER]
            kind = item[IDX_KIND]
            if not kind:
                kind = wx.ITEM_NORMAL

            if label:
                menu.Append(id, label, help, kind=kind)
                wnd.Bind(wx.EVT_MENU, handler, id=id)
            else:
                menu.AppendSeparator()
    return menu

def createPopmenu(wnd, popmenuDef):
    wnd.popupmenu = wx.Menu()
    for item in popmenuDef:
        label = item[IDX_LABEL]
        help = item[IDX_HELP]
        id = item[IDX_ID]
        handler = item[IDX_HANDLER]
        kind = item[IDX_KIND]
        if not kind:
            kind = wx.ITEM_NORMAL

        if label:
            wnd.popupmenu.Append(id, label, help, kind=kind)
            wnd.Bind(wx.EVT_MENU, handler, id=id, id2=item[IDX_ID2])
        else:
            wnd.popupmenu.AppendSeparator()
    return wnd.popupmenu

def createToolBar(wnd, toolbarDef):
    '''self.TOOLBAR = [
        (MainWindow.ID_TOOL_FETCH, 'Fetch', wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_BUTTON, MainWindow.tsize), self.onUpdate),
        '''
    toolbar = wnd.CreateToolBar()
    for item in toolbarDef:
        label = item[IDX_LABEL]
        help = item[IDX_HELP]
        bitmap = item[IDX_BITMAP]
        id = item[IDX_ID]
        handler = item[IDX_HANDLER]
        kind = item[IDX_KIND]
        if not kind:
            kind = wx.ITEM_NORMAL
        toolbar.AddLabelTool(id, label, bitmap, kind=kind, shortHelp=help)
        wnd.Bind(wx.EVT_TOOL, handler, id=id)
    toolbar.Realize()
    return toolbar

def showDirDlg(wnd, msg = '', path = ''):
    ret = True
    filePath = ''
    dlg = wx.DirDialog(wnd,
                        msg,
                        path,
                        style = wx.OPEN,
                        )
    if dlg.ShowModal() == wx.ID_OK:
        filePath = dlg.GetPath()
    else:
        ret = False
    dlg.Destroy()
    return (ret, filePath)

def showFileDlg(wnd, msg = '', path = '', wildcard = "All Files(*.*)|*.*", single = True):
    if single:
        style = wx.OPEN
    else:
        style = wx.MULTIPLE

    ret = True
    filePath = ''
    dlg = wx.FileDialog(wnd,
                        msg,
                        path,
                        style = style,
                        wildcard = wildcard
                        )
    if dlg.ShowModal() == wx.ID_OK:
        if single:
            filePath = dlg.GetPath()
        else:
            filePath = dlg.GetPaths()
    else:
        ret = False
    dlg.Destroy()
    return (ret, filePath)

def showMsg(wnd, msg = '', title = ''):
    dlg = wx.MessageDialog(wnd, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()
    return True

def openInNewTab(url):
        '''open in browser with new tab'''
        if len(url) > 0:
            webbrowser.open(url, new=2, autoraise=True)
        else:
            print('url is empty')

class FileDropTarget(wx.FileDropTarget, Callbacks):
    (EVT_ON_DROP_FILES,) = range(0, 1)

    def __init__(self):
        wx.FileDropTarget.__init__(self)
        Callbacks.__init__(self)
        self.init([FileDropTarget.EVT_ON_DROP_FILES, ])

    def OnDropFiles(self,  x,  y, fileNames):
        print fileNames
        self.dispatch(FileDropTarget.EVT_ON_DROP_FILES, fileNames)
