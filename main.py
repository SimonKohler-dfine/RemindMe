import tkinter as tk

class RemindMeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("RemindMe - Counter")
        self.root.geometry("400x200")

        # 1. State: track the number of clicks
        self.counter: int = 0

        # 2. UI Elements
        self.label = tk.Label(
            self.root,
            text="Button clicked 0 times",
            font=("Arial", 14)
        )
        self.label.pack(pady=20)

        # The 'command' argument binds the button event to our callback method
        self.button = tk.Button(
            self.root,
            text="Click Me!",
            command=self._on_button_click,
            font=("Arial", 12)
        )
        self.button.pack(pady=10)

    def _on_button_click(self) -> None:
        """Callback method triggered every time the button is pressed."""
        self.counter += 1
        # Update the UI element property dynamically
        self.label.config(text=f"Button clicked {self.counter} times")


def main() -> None:
    root = tk.Tk()
    app = RemindMeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()