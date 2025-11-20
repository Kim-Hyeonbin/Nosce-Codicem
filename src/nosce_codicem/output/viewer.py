import sys
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box
from rich.rule import Rule
from rich.console import Group

console = Console()


# -------------------------------------------------------
# 값 truncate
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

    for iteration in grouped.keys():
        recs = grouped[iteration]

    # iteration 식별
    iterations = grouped.keys()

    for idx, iteration in enumerate(iterations):
        recs = grouped[iteration]
        is_last = idx == len(iterations) - 1

        # 마지막 루프에서 테이블 제목 수정
        title = "Result" if is_last else f"Loop #{iteration}"

        console.print(Panel(title, style="bold magenta", expand=False))
        console.print()

        # Result 출력 시 첫 행만 출력
        if is_last:
            recs = [recs[0]]

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
#  재귀 랜더링
# -------------------------------------------------------


#  재귀 트리 랜더링
def render_recursion_tree(records):
    console.rule("[bold magenta]Recursion Call Tree[/bold magenta]")
    console.print()

    if not records:
        console.print("[red]No recursion data.[/red]")
        console.input("\nPress Enter to exit...")
        return

    # call_id 기준으로 모든 레코드 그룹핑

    grouped = {}
    parent_map = {}
    func_name_map = {}
    depth_map = {}

    for rec in records:
        cid = rec.get("call_id")
        pid = rec.get("parent_id")
        if cid is None:
            continue

        grouped.setdefault(cid, []).append(rec)
        parent_map[cid] = pid
        func_name_map[cid] = rec.get("func_name")
        depth_map[cid] = rec.get("depth")

    # root call_id 찾기

    roots = [cid for cid, pid in parent_map.items() if pid is None]

    if not roots:
        console.print("[red]No root call found.[/red]")
        return

    root_id = roots[0]

    # 변수 패널
    def build_var_panel(call_id, events):
        rep = events[-1]
        vars_snapshot = rep.get("variables", {}) or {}

        parts = []
        for k in vars_snapshot.keys():
            v = vars_snapshot[k]
            parts.append(f"[cyan]{k}[/cyan]={v}")

        line = ", ".join(parts) if parts else "[dim]no variables[/dim]"
        header = f"[red]#{call_id}[/red]  {line}"

        return Panel(header, padding=(0, 1), border_style="green", expand=False)

    # 리스트 패널
    def build_list_panel(call_id, events):
        rep = events[-1]
        vars_snapshot = rep.get("variables", {}) or {}

        blocks = [f"[red]#{call_id}[/red]"]
        blocks.append(Rule(style="dim"))

        def summarize_list(lst):
            if len(lst) <= 20:
                return ", ".join(str(x) for x in lst)
            else:
                line_front = [str(lst[i]) for i in range(10)]
                line_back = [str(lst[i]) for i in range(-10, 0)]
            return ", ".join(line_front) + ", (...), " + ", ".join(line_back)

        for idx, k in enumerate(vars_snapshot.keys()):
            v = vars_snapshot[k]

            if isinstance(v, list):
                summary = summarize_list(v)
                blocks.append(f"{k}(length={len(v)}): {summary}")
                blocks.append(Rule(style="dim"))

        body = Group(*blocks)

        return Panel(body, padding=(0, 1), border_style="blue", expand=False)

    # 모드 분기 패널
    def build_panel(call_id, events):
        mode = events[0]["mode"]
        if mode == "list":
            return build_list_panel(call_id, events)
        else:
            return build_var_panel(call_id, events)

    # 트리 구성
    def build_tree(call_id, parent_node):
        label = f"{func_name_map[call_id]} [dim](depth={depth_map[call_id]})[/dim]"
        node = parent_node.add(label)

        # 이 call_id에 해당하는 이벤트 묶음
        events = grouped[call_id]

        # 모드에 따라 패널 자동 생성
        panel = build_panel(call_id, events)
        node.add(panel)

        # 자식 call_id 찾기
        children = [cid for cid, pid in parent_map.items() if pid == call_id]

        for child_id in children:
            build_tree(child_id, node)

    # 전체 트리 렌더링
    root_label = f"[bold]{func_name_map[root_id]}[/bold]  [dim](root)[/dim]"
    root = Tree(root_label)

    build_tree(root_id, root)

    console.print(root)


# 재귀 타임라인 랜더링
def render_recursion_timeline(records):
    console.print(Rule("[bold magenta]Recursion Timeline[/bold magenta]\n"))
    console.print()

    logical_depth = 0

    for rec in records:
        etype = rec.get("event_type")
        func_name = rec.get("func_name")
        call_id = rec.get("call_id")

        # CALL
        if etype == "call":
            indent = "    " * logical_depth
            console.print(f"{indent}→ call [red]#{call_id}[/red] {func_name}()")
            console.print()
            logical_depth += 1
            continue

        # RETURN
        if etype == "return":
            indent = "    " * logical_depth
            console.print(f"{indent}← return [red]#{call_id}[/red]")
            console.print()
            logical_depth -= 1
            continue


# 트리 + 타임라인 통합
def render_recursion(records):
    render_recursion_tree(records)
    console.print("\n\n")
    render_recursion_timeline(records)
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
