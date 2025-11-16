class Formatter:
    def format(self, lineno, snapshot, iteration):
        """
        lineno : 실행된 라인 번호
        snapshot : observer.capture()가 반환한 dict
        차후 renderer와 통합하거나 renderer를 조정할 수 있도록 수정 예정
        """

        # 첫 줄: [line N]
        lines = [f"[line {lineno}] #Loop-{iteration}"]

        # 두 번째 줄부터: 2칸 들여쓰기 + key : value
        for var, val in snapshot.items():
            lines.append(f"  {var} : {val}")

        # 문자열로 합쳐서 반환
        return "\n".join(lines)
