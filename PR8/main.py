import tkinter as tk
from tkinter import filedialog, messagebox
from PR8.entropy import encode_file, decode_file, calculate_compression_ratio

class HuffmanApp:
    """Графический интерфейс для кодирования и декодирования текстовых файлов методом Хаффмана."""

    def __init__(self, root_window):
        """Инициализация приложения.

        Args:
            root_window (tk.Tk): Корневое окно приложения.
        """
        self.root = root_window
        self.root.title("Huffman Encoding/Decoding")
        self.root.bind('<Escape>', lambda e: self.root.quit())

        self.mode = tk.StringVar(value="encode")
        self.create_widgets()

    def create_widgets(self):
        """Создание виджетов приложения."""
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Radiobutton(frame, text="Encode", variable=self.mode,
                       value="encode").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame, text="Decode", variable=self.mode,
                       value="decode").pack(side=tk.LEFT, padx=10)

        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute)
        self.execute_button.pack(pady=10)

        self.info_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.info_label.pack(pady=10)

    def browse_file(self):
        """Открытие диалогового окна для выбора файла."""
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        return filename

    def save_file(self):
        """Открытие диалогового окна для сохранения файла."""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        return filename

    def execute(self):
        """Выполнение операции кодирования или декодирования."""
        mode = self.mode.get()
        if mode == "encode":
            self.encode()
        else:
            self.decode()

    def encode(self):
        """Кодирование выбранного файла."""
        input_file = self.browse_file()
        if not input_file:
            return
        output_file = self.save_file()
        if not output_file:
            return
        try:
            original_size, encoded_size, entropy = encode_file(input_file, output_file)
            compression_ratio = calculate_compression_ratio(original_size, encoded_size)
            avg_bits_per_symbol = encoded_size * 8 / original_size

            result = f"""Encoding complete!
Original size: {original_size} bytes
Encoded size: {encoded_size} bytes
Entropy: {entropy:.4f} bits/symbol
Average bits per symbol: {avg_bits_per_symbol:.4f}
Compression ratio: {compression_ratio:.4f}
"""
            self.info_label.config(text=result)
            messagebox.showinfo("Encoding Result", result)
        except (OSError, IOError) as e:
            messagebox.showerror("File Error", f"An error occurred while processing the files: {e}")
        except ValueError as e:
            messagebox.showerror("Value Error", f"An error occurred with the values provided: {e}")

    def decode(self):
        """Декодирование выбранного файла."""
        input_file = self.browse_file()
        if not input_file:
            return
        output_file = self.save_file()
        if not output_file:
            return

        try:
            encoded_size, decoded_size = decode_file(input_file, output_file)
            result = f"""Decoding complete!
Encoded size: {encoded_size} bytes
Decoded size: {decoded_size} bytes
"""
            self.info_label.config(text=result)
            messagebox.showinfo("Decoding Result", result)
        except (OSError, IOError) as e:
            messagebox.showerror("File Error", f"An error occurred while processing the files: {e}")
        except ValueError as e:
            messagebox.showerror("Value Error", f"An error occurred with the values provided: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
