#!/usr/bin/env python3

"""
TASK MANAGER OFFLINE
====================

Server lokal untuk aplikasi Task Manager.

Teknologi:
- Python
- HTML
- CSS
- JSON

Tidak menggunakan Flask atau library pihak ketiga.

Jalankan:

    python task_manager.py

Kemudian buka:

    http://127.0.0.1:8000
"""

from __future__ import annotations

import json
import mimetypes
import os
import threading
import webbrowser

from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


# =========================================================
# KONFIGURASI
# =========================================================

HOST = "127.0.0.1"
PORT = 8000

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"

ALLOWED_PRIORITIES = {
    "Tinggi",
    "Sedang",
    "Rendah"
}

LOCK = threading.Lock()


# =========================================================
# LOAD DATA
# =========================================================

def read_tasks() -> list[dict]:
    """
    Membaca semua task dari tasks.json.
    Jika file belum ada atau rusak,
    aplikasi mengembalikan list kosong.
    """

    if not DATA_FILE.exists():
        return []

    try:
        with LOCK:
            with DATA_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

    except (
        OSError,
        json.JSONDecodeError
    ):
        return []

    if isinstance(data, list):
        return data

    return []


# =========================================================
# SAVE DATA
# =========================================================

def write_tasks(
    tasks: list[dict]
) -> None:
    """
    Menyimpan task ke tasks.json.
    Menggunakan file sementara agar
    risiko kerusakan file lebih kecil.
    """

    temp_file = DATA_FILE.with_suffix(".tmp")

    with LOCK:

        with temp_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                tasks,
                file,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temp_file,
            DATA_FILE
        )


# =========================================================
# PARSE REQUEST JSON
# =========================================================

def parse_body(
    handler: BaseHTTPRequestHandler
) -> dict:
    """
    Membaca JSON dari request HTTP.
    """

    try:

        length = int(
            handler.headers.get(
                "Content-Length",
                "0"
            )
        )

    except ValueError:

        length = 0


    if length <= 0:
        return {}


    raw = handler.rfile.read(
        length
    )


    try:

        value = json.loads(
            raw.decode("utf-8")
        )

    except (
        UnicodeDecodeError,
        json.JSONDecodeError
    ):

        return {}


    if isinstance(value, dict):
        return value

    return {}


# =========================================================
# VALIDASI TASK
# =========================================================

def clean_task(
    data: dict
) -> dict:
    """
    Membersihkan dan memvalidasi
    data task sebelum disimpan.
    """

    title = str(
        data.get("title", "")
    ).strip()


    category = str(
        data.get(
            "category",
            "Umum"
        )
    ).strip()


    priority = str(
        data.get(
            "priority",
            "Sedang"
        )
    ).strip()


    deadline = str(
        data.get(
            "deadline",
            ""
        )
    ).strip()


    time_value = str(
        data.get(
            "time",
            ""
        )
    ).strip()


    notes = str(
        data.get(
            "notes",
            ""
        )
    ).strip()


    if not category:
        category = "Umum"


    # Validasi nama task

    if not title:

        raise ValueError(
            "Nama task wajib diisi."
        )


    if len(title) > 100:

        raise ValueError(
            "Nama task maksimal 100 karakter."
        )


    # Validasi kategori

    if len(category) > 40:

        raise ValueError(
            "Kategori maksimal 40 karakter."
        )


    # Validasi catatan

    if len(notes) > 300:

        raise ValueError(
            "Catatan maksimal 300 karakter."
        )


    # Validasi prioritas

    if priority not in ALLOWED_PRIORITIES:

        raise ValueError(
            "Prioritas tidak valid."
        )


    # Validasi tanggal

    if deadline:

        try:

            datetime.strptime(
                deadline,
                "%Y-%m-%d"
            )

        except ValueError as exc:

            raise ValueError(
                "Format deadline harus YYYY-MM-DD."
            ) from exc


    # Validasi waktu

    if time_value:

        try:

            datetime.strptime(
                time_value,
                "%H:%M"
            )

        except ValueError as exc:

            raise ValueError(
                "Format waktu harus HH:MM."
            ) from exc


    return {
        "title": title,
        "category": category,
        "priority": priority,
        "deadline": deadline,
        "time": time_value,
        "notes": notes
    }


# =========================================================
# GENERATE ID
# =========================================================

def next_id(
    tasks: list[dict]
) -> int:

    ids = []

    for task in tasks:

        try:

            ids.append(
                int(
                    task.get(
                        "id",
                        0
                    )
                )
            )

        except (
            TypeError,
            ValueError
        ):

            continue


    return max(
        ids,
        default=0
    ) + 1


# =========================================================
# FIND TASK
# =========================================================

def find_task(
    tasks: list[dict],
    task_id: int
) -> dict | None:

    for task in tasks:

        try:

            if int(
                task.get("id")
            ) == task_id:

                return task

        except (
            TypeError,
            ValueError
        ):

            continue


    return None


# =========================================================
# HTTP HANDLER
# =========================================================

class Handler(
    BaseHTTPRequestHandler
):

    """
    Handler untuk website dan API.
    """

    server_version = "TaskManager/1.0"


    # -----------------------------------------------------
    # LOG SERVER
    # -----------------------------------------------------

    def log_message(
        self,
        format: str,
        *args
    ) -> None:

        print(
            f"[{self.log_date_time_string()}] "
            f"{format % args}"
        )


    # -----------------------------------------------------
    # RESPONSE JSON
    # -----------------------------------------------------

    def json_response(
        self,
        status: int,
        payload: dict
    ) -> None:

        body = json.dumps(
            payload,
            ensure_ascii=False
        ).encode("utf-8")


        self.send_response(
            status
        )


        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )


        self.send_header(
            "Content-Length",
            str(len(body))
        )


        self.send_header(
            "Cache-Control",
            "no-store"
        )


        self.end_headers()


        self.wfile.write(
            body
        )


    # -----------------------------------------------------
    # RESPONSE FILE
    # -----------------------------------------------------

    def file_response(
        self,
        path: Path
    ) -> None:

        if not path.is_file():

            self.send_error(
                404,
                "File tidak ditemukan"
            )

            return


        content_type = (
            mimetypes.guess_type(
                str(path)
            )[0]
            or
            "application/octet-stream"
        )


        body = path.read_bytes()


        self.send_response(
            200
        )


        self.send_header(
            "Content-Type",
            content_type
        )


        self.send_header(
            "Content-Length",
            str(len(body))
        )


        self.send_header(
            "Cache-Control",
            "no-cache"
        )


        self.end_headers()


        self.wfile.write(
            body
        )


    # =====================================================
    # GET
    # =====================================================

    def do_GET(self) -> None:

        path = urlparse(
            self.path
        ).path


        # Halaman utama

        if path == "/":

            self.file_response(
                BASE_DIR /
                "index.html"
            )

            return


        # CSS

        if path == "/style.css":

            self.file_response(
                BASE_DIR /
                "style.css"
            )

            return


        # API TASK

        if path == "/api/tasks":

            self.json_response(
                200,
                {
                    "tasks":
                        read_tasks()
                }
            )

            return


        self.send_error(
            404,
            "Endpoint tidak ditemukan"
        )


    # =====================================================
    # POST
    # =====================================================

    def do_POST(self) -> None:

        path = urlparse(
            self.path
        ).path


        payload = parse_body(
            self
        )


        tasks = read_tasks()


        try:

            # ------------------------------------------------
            # TAMBAH TASK
            # ------------------------------------------------

            if path == "/api/tasks":

                task_data = clean_task(
                    payload
                )


                now = (
                    datetime.now()
                    .timestamp()
                )


                task = {

                    "id":
                        next_id(tasks),

                    **task_data,

                    "completed":
                        False,

                    "createdAt":
                        now,

                    "updatedAt":
                        now

                }


                tasks.append(
                    task
                )


                write_tasks(
                    tasks
                )


                self.json_response(
                    201,
                    {
                        "task":
                            task
                    }
                )


                return


            # ------------------------------------------------
            # TOGGLE STATUS
            # ------------------------------------------------

            parts = (
                path
                .strip("/")
                .split("/")
            )


            if (

                len(parts) == 4

                and

                parts[0] == "api"

                and

                parts[1] == "tasks"

                and

                parts[3] == "toggle"

            ):

                task_id = int(
                    parts[2]
                )


                task = find_task(
                    tasks,
                    task_id
                )


                if task is None:

                    self.json_response(
                        404,
                        {
                            "error":
                                "Task tidak ditemukan."
                        }
                    )

                    return


                task[
                    "completed"
                ] = not bool(
                    task.get(
                        "completed",
                        False
                    )
                )


                task[
                    "updatedAt"
                ] = (
                    datetime.now()
                    .timestamp()
                )


                write_tasks(
                    tasks
                )


                self.json_response(
                    200,
                    {
                        "task":
                            task
                    }
                )


                return


        except (
            ValueError,
            TypeError
        ) as exc:

            self.json_response(
                400,
                {
                    "error":
                        str(exc)
                        or
                        "Data tidak valid."
                }
            )

            return


        self.json_response(
            404,
            {
                "error":
                    "Endpoint tidak ditemukan."
            }
        )


    # =====================================================
    # PUT
    # =====================================================

    def do_PUT(self) -> None:

        path = urlparse(
            self.path
        ).path


        payload = parse_body(
            self
        )


        parts = (
            path
            .strip("/")
            .split("/")
        )


        if (

            len(parts) != 3

            or

            parts[0] != "api"

            or

            parts[1] != "tasks"

        ):

            self.json_response(
                404,
                {
                    "error":
                        "Endpoint tidak ditemukan."
                }
            )

            return


        try:

            task_id = int(
                parts[2]
            )


            task_data = clean_task(
                payload
            )


        except (
            ValueError,
            TypeError
        ) as exc:

            self.json_response(
                400,
                {
                    "error":
                        str(exc)
                        or
                        "Data tidak valid."
                }
            )

            return


        tasks = read_tasks()


        task = find_task(
            tasks,
            task_id
        )


        if task is None:

            self.json_response(
                404,
                {
                    "error":
                        "Task tidak ditemukan."
                }
            )

            return


        task.update(
            task_data
        )


        task[
            "updatedAt"
        ] = (
            datetime.now()
            .timestamp()
        )


        write_tasks(
            tasks
        )


        self.json_response(
            200,
            {
                "task":
                    task
            }
        )


    # =====================================================
    # DELETE
    # =====================================================

    def do_DELETE(self) -> None:

        path = urlparse(
            self.path
        ).path


        # -------------------------------------------------
        # HAPUS TASK SELESAI
        # -------------------------------------------------

        if (
            path ==
            "/api/tasks/completed"
        ):

            tasks = read_tasks()


            remaining = [

                task

                for task in tasks

                if not bool(
                    task.get(
                        "completed",
                        False
                    )
                )

            ]


            removed = (
                len(tasks)
                -
                len(remaining)
            )


            write_tasks(
                remaining
            )


            self.json_response(
                200,
                {
                    "removed":
                        removed
                }
            )


            return


        # -------------------------------------------------
        # HAPUS BERDASARKAN ID
        # -------------------------------------------------

        parts = (
            path
            .strip("/")
            .split("/")
        )


        if (

            len(parts) != 3

            or

            parts[0] != "api"

            or

            parts[1] != "tasks"

        ):

            self.json_response(
                404,
                {
                    "error":
                        "Endpoint tidak ditemukan."
                }
            )

            return


        try:

            task_id = int(
                parts[2]
            )

        except ValueError:

            self.json_response(
                400,
                {
                    "error":
                        "ID task tidak valid."
                }
            )

            return


        tasks = read_tasks()


        remaining = [

            task

            for task in tasks

            if str(
                task.get("id")
            ) != str(task_id)

        ]


        if (
            len(remaining)
            ==
            len(tasks)
        ):

            self.json_response(
                404,
                {
                    "error":
                        "Task tidak ditemukan."
                }
            )

            return


        write_tasks(
            remaining
        )


        self.json_response(
            200,
            {
                "removed":
                    1
            }
        )


# =========================================================
# MAIN
# =========================================================

def main() -> None:

    server = (
        ThreadingHTTPServer(
            (
                HOST,
                PORT
            ),
            Handler
        )
    )


    url = (
        f"http://{HOST}:{PORT}"
    )


    print(
        "=" * 58
    )

    print(
        "  TASK MANAGER OFFLINE"
    )

    print(
        "=" * 58
    )

    print(
        f"  URL  : {url}"
    )

    print(
        f"  DATA : {DATA_FILE}"
    )

    print(
        "  Tutup dengan Ctrl+C"
    )

    print(
        "=" * 58
    )


    try:

        webbrowser.open(
            url
        )

    except Exception:

        pass


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nServer dihentikan."
        )

    finally:

        server.server_close()


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    main()