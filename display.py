import tkinter as tk
from collection import Collection
from youtube_transcripts import *

_FONT_BASIC = ("Helvetica", "12")
_FONT_CURRENT = ("Helvetica","10", "bold")
_FONT_LARGE = ("Helvetica", "12" , "bold")

class Display:
    def __init__(self, master):
        self.master = master
        self.master.resizable(False,False)
        self.master.title("Youtube Transcript Scraper")
        self.master["bg"] = "dark slate blue"

        self.lbl_title = tk.Label(self.master, text = "Youtube Transcript Scraper", font = _FONT_BASIC, bg = "firebrick3")
        self.lbl_title.grid(row = 0, column = 0, sticky = "ew", columnspan = 12)

        self.collection = Collection(self)

        self.scrlcol_links = ScrollCollection(self.master, self)

        self.lbl_collection = tk.Label(self.master, text = "Collection", font = _FONT_LARGE, bg = "slate blue", relief = "solid", borderwidth = 2)
        self.lbl_collection.grid( row = 1, column = 0, columnspan = 2, sticky = "ew")



        self.lbl_data = tk.Label(self.master, text = "Data", font = _FONT_LARGE, bg = "slate blue", relief = "solid", borderwidth = 2)
        self.lbl_data.grid(row = 1, column = 2, columnspan = 10, sticky = "ew")

        self.frm_data = tk.Frame(self.master,  bg = "dark slate blue")
        self.frm_data.grid(row = 2, column = 3, sticky = "n")

        self.lbl_collection_info= tk.Label(self.frm_data, text = "Collection Info   ", bg = "dark slate blue", font = _FONT_BASIC, relief = "solid")
        self.lbl_collection_info.grid(row = 0, column = 0, sticky = "nw")

        self.lbl_docs= tk.Label(self.frm_data, text = "Docs in collection: 0 ", bg = "slate blue", font = _FONT_BASIC, relief = "solid")
        self.lbl_docs.grid(row = 0, column = 1, sticky = "nw")

        self.lbl_avg_len= tk.Label(self.frm_data, text = "Avg Doc Length: 0 ", bg = "slate blue", font = _FONT_BASIC, relief = "solid")
        self.lbl_avg_len.grid(row = 0, column = 2, sticky = "nw")

        self.ent_search = tk.Entry(self.frm_data)
        self.ent_search.grid(row = 1, column = 0,sticky = "w", columnspan = 3)

        self.btn_search = tk.Button(self.frm_data, text = "Search & Retrieve Transripts", bg = "green", font = _FONT_LARGE, command = lambda: self.search_for_transcripts())
        self.btn_search.grid(row = 1, column = 1, sticky = "ew", columnspan = 2)

        self.lbl_query = tk.Label(self.frm_data, text = "Query", bg = "slate blue", font = _FONT_LARGE)
        self.lbl_query.grid(row = 2, column = 0, sticky = "ew")
        self.ent_query = tk.Entry(self.frm_data)
        self.ent_query.grid(row = 2, column = 1,sticky = "ew")

        self.btn_get_basic_data = tk.Button(self.frm_data, text = "Get DocFreq, Term Freq, and Total Occurences", bg = "green", command = lambda: self.get_basic_query_data())
        self.btn_get_basic_data.grid(row = 3, column = 0, sticky = "ew", columnspan = 2)

        self.btn_get_PNScore = tk.Button(self.frm_data, text = "Get PN Score", bg = "green", command = lambda: self.get_pn_score())
        self.btn_get_PNScore.grid(row = 4, column = 0, sticky = "ew", columnspan = 2)

        self.btn_get_Similarity = tk.Button(self.frm_data, text = "Get Similarity Score", bg = "green", command = lambda: self.get_similarity_score())
        self.btn_get_Similarity.grid(row = 5, column = 0, sticky = "ew", columnspan = 2)

        self.btn_get_PNScore = tk.Button(self.frm_data, text = "Get Okapi Score", bg = "green", command = lambda: self.get_okapi_score())
        self.btn_get_PNScore.grid(row = 6, column = 0, sticky = "ew", columnspan = 2)





        self.btn_get_collection = tk.Button(self.master, text = "Initialize The Collection", font = _FONT_BASIC, bg = "slate blue", command = lambda: self.scrlcol_links.update())
        self.btn_get_collection.grid(row = 3, column = 0, sticky = "ew")
        self.btn_delete_collection = tk.Button(self.master, text = "Delete Collection", font = _FONT_BASIC, bg = "red", command = lambda: self.scrlcol_links.remove_buttons())
        self.btn_delete_collection.grid(row = 3, column = 1, sticky = "ew")
        self.btn_clear_active = tk.Button(self.master, text = "Clear Active Document", font = _FONT_BASIC, bg = "red", command = lambda: self.update_current_label("None"))
        self.btn_clear_active.grid(row = 5, column = 0, sticky = "ew", columnspan = 2)

        self.lbl_current = tk.Label(self.master, text = "Active Document: None", font = _FONT_CURRENT, bg = "dark slate blue")
        self.current = ""
        self.lbl_current.grid(row = 4, column = 0, columnspan = 2, sticky = "w")

        #console widget
        self.lbl_console = tk.Label(self.master, text = "Console Window", bg = "dark slate blue", font = _FONT_LARGE)
        self.lbl_console.grid(row = 6, column = 0, columnspan = 12)
        self.scrl_console_y = tk.Scrollbar(self.master)
        self.scrl_console_y.grid(row = 7, column = 11, rowspan = 4, sticky = "nse")
        self.text_console = tk.Text(self.master, bg = "black", fg = "white", yscrollcommand  = self.scrl_console_y.set)
        self.text_console.config(state = "disabled")
        self.text_console.grid(row = 8, column = 0, columnspan = 11, sticky = "ew")
        self.scrl_console_y.config(command = self.text_console.yview)
        self.btn_console_clear = tk.Button(self.master, text = "clear console", bg = "firebrick3", font = _FONT_LARGE, command = lambda: self.clear_console())
        self.btn_console_clear.grid(row = 9, column = 0, columnspan = 12, sticky = "ew")

    def get_basic_query_data(self):
        qf = self.collection.getQueryFreq(self.ent_query.get().lower())
        self.update_console(f"Getting Query Frequency for query: {self.ent_query.get()}", color = "cyan")
        for key in qf.keys():
            self.update_console(f"{key}:{qf[key]}")

        qt = self.collection.getQueryTotalOccur(self.ent_query.get().lower())
        self.update_console(f"Getting Query Total for query: {self.ent_query.get()}", color = "cyan")
        for key in qt.keys():
            self.update_console(f"{key}:{qt[key]}")

    def get_pn_score(self):
        if self.current != "None":
            self.update_console(f"Getting PN Scores for the document [{self.current}] in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            pn_score = self.collection.getPNScore(self.current, self.ent_query.get().lower())
            self.update_console(f"{self.ent_query.get()}:{pn_score}")
        else:
            self.update_console(f"Getting PN Scores for all documents in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            pn_scores = self.collection.getPNScores(self.ent_query.get().lower())
            pn_scores = dict(sorted(pn_scores.items(), key=lambda item: item[1]))
            for key in pn_scores.keys():
                self.update_console(f"{key}:{pn_scores[key]}", color = "green" if pn_scores[key] > 0 else "snow")

    def get_okapi_score(self):
        if self.current != "None":
            self.update_console(f"Getting Okapi Scores for the document [{self.current}] in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            okapi_score = self.collection.getOkapiScore(self.current, self.ent_query.get().lower())
            self.update_console(f"{self.ent_query.get()}:{okapi_score}")
        else:
            self.update_console(f"Getting Okapi Scores for all documents in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            okapi_scores = self.collection.getOkapiScores(self.ent_query.get().lower())
            okapi_scores = dict(sorted(okapi_scores.items(), key=lambda item: item[1]))
            for key in okapi_scores.keys():
                self.update_console(f"{key}:{okapi_scores[key]}", color = "green" if okapi_scores[key] > 0 else "snow")

    def get_similarity_score(self):
        if self.current != "None":
            self.update_console(f"Getting PN Scores for the document [{self.current}] in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            s_score = self.collection.getDocSimilarity(self.current, self.ent_query.get().lower())
            self.update_console(f"{self.ent_query.get()}:{s_score}")
        else:
            self.update_console(f"Getting PN Scores for all documents in collection for the query:", color = "green")
            self.update_console(f"{self.ent_query.get()}")
            s_scores = self.collection.getCollectionSimilarity(self.ent_query.get().lower())
            s_scores = dict(sorted(s_scores.items(), key=lambda item: item[1]))
            for key in s_scores.keys():
                self.update_console(f"{key}:{s_scores[key]}", color = "green" if s_scores[key] > 0 else "snow")

    def update_current_label(self, current):
        self.current = current
        self.lbl_current["text"] = f"Active Document: {self.current}"
        self.update_console(f"Setting Active Document: {self.current}", color = "cyan")

    def search_for_transcripts(self):
        query = self.ent_search.get()
        self.update_console(f"Searching for youtube videos by query: {query}")
        vs = VideosSearch(query,10)
        res = format_results(vs,query)
        aquired = create_transcripts(res, parent = self)
        self.update_console(f"Completed Transcript retrieval, retrieved: {aquired} transcripts")
        self.scrlcol_links.update()

    def update_console(self,message,color = "snow"):
        """
        updates the console window with message in the specified color
        Arguements:
        message: string - representing message displayed to the console
        color: string - color the text will be displayed in
        returns: nothing
        """
        self.text_console.config(state = "normal")
        self.text_console.tag_config(color, foreground = color)
        self.text_console.insert(tk.END, message + "\n", color)
        self.text_console.config(state = "disabled")
        self.text_console.see(tk.END)


    def update_data(self):
        self.lbl_docs["text"] = f"Docs in collection: {self.collection.doc_num} "
        self.lbl_avg_len["text"] = f"Avg Doc Length: {self.collection.avg_doc_len} "

    def clear_console(self):
        """
        Clears the console window
        returns: nothing
        """
        self.text_console.config(state = "normal")
        self.text_console.delete("1.0", tk.END)
        self.text_console.config(state = "disabled")

class ScrollCollection:
    def __init__(self,parent, parent_class):
        self.parent = parent
        self.parent_class = parent_class
        self.canvas = tk.Canvas(parent,bg = "black", width = 800)
        self.scroll_y = tk.Scrollbar(parent, orient = "vertical", command = self.canvas.yview)
        self.frame = tk.Frame(self.canvas, bg = "black")
        self.frame.grid(row = 0, column = 0, sticky = "nsew")
        self.setup_frame()

    def setup_frame(self):
        self.canvas.create_window(0,0, anchor = "nw", window = self.frame)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion = self.canvas.bbox("all"),yscrollcommand = self.scroll_y.set)
        self.canvas.grid(row = 2, column = 0, sticky = "ew", columnspan = 2)
        self.scroll_y.grid(row = 2, column = 1, sticky = "nse")

    def add_buttons(self,buttons):
        row = 0
        for button in buttons:
            tk.Button(self.frame, text = button, command = lambda x=button: self.parent_class.update_current_label(x)).grid(row = row, column = 0, sticky = "w")
            row += 1

    def remove_buttons(self):
        self.parent_class.update_console("Clearing Collection")
        self.parent_class.update_current_label("None")
        for child in self.frame.winfo_children():
            child.destroy()

    def update(self):
        self.parent_class.update_console("Showing Collection")
        self.parent_class.collection.setup()
        self.parent_class.update_data()
        self.remove_buttons()
        self.add_buttons(self.parent_class.collection.collection.keys())
        self.setup_frame()

root = tk.Tk()
display = Display(root)
root.mainloop()
