import downloader as dl
import scripts as scr
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

_X_MINSIZE = 400


class UI_Work:
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
        self.__status.set(new_status)
        self.__refresh_ui()


    def __refresh_ui(self):
        self.__root.update()
        self.__w_f.update()


    def _destroy(self):
        self.__w_f.destroy()
        update_window_minsize(self.__root)


    def update_progress_bar(self, bytes_downloaded, new_counter):
        self.__prg.set(bytes_downloaded)
        self.__counter.set(new_counter)
        self.__percentage.set("{:.2f}%".format(bytes_downloaded*100/self.__total_size))
        self.__refresh_ui()


def update_window_minsize(root):
    root.update()
    root.minsize(_X_MINSIZE, root.winfo_reqheight())


def _func_button(*args):  
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
        dlr.download()

    except (AssertionError, ValueError) as e:
        messagebox.showerror(parent=root, title="Error", message=e)
    else:
        messagebox.showinfo(parent=root, message=scr.FINISHED_DOWNLOADING)
    finally:
        dl_b.state(['!disabled'])
        uiw._destroy()


def _toggle_vid_pl(*args):
    if dlt.get() == scr.DL_TYPES[0] : name_ent.state(['!disabled'])
    else: name_ent.state(['disabled'])


if __name__ == '__main__':

    root = Tk()
    root.title("YTdownloader")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Info frame
    i_f = ttk.Frame(root, padding="15 15 15 15")
    i_f.grid(row=0, sticky="we")
    i_f.columnconfigure(1, weight=1)

    # Link entry
    ttk.Label(i_f, text=scr.INFO['url']).grid(row=0, column=0, sticky=(W,E))
    link = StringVar()
    link_ent = ttk.Entry(i_f, textvariable=link)
    link_ent.grid(row=0, column=1, sticky=(W,E))

    # Path entry
    ### TODO Change to "open folder" OS window, not just text entry
    ttk.Label(i_f, text=scr.INFO['path']).grid(row=1, column=0, sticky=(W,E))
    path = StringVar()
    path_ent = ttk.Entry(i_f, textvariable=path)
    path_ent.grid(row=1, column=1, sticky=(W,E), columnspan=2)

    # Name entry
    ttk.Label(i_f, text=scr.INFO['name']).grid(row=2, column=0, sticky=(W,E))
    name = StringVar()
    name_ent = ttk.Entry(i_f, textvariable=name)
    name_ent.grid(row=2, column=1, sticky=(W,E))
    ttk.Label(i_f, text=scr.INFO['name_info']).grid(
        row=3, column=0, columnspan=2, sticky=W)

    # Extension combobox
    exten = StringVar()
    exten_cbb = ttk.Combobox(i_f, textvariable=exten, width=6,
                             values=scr.EXT_TYPES, state='readonly')
    exten_cbb.current(1)
    exten_cbb.grid(row=2, column=2, sticky="we")

    # Video/Playlist (download type) combobox
    dlt = StringVar()
    dlt_cbb = ttk.Combobox(i_f, textvariable=dlt, width=8,
                           values=scr.DL_TYPES, state='readonly')
    dlt_cbb.current(0)
    dlt_cbb.grid(row=0, column=2, sticky=(W,E))
    dlt_cbb.bind('<<ComboboxSelected>>', _toggle_vid_pl)

    # 'Download' button
    dl_b = ttk.Button(root, text=scr.DL_BUTTON, command=_func_button, width=20)
    dl_b.grid(sticky=E, padx=15, pady=15)

    for child in i_f.winfo_children(): child.grid_configure(padx=5, pady=5)
    update_window_minsize(root)
    link_ent.focus()
    root.bind('<Return>', _func_button)
    root.mainloop()
