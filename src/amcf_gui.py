"""Small Windows-friendly AMCF workflow UI.

This UI is intentionally a workflow launcher rather than a claim of a
manufactured player or a physical reader.  The console CLI remains the
normative interface; this window makes the common local actions discoverable.
"""

from __future__ import annotations

import io
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from contextlib import redirect_stdout

from amcf_cli import main as cli_main


class AmcfApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AMCF Workflow")
        self.geometry("800x680")
        self.minsize(720, 560)
        self.mode = tk.StringVar(value="Validate seeded 4K AMCF")
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.project_root = tk.StringVar(value=str(self._default_project_root()))
        self.render_video = tk.BooleanVar(value=False)
        self._build()

    @staticmethod
    def _default_project_root() -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parents[1]

    def _build(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="AMCF Workflow", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(root, text="Digital AMCF tools and virtual physical-path preparation", foreground="#555").pack(anchor="w", pady=(0, 14))

        form = ttk.LabelFrame(root, text="Operation", padding=10)
        form.pack(fill="x")
        ttk.Label(form, text="Action").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        choices = [
            "Validate seeded 4K AMCF",
            "Decode AMCF archive to video",
            "Encode source video to AMCF",
            "Render diagnostics (03M zone + 08E heat)",
            "Create physical print plan",
            "Run physical software adapter layer",
            "Check dependencies",
            "Prepare deep dependencies",
            "Download HOOT proof dataset",
        ]
        box = ttk.Combobox(form, textvariable=self.mode, values=choices, state="readonly", width=38)
        box.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)
        ttk.Label(form, text="Input archive/video").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.input_path).grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(form, text="Browse", command=self._browse_input).grid(row=1, column=2, padx=(8, 0), pady=4)
        ttk.Label(form, text="Output folder").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.output_path).grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Button(form, text="Browse", command=self._browse_output).grid(row=2, column=2, padx=(8, 0), pady=4)
        ttk.Label(form, text="Project / bundle root").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(form, textvariable=self.project_root).grid(row=3, column=1, sticky="ew", pady=4)
        ttk.Button(form, text="Browse", command=self._browse_project_root).grid(row=3, column=2, padx=(8, 0), pady=4)
        ttk.Checkbutton(form, text="Render a review MP4 when validating the seeded profile", variable=self.render_video).grid(row=4, column=1, columnspan=2, sticky="w", pady=4)
        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(root)
        buttons.pack(fill="x", pady=12)
        ttk.Button(buttons, text="Run", command=self._run).pack(side="left")
        ttk.Button(buttons, text="CLI status", command=self._status).pack(side="left", padx=8)
        ttk.Button(buttons, text="Clear log", command=self._clear).pack(side="right")

        log_frame = ttk.LabelFrame(root, text="Result", padding=8)
        log_frame.pack(fill="both", expand=True)
        self.log = tk.Text(log_frame, wrap="word", state="disabled", font=("Consolas", 9))
        self.log.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        scrollbar.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=scrollbar.set)

    def _browse_input(self) -> None:
        mode = self.mode.get()
        if mode in {"Encode source video to AMCF", "Render diagnostics (03M zone + 08E heat)"}:
            path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.mov *.avi"), ("All files", "*.*")])
        else:
            path = filedialog.askopenfilename(filetypes=[("AMCF archives", "*.amcf.zip *.zip"), ("All files", "*.*")])
        if path:
            self.input_path.set(path)

    def _browse_output(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def _browse_project_root(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.project_root.set(path)

    def _append(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _clear(self) -> None:
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _status(self) -> None:
        self._run_cli(["status"])

    def _run(self) -> None:
        mode = self.mode.get()
        input_path = Path(self.input_path.get().strip())
        output_path = Path(self.output_path.get().strip())
        input_required = mode in {
            "Validate seeded 4K AMCF",
            "Decode AMCF archive to video",
            "Encode source video to AMCF",
            "Render diagnostics (03M zone + 08E heat)",
            "Create physical print plan",
        }
        if input_required and not input_path.exists():
            messagebox.showerror("AMCF", "Choose an existing input file first.")
            return
        if not self.output_path.get().strip():
            messagebox.showerror("AMCF", "Choose an output folder first.")
            return
        if mode == "Validate seeded 4K AMCF":
            args = ["seeded-materializer", "--input-archive", str(input_path), "--output", str(output_path)]
            if self.render_video.get():
                args.append("--render-video")
        elif mode == "Decode AMCF archive to video":
            args = ["decode", "--input", str(input_path), "--output", str(output_path), "--video"]
        elif mode == "Encode source video to AMCF":
            args = ["encode", "--input-video", str(input_path), "--output", str(output_path)]
        elif mode == "Render diagnostics (03M zone + 08E heat)":
            args = ["diagnostics", "--input-video", str(input_path), "--output", str(output_path)]
        elif mode == "Create physical print plan":
            args = ["print-plan", "--input", str(input_path), "--output", str(output_path)]
        elif mode == "Run physical software adapter layer":
            args = ["adapter-roundtrip", "--project-root", self.project_root.get(), "--output", str(output_path)]
        elif mode == "Check dependencies":
            args = [
                "setup",
                "--check",
                "--project-root",
                self.project_root.get(),
                "--report-output",
                str(output_path / "setup_report.json"),
            ]
        elif mode == "Prepare deep dependencies":
            if not messagebox.askyesno(
                "AMCF dependency setup",
                "Install the pinned deep packages, clone SAMURAI/CoTracker, and download declared checkpoints?\n\nReview upstream licences first.",
            ):
                return
            args = [
                "setup",
                "--install-deep",
                "--accept-upstream-licenses",
                "--accept-noncommercial",
                "--project-root",
                self.project_root.get(),
                "--report-output",
                str(output_path / "setup_report.json"),
            ]
        else:
            if not messagebox.askyesno("AMCF HOOT setup", "Download the optional HOOT potted_plant/008 proof dataset after accepting its terms?"):
                return
            args = [
                "setup",
                "--download-hoot",
                "--accept-hoot-terms",
                "--project-root",
                self.project_root.get(),
                "--report-output",
                str(output_path / "setup_report.json"),
            ]
        self._run_cli(args)

    def _run_cli(self, args: list[str]) -> None:
        self._append(f"> amcf {' '.join(args)}")
        stream = io.StringIO()
        try:
            with redirect_stdout(stream):
                code = cli_main(args)
            self._append(stream.getvalue().strip() or f"completed with exit code {code}")
            if code:
                messagebox.showerror("AMCF", f"The operation failed with exit code {code}.")
        except Exception as exc:  # noqa: BLE001 - display the actionable workflow error.
            self._append(f"ERROR: {exc}")
            messagebox.showerror("AMCF", str(exc))


def main() -> int:
    AmcfApp().mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

