import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_aab_file():
    file_path = filedialog.askopenfilename(filetypes=[("Android App Bundle", "*.aab")])
    if file_path:
        aab_file_var.set(file_path)

def select_keystore_file():
    file_path = filedialog.askopenfilename(filetypes=[("Keystore File", "*.jks")])
    if file_path:
        keystore_file_var.set(file_path)

def select_bundletool():
    file_path = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")])
    if file_path:
        bundletool_file_var.set(file_path)

def convert_to_apks():
    aab_file = aab_file_var.get()
    keystore_file = keystore_file_var.get()
    keystore_password = keystore_password_var.get()
    key_alias = key_alias_var.get()
    key_password = key_password_var.get()
    bundletool_file = bundletool_file_var.get()

    if not (aab_file and keystore_file and keystore_password and key_alias and key_password and bundletool_file):
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
    
    print(bundletool_file)

    output_file = os.path.splitext(aab_file)[0] + ".apks"
    cmd = [
        "java", "-jar", bundletool_file,
        "build-apks",
        "--mode=universal",
        f"--bundle={aab_file}",
        f"--output={output_file}",
        f"--ks={keystore_file}",
        f"--ks-pass=pass:{keystore_password}",
        f"--ks-key-alias={key_alias}",
        f"--key-pass=pass:{key_password}"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        messagebox.showinfo("Success", f"APKs file created: {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Conversion Error", e.stderr)

# Create the main window
root = tk.Tk()
root.title("AAB to APKs Converter")

# Create and set the GUI elements
aab_file_var = tk.StringVar()
keystore_file_var = tk.StringVar()
keystore_password_var = tk.StringVar()
key_alias_var = tk.StringVar()
key_password_var = tk.StringVar()
bundletool_file_var = tk.StringVar()

tk.Label(root, text="AAB File:").grid(row=0, column=0, sticky=tk.W)
tk.Entry(root, textvariable=aab_file_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_aab_file).grid(row=0, column=2)

tk.Label(root, text="Keystore File:").grid(row=1, column=0, sticky=tk.W)
tk.Entry(root, textvariable=keystore_file_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_keystore_file).grid(row=1, column=2)

tk.Label(root, text="Keystore Password:").grid(row=2, column=0, sticky=tk.W)
tk.Entry(root, textvariable=keystore_password_var, width=50).grid(row=2, column=1)

tk.Label(root, text="Key Alias:").grid(row=3, column=0, sticky=tk.W)
tk.Entry(root, textvariable=key_alias_var, width=50).grid(row=3, column=1)

tk.Label(root, text="Key Password:").grid(row=4, column=0, sticky=tk.W)
tk.Entry(root, textvariable=key_password_var, width=50).grid(row=4, column=1)

tk.Label(root, text="Bundletool JAR:").grid(row=5, column=0, sticky=tk.W)
tk.Entry(root, textvariable=bundletool_file_var, width=50).grid(row=5, column=1)
tk.Button(root, text="Browse", command=select_bundletool).grid(row=5, column=2)

tk.Button(root, text="Convert", command=convert_to_apks).grid(row=6, column=0, columnspan=3)

# Start the GUI event loop
root.mainloop()
