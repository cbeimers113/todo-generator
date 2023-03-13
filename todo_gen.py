import os
from time import time

try:
    import tkinter as tk
    from tkinter import filedialog, ttk
except ModuleNotFoundError:
    import sys
    print('Missing dependencies: tkinter')
    print('Please see the following page for installation instructions:')
    print('https://bobbyhadz.com/blog/python-no-module-named-tkinter')
    sys.exit(1)


def get_proj_path() -> None:
    """Open a directory browser to get the source root."""
    directory = filedialog.askdirectory()
    proj_path.set(directory if len(directory) else proj_path.get())


def get_out_path() -> None:
    """Open a directory browser to get the output folder."""
    directory = filedialog.askdirectory()
    out_path.set(os.path.join(directory, 'TODO.txt') if len(directory) else out_path.get())


def generate_notes() -> None:
    """Generate the todo notes from the source folder."""
    todo_notes: list[str] = []
    todo_file = out_path.get()
    search_str = search_key.get()
    start_time = time()
    txt_notes.configure(state='normal')
    txt_notes.delete(1.0, tk.END)

    for root, _, files in os.walk(proj_path.get()):
        for src_file in files:
            file_path = os.path.join(root, src_file)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    line = f.readline()
                    line_num = 1

                    while line:
                        if search_str in line:
                            substring_start: int = line.index(
                                search_str) + len(search_str)
                            note: str = line[substring_start:]
                            todo_notes.append(f'{file_path} ({line_num}): {note}')

                        line = f.readline()
                        line_num += 1
            except:
                continue

    # If we found some notes, print them both to gui and the disk
    if len(todo_notes):
        with open(todo_file, 'w', encoding='utf-8') as f:
            def out(msg: str):
                """Output msg to both the gui and the disk."""
                # Shorten file paths for gui 
                txt_notes.insert('end', msg.replace(proj_path.get(), '$PROJ') + '\n')
                f.write(msg + '\n')

            out('List of tasks to do:\n')

            for note in sorted(todo_notes):
                out(note)

        print()

    # If there are no TODO notes found, remove any existing previous output
    elif os.path.exists(todo_file):
        os.remove(todo_file)

    end_time = time()
    txt_notes.insert('end', f'\nDone in {round(end_time - start_time, 5)}ms')
    txt_notes.configure(state='disabled')


# Window configuration
window = tk.Tk()
window.geometry('550x550')
window.resizable(False, False)
window.title('TODO Gen')

# Some variables
cont_root_path = tk.Frame(window)
cont_out_path = tk.Frame(window)
cont_search_key = tk.Frame(window)
proj_path = tk.StringVar()
proj_path.set(os.getcwd())
out_path = tk.StringVar()
out_path.set(os.path.join(os.getcwd(), 'TODO.txt'))
search_key = tk.StringVar()
search_key.set('TODO:')

pad_x = 5
pad_y = 5

# Build root path frame
tk.Label(text='Project root path:').pack(in_=cont_root_path, padx=pad_x, pady=pad_y, side='left')
tk.Entry(textvariable=proj_path, width=35).pack(in_=cont_root_path, padx=pad_x, pady=pad_y, side='left')
tk.Button(text='Browse', command=get_proj_path).pack(in_=cont_root_path, padx=pad_x, pady=pad_y, side='right')
cont_root_path.pack()

tk.Label(text='Write to file:').pack(in_=cont_out_path, padx=pad_x, pady=pad_y, side='left')
tk.Entry(textvariable=out_path, width=40).pack(in_=cont_out_path, padx=pad_x, pady=pad_y, side='left')
tk.Button(text='Browse', command=get_out_path).pack(in_=cont_out_path, padx=pad_x, pady=pad_y, side='right')
cont_out_path.pack()

tk.Label(text='TODO Style:').pack(in_=cont_search_key, padx=pad_x, pady=pad_y, side='left')
tk.Entry(textvariable=search_key, width=10).pack(in_=cont_search_key, padx=pad_x, pady=pad_y, side='right')
cont_search_key.pack()

tk.Button(text='Generate', command=generate_notes).pack(padx=pad_x, pady=pad_y)
ttk.Separator(window, orient='horizontal').pack(fill='x', padx=pad_x, pady=pad_y)
txt_notes = tk.Text(state='disabled', wrap=tk.WORD)
txt_notes.pack(padx=pad_x, pady=pad_y)

window.mainloop()
