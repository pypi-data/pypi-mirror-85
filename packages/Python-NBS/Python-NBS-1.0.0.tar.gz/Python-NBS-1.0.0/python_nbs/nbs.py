
'''NBSファイルを読み込むライブラリ
'''
import io
from . import binary, NoteBlock, Instrument, Layer


class NBS:
    """NBSを管理するクラス
    Attributes:
        version: NBSフォーマットのバージョン
        insts: バニラの楽器の数
        length: 曲の長さ(tick)
        layers: レイヤーの数
        song_name: 曲の名称
        song_author: NBSファイルの作者
        song_original_author: オリジナルの作曲者
        song_description: 曲の詳細
        song_tempo: 曲のテンポ(ticks per second)
        auto_saving: 自動保存を有効にするか(1: 有効)
        auto_saving_duration: 自動保存の間隔(秒)
        time_signature: 曲の拍子記号(4分の何拍子か, default:4, range is 2-8)
        minutes_spent: 曲の編集に費やした時間(分)
        left_cliks: ユーザーが左クリックした回数
        right_cliks: ユーザーが右クリックした回数
        note_blocks_added: ノーツブロックが追加された回数
        note_blocks_removed: ノーツブロックが削除された回数
        midi_file_name: 元となったMIDIファイル名
        loop: ループするか(0=off,1=on)
        max_loop_count: 最大ループ数
        loop_start_tick: ループが開始されるtick
        note_blocks: 曲に含まれるNoteBlockのリスト
        layer_info: 曲に含まれるLayerのリスト
    """    
    def __init__(self, path: str):
        """初期化

        Args:
            path (str): NBSファイルパス
        """        
        br = binary.File(path, endian=binary.LE)
        # 1: ヘッダー
        # 最初の2バイトは0
        br.read_short()
        self.version = br.read_byte() 
        self.insts = br.read_byte()
        self.length = br.read_short()
        self.layers = br.read_short()
        self.song_name = self.nbs_read_string(br)
        self.song_author = self.nbs_read_string(br)
        self.song_original_author = self.nbs_read_string(br)
        self.song_description = self.nbs_read_string(br)
        self.song_tempo = br.read_short()
        self.auto_saving = br.read_byte()
        self.auto_saving_duration = br.read_byte()
        self.time_signature = br.read_byte()
        self.minutes_spent = br.read_int()
        self.left_clicks = br.read_int()
        self.right_clicks = br.read_int()
        self.note_blocks_added = br.read_int()
        self.note_blocks_removed = br.read_int()
        self.midi_file_name = self.nbs_read_string(br)
        self.loop = br.read_byte()
        self.max_loop_count = br.read_byte()
        self.loop_start_tick = br.read_short()

        # 2: noteblocks
        self.note_blocks = []
        self.layer_count = [0] * self.layers

        tick = -1
        jumps = 0
        while(True):
            jumps = br.read_short()
            if(jumps == 0):
                break
            tick += jumps
            layer = -1
            while(True):
                jumps = br.read_short()
                if(jumps == 0):
                    break
                layer += jumps
                inst = br.read_byte()
                key = br.read_byte()
                velocity = br.read_byte()
                panning = br.read_byte()
                pitch = br.read_short()
                self.note_blocks.append(NoteBlock.NoteBlock(
                    tick, layer, inst, key, velocity, panning, pitch
                ))
                if(layer < self.layers):
                    self.layer_count[layer] += 1

        # 3: layer info
        self.layer_infos = []
        for i in range(self.layers):
            name = self.nbs_read_string(br)
            lock = br.read_byte()
            volume = br.read_byte()
            stereo = br.read_byte()
            self.layer_infos.append(Layer.Layer(name, lock, volume, stereo))

        br.close()

    def nbs_read_string(self, br: binary.File):
        length = br.read_int()
        return br.read_text(length)
