class NoteBlock:
    """ノーツブロック情報を保存するクラス
    Attributes:
        tick: 位置するtick
        key: キー(range is 0-87, 33-57 is within the 2-octave limit.)
        layer: 所属するレイヤー番号
        inst: 楽器ID(range is 0-15)
        panning: 左右の角度(0: 2ブロック右, 100: 中央, 200: 2ブロック左)
        pitch: ピッチ(default:0, 100ごとに1オクターブ)
        volume: ボリューム
    """    
    def __init__(self, tick, layer, inst, key, velocity, panning, pitch):
        self.tick = tick
        self.layer = layer
        self.inst = inst
        self.key = key
        self.volume = velocity
        self.panning = panning
        self.pitch = pitch