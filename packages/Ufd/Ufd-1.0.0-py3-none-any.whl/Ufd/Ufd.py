from tkinter import (
    Tk,
    PanedWindow,
    Listbox,
    Button,
    Scrollbar,
    PhotoImage,
    messagebox
)
from tkinter.ttk import Treeview, Style
from os.path import normpath, dirname, isdir, isfile, split as path_split
from re import findall, sub, split as re_split
from platform import system
from subprocess import run
from math import ceil
from collections import deque


class Ufd:
    """
        Universal File Dialog - "UFD"
        
        Unopinionated, minimalist, reusable, slightly configurable,
        general-purpose file-dialog.
    """

    def __init__(
        self,
        title:str="Universal File Dialog",
        icon:str="",
        show_hidden:bool=False,
        include_files:bool=True,
        multiselect:bool=True,
        select_dirs:bool=True,
        select_files:bool=True,
        unix_delimiter:bool=True,
        stdout:bool=False
    ):

        """
            Init kwargs as object attributes, save references to 
            Tk PhotoImages, & define the widgets + layout
        """

        if not isinstance(title, str):
            raise TypeError("Argument title must be type string.")

        self.title = title

        if icon:
            if not isinstance(icon, str):
                raise TypeError("Argument icon must be type string.")

            if not isfile(icon):
                raise FileNotFoundError(f"File not found: {icon}")

            self.icon = icon

        else: 
            self.icon = ""

        if show_hidden:
            self.show_hidden = True
        else:
            self.show_hidden = False

        if include_files:
            self.include_files = True
        else:
            self.include_files = False

        if multiselect:
            self.multiselect = True
        else:
            self.multiselect = False

        if select_dirs:
            self.select_dirs = True
        else:
            self.select_dirs = False

        if select_files:
            self.select_files = True
        else:
            self.select_files = False

        if unix_delimiter:
            self.unix_delimiter = True
        else:
            self.unix_delimiter = False

        if stdout:
            self.stdout = True
        else:
            self.stdout = False

        # Tkinter:
        self.dialog = Tk()
        self.dialog.withdraw()
        self.dialog.title(self.title)
        self.dialog.minsize(width=300, height=200)
        self.dialog.geometry("500x300")
        self.dialog.update_idletasks()

        self.file_icon=PhotoImage(
            file=f"{dirname(__file__)}/file.gif",
            master=self.dialog
        ).subsample(50)

        self.folder_icon=PhotoImage(
            file=f"{dirname(__file__)}/folder.gif",
            master=self.dialog
        ).subsample(15)
        
        self.disk_icon=PhotoImage(
            file=f"{dirname(__file__)}/disk.gif",
            master=self.dialog
        ).subsample(15)

        if self.icon:
            self.dialog.iconbitmap(self.icon)
        else:
            self.dialog.iconbitmap(f"{dirname(__file__)}/icon.ico")
        
        # Widgets:
        self.paneview = PanedWindow(
            self.dialog,
            sashwidth=7,
            bg="#cccccc",
            bd=0,
        )

        self.left_pane = PanedWindow(self.paneview)
        self.right_pane = PanedWindow(self.paneview)
        self.paneview.add(self.left_pane)
        self.paneview.add(self.right_pane)

        self.treeview_x_scrollbar=Scrollbar(self.left_pane, orient="horizontal")
        self.treeview_y_scrollbar=Scrollbar(self.left_pane, orient="vertical")
        self.list_box_x_scrollbar=Scrollbar(self.right_pane, orient="horizontal")
        self.list_box_y_scrollbar=Scrollbar(self.right_pane, orient="vertical")
        
        # tstyle = Style().configure(".", )

        self.treeview=Treeview(
            self.left_pane,
            xscrollcommand=self.treeview_x_scrollbar.set,
            yscrollcommand=self.treeview_y_scrollbar.set,
            show="tree",
            selectmode="browse",
            # style=tstyle
        )


        self.list_box=Listbox(
            self.right_pane,
            xscrollcommand=self.list_box_x_scrollbar.set,
            yscrollcommand=self.list_box_y_scrollbar.set,
            width=34,
            highlightthickness=0,
            bd=2,
            relief="ridge"
        )

        if self.multiselect:
            self.list_box.config(selectmode="extended")
        else:
            self.list_box.config(selectmode="browse")

        self.cancel_button = Button(
            self.left_pane,
            text="Cancel",
            command=self.cancel
        )

        self.submit_button = Button(
            self.right_pane,
            text="Submit",
            command=self.submit
        )

        self.treeview_x_scrollbar.config(command=self.treeview.xview)
        self.treeview_y_scrollbar.config(command=self.treeview.yview)
        self.list_box_x_scrollbar.config(command=self.list_box.xview)
        self.list_box_y_scrollbar.config(command=self.list_box.yview)
        
        #Layout:
        self.dialog.rowconfigure(0, weight=1)
        self.dialog.columnconfigure(0, weight=1)

        self.left_pane.grid_rowconfigure(0, weight=1)
        self.left_pane.grid_columnconfigure(0, weight=1)
        self.right_pane.grid_rowconfigure(0, weight=1)
        self.right_pane.grid_columnconfigure(0, weight=1)

        self.paneview.paneconfigure(
            self.left_pane,
            minsize=100,
            #Start off w/ the sash centered in the GUI:
            width=(self.dialog.winfo_width() / 2) - 
            ceil((self.paneview.cget("sashwidth") * 1.5)),
        )
        self.paneview.paneconfigure(self.right_pane, minsize=100)

        self.paneview.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.treeview.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.treeview_y_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        self.treeview_x_scrollbar.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.list_box.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.list_box_y_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        self.list_box_x_scrollbar.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.cancel_button.grid(
            row=2,
            column=0,
            sticky="w",
            padx=10, 
            pady=10
        )
        self.submit_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="e",
            padx=10,
            pady=10
        )
        
        #Bindings, Protocols, & Misc:
        self.dialog.bind("<Control-w>", self.cancel)
        self.treeview.bind("<<TreeviewSelect>>", self.treeview_select)
        self.treeview.bind("<Double-Button-1>", self.dialog_populate)
        self.treeview.bind("<Return>", self.dialog_populate)
        self.treeview.bind("<Right>", self.dialog_populate)
        self.list_box.bind("<<ListboxSelect>>", self.list_box_select)
        self.list_box.bind("<Return>", self.submit)
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)

        self.dialog_selection = deque()
        self.selection_paths = deque()

        for disk in self.get_disks():
            self.treeview.insert(
                "",
                index="end",
                text=disk,
                image=self.disk_icon,
            )

        self.dialog.focus()


    def __call__(self):
        """
            Display dialog & return selection
        """

        (width_offset, height_offset)=self.get_offset(self.dialog)
        self.dialog.geometry(f"+{width_offset}+{height_offset}")
        self.dialog.update_idletasks()
        self.dialog.deiconify()

        self.dialog.wait_window()

        for i, path in enumerate(self.dialog_selection):
            if self.unix_delimiter:
                self.dialog_selection[i] = sub("\\\\", "/", path)
            else:
                self.dialog_selection[i] = sub("/", "\\\\", path)


        if self.stdout:
            [print(item) for item in self.dialog_selection]

        return list(self.dialog_selection)


    def __str__(self):
        """
            Return own address
        """

        return "Universal File Dialog"\
        f" @ {hex(id(self))}"


    def __repr__(self):
        """
            Return full string representation of constructor signature
        """

        return f"Ufd("\
        f"title=\"{self.title}\","\
        f" icon=\"{self.icon}\","\
        f" show_hidden={self.show_hidden},"\
        f" include_files={self.include_files},"\
        f" multiselect={self.multiselect},"\
        f" select_dirs={self.select_dirs},"\
        f" select_files={self.select_files},"\
        f" unix_delimiter={self.unix_delimiter})"\
        f" stdout={self.stdout})"\
        f" @ {hex(id(self))}"


    @staticmethod
    def get_offset(tk_window):
        """
            Returns an appropriate offset for a given tkinter toplevel,
            such that it always is created center screen on the primary display.
        """

        width_offset = int(
            (tk_window.winfo_screenwidth() / 2) - (tk_window.winfo_width() / 2)
        )

        height_offset = int(
            (tk_window.winfo_screenheight() / 2) - (tk_window.winfo_height() / 2)
        )

        return (width_offset, height_offset)


    @staticmethod
    def get_disks():
        """
            Returns all mounted disks (for Windows)

            >> ["A:", "B:", "C:"]
        """

        if system() != "Windows":
            raise OSError("For use with Windows platforms.")

        logicaldisks=run(
            ["wmic", "logicaldisk", "get", "name"],
            capture_output=True
        )

        return findall("[A-Z]:", str(logicaldisks.stdout))


    @staticmethod
    def list_dir(path, force=False):
        """
            Reads a directory with a shell call to dir.
            Truthiness of bool force determines whether 
            hidden items are returned or not. (For Windows)
        """

        path = sub("/", "\\\\", path)

        if force:
            dir_listing=run([
                "dir",
                path,
                "/b",
                "/a"
            ], shell=True, capture_output=True)

        else:
            dir_listing=run([
                "dir",
                path,
                "/b"
            ], shell=True, capture_output=True)

        output=dir_listing.stdout
        err=dir_listing.stderr

        if not output:
            return []

        if err:
            err=err.decode("utf-8")
            raise Exception(err)

        str_output=output.decode("utf-8")
        list_output=re_split("\r\n", str_output)
        
        return sorted([item for item in list_output if item])


    def climb(self, item):
        """
            Builds & returns a complete path to root directory,
            including the item name itself as the path tail.
            An extra delimiter is appeneded for the subsequent
            child node, which is normalized in dialog_populate()
        """
        
        item_text = self.treeview.item(item)["text"]
        parent = self.treeview.parent(item)
        path = ""
        parents = deque()

        while parent:
            parents.append(self.treeview.item(parent)["text"] + "/")
            parent = self.treeview.parent(parent)

        for parent in reversed(parents):
            path += parent

        path += item_text + "/"
        return path


    def dialog_populate(self, event=None):
        """
            Dynamically populates & updates the treeview, listbox,
            and keeps track of the full paths corresponding to each
            item in the listbox
        """
        if not self.treeview.focus():
            return

        self.treeview.column("#0", width=1000)

        existing_children = self.treeview.get_children(self.treeview.focus())
        [self.treeview.delete(child) for child in existing_children]

        self.list_box.delete(0, "end")
        self.selection_paths.clear()

        focus_item = self.treeview.focus()
        path = self.climb(focus_item)

        if self.show_hidden:
            children = self.list_dir(path, force=True)
        else:
            children = self.list_dir(path)

        for child in children:
            if isdir(path+child):

                self.treeview.insert(
                    focus_item,
                    index="end",
                    text=child,
                    image=self.folder_icon
                )

                if self.select_dirs:
                    self.list_box.insert("end", child)
                    self.selection_paths.append(path+child)

            elif isfile(path+child):

                if self.include_files:
                    self.treeview.insert(
                        focus_item,
                        index="end",
                        text=child,
                        image=self.file_icon
                    )

                if self.select_files:
                    self.list_box.insert("end", child)
                    self.list_box.itemconfig("end", {"bg":"#EAEAEA"})
                    self.selection_paths.append(path+child)

        if isfile(normpath(path)):
            (head, tail) = path_split(normpath(path))
            head = sub("\\\\", "/", head)
            
            self.list_box.insert("end", tail)
            self.selection_paths.append(head + "/" + tail)
            self.list_box.itemconfig("end", {"bg":"#EAEAEA"})


    def list_box_select(self, event=None):
        """
            Dynamically refresh the dialog selection with
            what's selected in the listbox
            (Callback for <<ListboxSelect>>).
        """

        self.dialog_selection.clear()
        
        for i in self.list_box.curselection():
            self.dialog_selection.append(self.selection_paths[i])


    def treeview_select(self, event=None):
        """
            Dynamically refresh the dialog selection with
            what's selected in the treeview
            (Callback for <<TreeviewSelect>>).
        """

        for i in self.list_box.curselection():
            self.list_box.selection_clear(i)

        self.dialog_selection.clear()

        item = normpath(self.climb(self.treeview.focus()))
        self.dialog_selection.append(item)


    def submit(self, event=None):
        """
            Satisfies wait_window() in self.__call__() and validates selection

            (Callback for <Return>, <Button-1> on file_list, submit_button)
        """

        if self.select_dirs == False:
            for item in self.dialog_selection:
                if isdir(item):
                    messagebox.showwarning(
                        "Error - Invalid Selection",
                        "Unable to select directory. Please select a file(s)."
                    )
                    return

        if self.select_files == False:
            for item in self.dialog_selection:
                if isfile(item):
                    messagebox.showwarning(
                        "Error - Invalid Selection",
                        "Unable to select file. Please select a folder(s)"
                    )
                    return
        
        self.dialog.destroy()


    def cancel(self, event=None):
        """
            Satisfies wait_window() in self.__call__() 

            (Callback for <Button-1> on cancel_button)
            (Callback for protocol "WM_DELETE_WINDOW" on self.dialog)
        """

        self.dialog_selection.clear()
        self.dialog.destroy()
