import downloader as dl
import scripts as scr
import file_renaming

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

_X_MINSIZE = 500


class UI_Work:
    """An instance of this class can be used to manipulate an additional 
    tkinter frame widget, which appears below the information frame and 
    provides the user with feedback on the global state of the download, using 
    a progress bar and numerical information."""

    def __init__(self, root, init_status):
        self.__root = root
        self.__w_f = ttk.Frame(root, relief="sunken", padding="15 15 15 15")
        self.__w_f.grid(row=2, sticky="nwes", padx=20, pady=20)
        self.__w_f.columnconfigure(0, weight=1)

        self.__prg = DoubleVar(value=0.0)
        self.__percentage = StringVar(value="")
        self.__counter = StringVar(value="0/0")
        self.__total_size = None
        self.__status = StringVar(value=init_status)

        ttk.Label(self.__w_f, textvariable=self.__status).grid(
            row=0, column=0, sticky=W)
        update_window_minsize(self.__root)
        self.__refresh_ui()

    def _add_progressbar(self, total_size):
        """Adds a progress bar to the work frame
        
        Args:
        - total_size (int) : the total size in bytes of the video/playlist
        to download"""
        self.__total_size = total_size
        prg_bar = ttk.Progressbar(
            self.__w_f, orient=HORIZONTAL, mode="determinate", 
            variable=self.__prg, maximum=total_size)
        prg_bar.grid(row=1, column=0, columnspan=2, sticky=(W, E))
        ttk.Label(self.__w_f, textvariable=self.__percentage).grid(
            row=2, column=1, sticky=E)
        ttk.Label(self.__w_f, textvariable=self.__counter).grid(
            row=2, column=0, sticky=W)
        update_window_minsize(self.__root)


    def set_status(self, new_status):
        """Changes the string displayed at the top of the work frame (above
        the progress bar, if showed)
        
        Args:
        - new_status (str) : the new message to display"""
        self.__status.set(new_status)
        self.__refresh_ui()


    def __refresh_ui(self):
        """Refreshes *all* the widgets of the application window, to ensure
        updates are properly displayed"""
        self.__root.update()
        self.__w_f.update()


    def _destroy(self):
        """Deletes the 'work frame' area from the application window, leaving
        only the information window"""
        self.__w_f.destroy()
        update_window_minsize(self.__root)


    def update_progress_bar(self, bytes_downloaded, new_counter):
        """Upgrades the work frame's progress bar, as well as the percentage of
        bytes downloaded and counter of downloaded videos, which are both
        displayed near the progress bar
        
        Args:
        - bytes_downloaded (int) : the total number of bytes that have been
        downloaded yet
        - new_counter (int) : the number of videos that have fully been
        downloaded yet"""
        self.__prg.set(bytes_downloaded)
        self.__counter.set(new_counter)
        self.__percentage.set("{:.2f}%".format(bytes_downloaded*100/self.__total_size))
        self.__refresh_ui()

def center_window(win):
    """
    Centers a tkinter window
    :param win: the main window or Toplevel window to center

    source:
    https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def update_window_minsize(root):
    """Updates the minimum size of the application window. The new minimum 
    height is such that all tkinter widgets contained in the window can be
    fully displayed, without any truncature
    
    - root (tkinter.Tk) : the application window whose minimum size must be
    updated"""
    root.update()
    root.minsize(_X_MINSIZE, root.winfo_reqheight())


def _func_button(*args):
    """Launches the download process based on the information provided by the 
    user in the 'info frame'. Also creates a new 'work frame' into the 
    application window to display and update the state of the download process.
    """  
    try:
        dl_b.state(['disabled'])
        is_playlist = (dlt.get()==scr.DL_TYPES[1])
        uiw = UI_Work(root, init_status=scr.LOADING_YT_OBJECT[is_playlist])
        dlr = dl.DownloadRequest(
            link=link.get(), 
            path=path.get(), 
            name=name.get(), 
            audio_only=(True if exten.get()==".mp3" else False),
            is_playlist=is_playlist,
            uiw=uiw)
        uiw._add_progressbar(dlr.total_byte_size())
        uiw.set_status(scr.DOWNLOADING_STREAMS)
        # TODO: add possibility to disable autorenaming
        dlr.download(func_renaming=file_renaming.get_spotify_name)

    except (AssertionError, ValueError) as e:
        messagebox.showerror(parent=root, title="Error", message=e)
    else:
        messagebox.showinfo(parent=root, message=scr.FINISHED_DOWNLOADING)
    finally:
        dl_b.state(['!disabled'])
        uiw._destroy()


def _browse_button(*args):
    """Opens a dialog that lets the user provide the path of a folder (which
    will be the destination path for the downloaded videos), then displays
    the selected file into the appropriate entry"""
    new_path = filedialog.askdirectory()
    path_ent.delete(0)
    path.set(new_path)
    root.update()


def _toggle_vid_pl(*args):
    """Enables the 'Nom fichier' ('filename') entry if the download type is
    set to 'Video', and disables it if the download type is set to 'Playlist'"""
    if dlt.get() == scr.DL_TYPES[0] : name_ent.state(['!disabled'])
    else: name_ent.state(['disabled'])


if __name__ == '__main__':

    root = Tk()
    root.title("YTdownloader")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Info frame
    i_f = ttk.Frame(root, padding="15 15 15 15")
    i_f.grid(row=0, sticky='we')
    i_f.columnconfigure(1, weight=1)

    # Link entry
    ttk.Label(i_f, text=scr.INFO['url']).grid(row=0, column=0, sticky='we')
    link = StringVar()
    link_ent = ttk.Entry(i_f, textvariable=link)
    link_ent.grid(row=0, column=1, sticky='we')

    # Path entry
    ttk.Label(i_f, text=scr.INFO['path']).grid(row=1, column=0, sticky='we')
    path = StringVar()
    path_ent = ttk.Entry(i_f, textvariable=path)
    path_ent.grid(row=1, column=1, sticky='we', columnspan=1)
    browse_b = ttk.Button(i_f, text=scr.BROWSE_BUTTON, 
                          command=_browse_button, width=12)
    browse_b.grid(row=1, column=2, sticky=E)

    # Name entry
    ttk.Label(i_f, text=scr.INFO['name']).grid(row=2, column=0, sticky='we')
    name = StringVar()
    name_ent = ttk.Entry(i_f, textvariable=name)
    name_ent.grid(row=2, column=1, sticky='we')
    ttk.Label(i_f, text=scr.INFO['name_info']).grid(
        row=3, column=0, columnspan=2, sticky=W)

    # Extension combobox
    exten = StringVar()
    exten_cbb = ttk.Combobox(i_f, textvariable=exten, width=6,
                             values=scr.EXT_TYPES, state='readonly')
    exten_cbb.current(1)
    exten_cbb.grid(row=2, column=2, sticky='we')

    # Video/Playlist (download type) combobox
    dlt = StringVar()
    dlt_cbb = ttk.Combobox(i_f, textvariable=dlt, width=8,
                           values=scr.DL_TYPES, state='readonly')
    dlt_cbb.current(0)
    dlt_cbb.grid(row=0, column=2, sticky='we')
    dlt_cbb.bind('<<ComboboxSelected>>', _toggle_vid_pl)

    # 'Download' button
    dl_b = ttk.Button(root, text=scr.DL_BUTTON, command=_func_button, width=20)
    dl_b.grid(sticky=E, padx=15, pady=15)

    for child in i_f.winfo_children(): child.grid_configure(padx=5, pady=5)
    update_window_minsize(root)
    center_window(root)
    link_ent.focus()
    root.bind('<Return>', _func_button)
    root.mainloop()
