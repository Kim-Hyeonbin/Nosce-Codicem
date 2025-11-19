import json
import sys
import subprocess
import os
import tempfile
from pathlib import Path


class Renderer:
    """
    LoopHandler에서 finalize() 호출 시,
    records를 JSON 파일로 저장해두고,
    viewer.py를 새 CMD 창에서 실행
    """

    def __init__(self, viewer_path=None):
        if viewer_path is None:
            base_dir = Path(__file__).resolve().parent
            self.viewer_path = str(base_dir / "viewer.py")
        else:
            self.viewer_path = viewer_path

    def __call__(self, records, dtype="loop"):

        # JSON을 임시파일에 저장
        tmp = tempfile.NamedTemporaryFile(
            delete=False, suffix=".json", mode="w", encoding="utf-8"
        )
        json.dump(records, tmp)
        tmp.close()

        data_path = tmp.name  # 이 경로만 viewer.py로 전달

        # viewer 명령 구성
        cmd = [sys.executable, "-u", self.viewer_path, dtype, data_path]

        # Windows에서 새 콘솔 열기 옵션
        creationflags = 0
        if os.name == "nt" and hasattr(subprocess, "CREATE_NEW_CONSOLE"):
            creationflags = subprocess.CREATE_NEW_CONSOLE

        # 실행
        subprocess.Popen(cmd, creationflags=creationflags)
