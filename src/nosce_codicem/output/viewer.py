import sys
import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from collections import defaultdict

console = Console()


# -------------------------------------------------------
# 공통 유틸
# -------------------------------------------------------
def print_header():
    console.print(
        Panel.fit(
            Text("Nosce Codicem – Trace Viewer", style="bold cyan"),
            border_style="bright_blue",
        )
    )


def fmt_val(v, width=5):
    """
    값의 길이가 달라도 고정 폭으로 변환해주는 함수.
    None → 공백, 숫자/문자 → 가운데 정렬
    """
    text = "" if v is None else str(v)
    return f"{text:^{width}}"


# -------------------------------------------------------
# Loop renderer (표 형식)
# -------------------------------------------------------
def render_loop(records):

    console.rule("[bold cyan]Loop Trace[/bold cyan]")

    # 1) 루프별 묶기
    grouped = defaultdict(list)
    for rec in records:
        grouped[rec["iteration"]].append(rec)

    # iteration 순서대로 출력
    for iteration in sorted(grouped.keys()):
        recs = grouped[iteration]

        console.print(Panel(f"Loop #{iteration}", style="bold magenta"))

        # 2) 테이블 구성
        table = Table(box=box.ROUNDED, border_style="bright_blue")

        # line 번호 추가
        table.add_column("line", justify="center", style="cyan", no_wrap=True)

        # 변수 이름들 (정렬)
        var_names = list(recs[0]["variables"].keys())

        for var in var_names:
            table.add_column(var, justify="center")

        # 3) 각 row 추가
        for rec in recs:
            lineno = str(rec["lineno"])
            row = [lineno]

            for var in var_names:
                val = rec["variables"].get(var)
                row.append(fmt_val(val, 5))

            table.add_row(*row)

        console.print(table)
        time.sleep(0.05)

    console.input("\nPress Enter to exit...")


# -------------------------------------------------------
# 다른 구문은 자리만
# -------------------------------------------------------
def render_condition(data):
    console.print("[yellow]Condition trace not implemented yet.[/]")
    console.input("\nPress Enter to exit...")


def render_recursion(data):
    console.print("[magenta]Recursion trace not implemented yet.[/]")
    console.input("\nPress Enter to exit...")


# -------------------------------------------------------
# main
# -------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: viewer.py <type> <json>")
        sys.exit(1)

    dtype = sys.argv[1]
    raw = sys.argv[2]

    data = json.loads(raw)

    if dtype == "loop":
        render_loop(data)

    elif dtype == "condition":
        render_condition(data)

    elif dtype == "recursion":
        render_recursion(data)

    else:
        print(f"Unknown type: {dtype}")
        console.input("\nPress Enter to exit...")
