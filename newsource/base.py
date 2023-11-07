class Base:
    def __init__(self, base, next_base):
        # 이름, 위치, 현재 주자가 있는지 여부
        self.base = base
        self.isFill = False
        self.next_base = next_base
