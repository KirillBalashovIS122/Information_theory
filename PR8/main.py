from tkinter import Tk, Frame, Radiobutton, Button, Label, filedialog, messagebox
from entropy import encode_file, decode_file, calculate_compression_ratio

class HuffmanApp:
    """GUI приложение для кодирования и декодирования файлов с использованием алгоритма Хаффмана."""

    def __init__(self, main_window):
        """Конструктор приложения.

        Args:
            main_window (Tk): Главное окно приложения.
        """
        self.main_window = main_window
        self.main_window.title("Huffman Encoder/Decoder")
        self.main_window.bind('<Escape>', lambda e: self.main_window.quit())

        self.operation_mode = "encode"  # Устанавливаем значение по умолчанию

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        control_frame = Frame(self.main_window)
        control_frame.pack(pady=20)

        Radiobutton(control_frame, text="Encode", variable=self.operation_mode,
                    value="encode").pack(side="left", padx=5)
        Radiobutton(control_frame, text="Decode", variable=self.operation_mode,
                    value="decode").pack(side="left", padx=5)

        self.action_button = Button(self.main_window, text="Start", command=self.execute_action)
        self.action_button.pack(pady=15)

        self.status_label = Label(self.main_window, text="", justify="left", wraplength=400)
        self.status_label.pack(pady=10)

    def select_input_file(self):
        """Выбор файла для обработки."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        return file_path

    def select_output_file(self):
        """Выбор файла для сохранения результата."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        return file_path

    def execute_action(self):
        """Выполнение выбранного действия (кодирование или декодирование)."""
        if self.operation_mode == "encode":
            self.encode_file()
        else:
            self.decode_file()

    def encode_file(self):
        """Кодирование файла с использованием алгоритма Хаффмана."""
        input_file_path = self.select_input_file()
        if not input_file_path:
            return
        output_file_path = self.select_output_file()
        if not output_file_path:
            return
        try:
            original_size, encoded_size, entropy, bits_per_symbol = encode_file(input_file_path, output_file_path)
            compression_ratio = calculate_compression_ratio(original_size, encoded_size)

            result_message = (
                f"Encoding complete!\n"
                f"Original size: {original_size} bytes\n"
                f"Encoded size: {encoded_size} bytes\n"
                f"Entropy: {entropy:.4f} bits/symbol\n"
                f"Average bits per symbol: {bits_per_symbol:.4f}\n"
                f"Compression ratio: {compression_ratio:.4f}\n"
            )
            self.status_label.config(text=result_message)
            messagebox.showinfo("Encoding Result", result_message)
        except (OSError, IOError) as e:
            messagebox.showerror("File Error", f"An error occurred while processing the files: {e}")
        except ValueError as e:
            messagebox.showerror("Value Error", f"An error occurred with the values provided: {e}")

    def decode_file(self):
        """Декодирование файла, закодированного с использованием алгоритма Хаффмана."""
        input_file_path = self.select_input_file()
        if not input_file_path:
            return
        output_file_path = self.select_output_file()
        if not output_file_path:
            return
        try:
            encoded_size, decoded_size = decode_file(input_file_path, output_file_path)
            result_message = (
                f"Decoding complete!\n"
                f"Encoded size: {encoded_size} bytes\n"
                f"Decoded size: {decoded_size} bytes\n"
            )
            self.status_label.config(text=result_message)
            messagebox.showinfo("Decoding Result", result_message)
        except (OSError, IOError) as e:
            messagebox.showerror("File Error", f"An error occurred while processing the files: {e}")
        except ValueError as e:
            messagebox.showerror("Value Error", f"An error occurred with the values provided: {e}")

if __name__ == "__main__":
    root = Tk()
    app = HuffmanApp(root)
    root.mainloop()
