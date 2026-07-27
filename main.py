import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Import the main functions from our testing module
from testing.smoke_step1_init import main as run_step1
from testing.smoke_step2_import import main as run_step2
from testing.smoke_step3_process import main as run_step3
from testing.smoke_step4_export import main as run_step4
from testing.smoke_step9_cleanup import main as run_step9


class RemindMeApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("RemindMe - ETL Controller & GUI")
        self.geometry("450x520")
        self.resizable(False, False)

        # Counter state
        self.click_count = 0

        self._build_ui()

    def _build_ui(self):
        # -------------------------------------------------------------
        # Section 1: Original Click Counter
        # -------------------------------------------------------------
        counter_frame = ttk.LabelFrame(self, text=" Click Counter ", padding=15)
        counter_frame.pack(fill="x", padx=15, pady=10)

        self.lbl_counter = ttk.Label(
            counter_frame,
            text="Clicks: 0",
            font=("Segoe UI", 12, "bold"),
        )
        self.lbl_counter.pack(pady=5)

        btn_counter = ttk.Button(
            counter_frame, text="Click Me!", command=self._increment_counter
        )
        btn_counter.pack(pady=5)

        # -------------------------------------------------------------
        # Section 2: Smoke Test Pipeline Controls
        # -------------------------------------------------------------
        etl_frame = ttk.LabelFrame(
            self, text=" Storage & ETL Operations ", padding=15
        )
        etl_frame.pack(fill="x", padx=15, pady=10)

        # Smoke Test Buttons
        ttk.Button(
            etl_frame,
            text="Step 1: Init Database Schema",
            command=lambda: self._execute_step("Step 1: Init DB", run_step1),
        ).pack(fill="x", pady=4)

        ttk.Button(
            etl_frame,
            text="Step 2: Import Sample Excel File",
            command=lambda: self._execute_step(
                "Step 2: Import Excel", run_step2
            ),
        ).pack(fill="x", pady=4)

        ttk.Button(
            etl_frame,
            text="Step 3: Process Staged Imports",
            command=lambda: self._execute_step(
                "Step 3: Process Data", run_step3
            ),
        ).pack(fill="x", pady=4)

        ttk.Button(
            etl_frame,
            text="Step 4: Export Tasks to Excel",
            command=lambda: self._execute_step(
                "Step 4: Export Excel", run_step4
            ),
        ).pack(fill="x", pady=4)

        ttk.Separator(etl_frame, orient="horizontal").pack(
            fill="x", pady=8
        )

        ttk.Button(
            etl_frame,
            text="Step 9: Reset & Delete Database",
            command=lambda: self._execute_step("Step 9: Cleanup", run_step9),
        ).pack(fill="x", pady=4)

        # -------------------------------------------------------------
        # Section 3: Status / Feedback Bar
        # -------------------------------------------------------------
        self.lbl_status = ttk.Label(
            self,
            text="Ready.",
            font=("Segoe UI", 9, "italic"),
            anchor="w",
            relief="sunken",
            padding=5,
        )
        self.lbl_status.pack(side="bottom", fill="x")

    def _increment_counter(self):
        """Increments the click counter."""
        self.click_count += 1
        self.lbl_counter.config(text=f"Clicks: {self.click_count}")

    def _execute_step(self, step_name: str, step_func):
        """Executes a smoke test function and displays status/error feedback."""
        try:
            step_func()
            self.lbl_status.config(
                text=f"Status: Executed {step_name} successfully."
            )
        except Exception as e:
            self.lbl_status.config(text=f"Status: Error in {step_name}.")
            messagebox.showerror(
                title=f"Error - {step_name}",
                message=f"Failed to execute {step_name}:\n\n{str(e)}",
            )


if __name__ == "__main__":
    app = RemindMeApp()
    app.mainloop()