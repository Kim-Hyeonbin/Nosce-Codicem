import json
import sys
import subprocess
import os
from pathlib import Path


class Renderer:
    """
    LoopHandler에서 finalize() 호출 시,
    전체 records를 JSON으로 직렬화하여
    viewer.py를 독립 CMD 창에서 딱 1번 실행하는 Renderer.
    """

    def __init__(self, viewer_path=None):
        if viewer_path is None:
            # renderer.py 기준으로 같은 디렉토리에 있는 viewer.py를 찾도록
            base_dir = Path(__file__).resolve().parent
            self.viewer_path = str(base_dir / "viewer.py")
        else:
            self.viewer_path = viewer_path

    def __call__(self, records, dtype="loop"):
        data = json.dumps(records)

        cmd = [sys.executable, "-u", self.viewer_path, dtype, data]

        # 윈도우/기타 OS 모두 동작하도록 처리
        creationflags = 0
        if os.name == "nt" and hasattr(subprocess, "CREATE_NEW_CONSOLE"):
            creationflags = subprocess.CREATE_NEW_CONSOLE

        subprocess.Popen(cmd, creationflags=creationflags)
