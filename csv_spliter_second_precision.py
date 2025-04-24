import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def filter_csv_by_time(file_path, start_time_str, end_time_str, time_column):
    try:
        df = pd.read_csv(file_path)

        if time_column not in df.columns:
            messagebox.showerror("Error", f"'{time_column}' column not found in the CSV.")
            return

        # Convert to datetime
        df[time_column] = pd.to_datetime(df[time_column])

        # Parse input times
        start_time = pd.to_datetime(start_time_str)
        end_time = pd.to_datetime(end_time_str)

        # Filter rows
        filtered_df = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)]

        # Ask where to save
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            filtered_df.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"Filtered CSV saved successfully with {len(filtered_df)} rows.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def browse_and_split():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    start_time = start_entry.get()
    end_time = end_entry.get()
    time_column = time_col_entry.get()

    if not start_time or not end_time or not time_column:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    filter_csv_by_time(file_path, start_time, end_time, time_column)

# GUI setup
root = tk.Tk()
root.title("CSV Time Range Splitter")
root.geometry("450x250")

tk.Label(root, text="Start Time (YYYY-MM-DD HH:MM:SS)").pack(pady=5)
start_entry = tk.Entry(root, width=40)
start_entry.pack()

tk.Label(root, text="End Time (YYYY-MM-DD HH:MM:SS)").pack(pady=5)
end_entry = tk.Entry(root, width=40)
end_entry.pack()

tk.Label(root, text="Time Column Name (e.g., systemTime)").pack(pady=5)
time_col_entry = tk.Entry(root, width=40)
time_col_entry.pack()

tk.Button(root, text="Browse CSV & Split", command=browse_and_split, width=30).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy, width=30).pack()

root.mainloop()
