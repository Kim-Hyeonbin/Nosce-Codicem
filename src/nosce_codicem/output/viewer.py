import traceback
import sys
import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


# -------------------------------------------------------
# 값 truncate (A 방식)
# -------------------------------------------------------
def truncate(v, width=9):
    s = str(v)
    return s if len(s) <= width else (s[: width - 1] + "…")


# -------------------------------------------------------
# 변수 추적 전용 테이블
# -------------------------------------------------------
def render_variable_table(recs):
    table = Table(box=box.ROUNDED, border_style="bright_blue")

    table.add_column("line", justify="center", style="cyan", no_wrap=True, min_width=3)

    var_names = list(recs[0]["variables"].keys())
    for name in var_names:
        # 폭 고정
        table.add_column(
            name, justify="center", min_width=12, max_width=12, no_wrap=False
        )

    for idx_rec, rec in enumerate(recs):
        row = [str(rec["lineno"])]
        for name in var_names:
            val = rec["variables"].get(name)
            row.append("" if val is None else truncate(val, width=9))

        table.add_row(*row)

        if idx_rec != len(recs) - 1:
            sep = []
            sep.append("[dim cyan]" + "─" * 12 + "[/dim cyan]")
            for name in var_names:
                sep.append("[dim cyan]" + "─" * 12 + "[/dim cyan]")
            table.add_row(*sep)

    console.print(table)


# -------------------------------------------------------
# 리스트 변수 전용 테이블
# -------------------------------------------------------
def render_list_table(list_name, recs, chunk_size=10):
    """
    리스트 테이블을 chunk_size 열씩 분할하여
    여러 개의 작은 테이블로 출력한다.
    """

    # 가장 긴 리스트 길이
    max_len = 0
    for rec in recs:
        lst = rec["variables"].get(list_name, [])
        if isinstance(lst, list):
            max_len = max(max_len, len(lst))

    indices = list(range(max_len))

    # 열을 chunk_size 단위로 나누는 헬퍼
    def chunked(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    tables = []

    # 각 청크에 대해 테이블 생성
    for chunk in chunked(indices, chunk_size):
        table = Table(box=box.ROUNDED, border_style="bright_blue")
        table.add_column(
            "line", justify="center", style="cyan", no_wrap=True, min_width=3
        )

        # 인덱스 컬럼 추가
        for idx in chunk:
            label = f"[{idx}]"
            table.add_column(
                label, justify="center", min_width=5, max_width=5, no_wrap=False
            )

        # 값 채우기
        for idx_rec, rec in enumerate(recs):
            row = [str(rec["lineno"])]
            full_list = rec["variables"].get(list_name)

            if not isinstance(full_list, list):
                full_list = []

            for idx in chunk:
                if idx < len(full_list):
                    row.append(truncate(full_list[idx], width=4))
                else:
                    row.append("")

            table.add_row(*row)

            # separator
            if idx_rec != len(recs) - 1:
                sep = ["[dim cyan]" + "─" * 3 + "[/dim cyan]"]
                for _ in chunk:
                    sep.append("[dim cyan]" + "─" * 5 + "[/dim cyan]")
                table.add_row(*sep)

        tables.append(table)

    return tables


# -------------------------------------------------------
# Loop 전체 렌더링
# -------------------------------------------------------
def render_loop(records):
    console.rule("[bold cyan]Loop Trace[/bold cyan]")

    grouped = {}
    for rec in records:
        grouped.setdefault(rec["iteration"], []).append(rec)

    for iteration in sorted(grouped.keys()):
        recs = grouped[iteration]

        console.print(Panel(f"Loop #{iteration}", style="bold magenta", expand=False))
        console.print()

        first_snapshot = recs[0]["variables"]
        is_list_mode = any(isinstance(v, list) for v in first_snapshot.values())

        if not is_list_mode:
            render_variable_table(recs)
            console.print("\n " + ("─" * (console.width - 2)) + " \n")
            continue

        for name in first_snapshot.keys():
            console.print(f"[ {name} ]", style="bold green")
            tables = render_list_table(name, recs)
            for t in tables:
                console.print(t)
            console.print("\n " + ("─" * (console.width - 2)) + " \n")

    console.input("\nPress Enter to exit...")


# -------------------------------------------------------
#  Recursion (아직 미구현)
# -------------------------------------------------------


def render_recursion(data):
    console.print("[magenta]Recursion trace not implemented yet.[/]")
    console.input("\nPress Enter to exit...")


# -------------------------------------------------------
# CLI
# -------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: viewer.py <type> <path_to_json>")
        sys.exit(1)

    dtype = sys.argv[1]
    path = sys.argv[2]

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if dtype == "loop":
        render_loop(data)
    elif dtype == "recursion":
        render_recursion(data)
    else:
        print(f"Unknown type: {dtype}")
        console.input("\nPress Enter to exit...")
