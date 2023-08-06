class Layer:
    """レイヤー情報を保存するクラス
    Attributes:
        name: レイヤーの名前
        lock: レイヤーがロックされているか(locked: 1)
        volume: レイヤーのボリューム(0-100)
        stereo: レイヤーの左右の角度(0: 2ブロック右, 100: 中央, 200: 2ブロック左)
    """    
    def __init__(self, name: str,lock: int, volume: int, stereo: int):
        self.name = name
        self.lock = lock
        self.volume = volume
        self.stereo = stereo
