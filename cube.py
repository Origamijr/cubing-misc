import itertools, copy
import random

class Cube3:

    class Piece:
        def __init__(self, tiles:list[str], faces: list[str]):
            assert len(tiles) == len(faces)
            self.tiles = {}
            for face in "UDFBRL":
                self.tiles[face] = tiles[faces.index(face)] if face in faces else None
        def __getitem__(self, key) -> str:
            return self.tiles[key]
        def __contains__(self, item) -> bool:
            return self.tiles[item] is not None
        def __repr__(self) -> str:
            return repr({f:c for f,c in self.tiles.items() if c})
        def position(self, orientation=None):
            return Cube3.order_faces(''.join([f for f,c in self.tiles.items() if c]), orientation)
        def colors(self, orientation=None):
            return Cube3.order_color(''.join([c for c in self.tiles.values() if c]), orientation)
        def rotate(self, face):
            if face in 'xyz':
                match face:
                    case 'x': self.tiles['U'], self.tiles['B'], self.tiles['D'], self.tiles['F'] = self.tiles['F'], self.tiles['U'], self.tiles['B'], self.tiles['D']
                    case 'y': self.tiles['F'], self.tiles['R'], self.tiles['B'], self.tiles['L'] = self.tiles['R'], self.tiles['B'], self.tiles['L'], self.tiles['F']
                    case 'z': self.tiles['U'], self.tiles['R'], self.tiles['D'], self.tiles['L'] = self.tiles['L'], self.tiles['U'], self.tiles['R'], self.tiles['D']
                return self
            if self[face] is None: return self
            match face:
                case 'U': self.tiles['F'], self.tiles['R'], self.tiles['B'], self.tiles['L'] = self.tiles['R'], self.tiles['B'], self.tiles['L'], self.tiles['F']
                case 'D': self.tiles['F'], self.tiles['R'], self.tiles['B'], self.tiles['L'] = self.tiles['L'], self.tiles['F'], self.tiles['R'], self.tiles['B']
                case 'F': self.tiles['U'], self.tiles['R'], self.tiles['D'], self.tiles['L'] = self.tiles['L'], self.tiles['U'], self.tiles['R'], self.tiles['D']
                case 'B': self.tiles['U'], self.tiles['R'], self.tiles['D'], self.tiles['L'] = self.tiles['R'], self.tiles['D'], self.tiles['L'], self.tiles['U']
                case 'R': self.tiles['U'], self.tiles['B'], self.tiles['D'], self.tiles['F'] = self.tiles['F'], self.tiles['U'], self.tiles['B'], self.tiles['D']
                case 'L': self.tiles['U'], self.tiles['B'], self.tiles['D'], self.tiles['F'] = self.tiles['B'], self.tiles['D'], self.tiles['F'], self.tiles['U']
                case _: return self
            return self

    def __init__(self):
        self.COLORS = ['W', 'G', 'R', 'Y', 'B', 'O']
        self.FACES = ['U', 'F', 'R', 'D', 'B', 'L']

        self.pieces: dict[str,Cube3.Piece] = {}
        for i in range(6):
            p = Cube3.Piece([self.COLORS[i]], [self.FACES[i]])
            self.pieces[self.COLORS[i]] = p
        for i, j in itertools.combinations(range(6), 2):
            if j-i==3: continue
            p = Cube3.Piece([self.COLORS[i],self.COLORS[j]], [self.FACES[i],self.FACES[j]])
            self.pieces[self.order_color(f'{self.COLORS[i]}{self.COLORS[j]}')] = p
        for i, j, k in itertools.combinations(range(6), 3):
            if j-i==3 or k-j==3 or k-i==3: continue
            p = Cube3.Piece([self.COLORS[i],self.COLORS[j],self.COLORS[k]], [self.FACES[i],self.FACES[j],self.FACES[k]])
            self.pieces[self.order_color(f'{self.COLORS[i]}{self.COLORS[j]}{self.COLORS[k]}')] = p

    def __repr__(self) -> str:
        p = self
        s = ""
        s += f"    {p['UBL']['U']}{p['UB']['U']}{p['UBR']['U']}\n"
        s += f"    { p['UL']['U']}{ p['U']['U']}{ p['UR']['U']}\n"
        s += f"    {p['UFL']['U']}{p['UF']['U']}{p['UFR']['U']}\n"
        s += f"{p['UBL']['L']}{p['UL']['L']}{p['UFL']['L']} {p['UFL']['F']}{p['UF']['F']}{p['UFR']['F']} {p['UFR']['R']}{p['UR']['R']}{p['UBR']['R']} {p['UBR']['B']}{p['UB']['B']}{p['UBL']['B']}\n"
        s += f"{ p['BL']['L']}{ p['L']['L']}{ p['FL']['L']} { p['FL']['F']}{ p['F']['F']}{ p['FR']['F']} { p['FR']['R']}{ p['R']['R']}{ p['BR']['R']} { p['BR']['B']}{ p['B']['B']}{ p['BL']['B']}\n"
        s += f"{p['DBL']['L']}{p['DL']['L']}{p['DFL']['L']} {p['DFL']['F']}{p['DF']['F']}{p['DFR']['F']} {p['DFR']['R']}{p['DR']['R']}{p['DBR']['R']} {p['DBR']['B']}{p['DB']['B']}{p['DBL']['B']}\n"
        s += f"    {p['DFL']['D']}{p['DF']['D']}{p['DFR']['D']}\n"
        s += f"    { p['DL']['D']}{ p['D']['D']}{ p['DR']['D']}\n"
        s += f"    {p['DBL']['D']}{p['DB']['D']}{p['DBR']['D']}"
        return s
    def __str__(self) -> str:
        return repr(self).replace(' ', '').replace('\n', '')

    @staticmethod
    def order_color(s, orientation=None):
        return ''.join(sorted(s, key=lambda c: (c!=orientation,"WYGBRO".index(c))))
    @staticmethod
    def order_faces(s, orientation=None):
        return ''.join(sorted(s, key=lambda f: (f!=orientation,"UDFBRL".index(f))))
    
    def __getitem__(self, key):
        return {self.order_faces(''.join([t for t in p.tiles if p[t]])): p for p in self.pieces.values()}[self.order_faces(key)]
    
    def get_face(self, f):
        c = self.rotate({'U': "x'", 'D': "x", 'R': "y", 'L': "y'", 'B': "y2", 'F': ""}[f], in_place=False)
        face = [[c['UFL'],c['UF'],c['UFR']],[c['FL'],c['F'],c['FR']],[c['DFL'],c['DF'],c['DFR']]]
        c.execute({'U': "x'", 'D': "x", 'R': "y", 'L': "y'", 'B': "y2", 'F': ""}[f], in_place=True, inverse=True)
        return face

    def is_solved(self):
        for face in self.FACES:
            pieces = [p for p in self.pieces.values() if p[face]]
            color = pieces[0].tiles[face]
            for piece in pieces[1:]:
                if color != piece.tiles[face]: return False
        return True
    
    def rotate(self, rotation, in_place=False) -> 'Cube3':
        cube = self if in_place else copy.deepcopy(self)
        if '2' in rotation:
            return cube.rotate(rotation[0], in_place).rotate(rotation[0], in_place)
        if "'" in rotation:
            return cube.rotate(rotation[0], in_place).rotate(rotation[0], in_place).rotate(rotation[0], in_place)
        if rotation.islower() and rotation in (''.join(self.FACES)).lower():
            return cube.rotate(rotation.upper, in_place).rotate({
                'u': "E'", 'd': "E", 'r': "M'", 'l': "M", 'f': "S", 'b': "S'"
            }[rotation], in_place)
        match rotation:
            case 'M': return cube.rotate("r'", in_place).rotate('R', in_place)
            case 'E': return cube.rotate("u'", in_place).rotate('U', in_place)
            case 'S': return cube.rotate('f', in_place).rotate("F'", in_place)
            case _:
                for p in cube.pieces.values(): p.rotate(rotation)
        return cube

    def execute(self, rotations, in_place=False, inverse=False):
        cube = self
        for rotation in rotations.strip().split(' ')[::-1 if inverse else 1]:
            if not rotation: continue # idk why this is necessary, but without it it breaks
            if inverse: rotation = rotation[:-1] if rotation[-1]=="'" else f"{rotation}'"
            cube = cube.rotate(rotation, in_place=in_place)
        return cube
    
    def scramble(self, seed=None): # Naive scramble for now
        if seed: random.seed(seed)
        scramble_rotations = ''
        last_letter = None
        for i in range(20):
            scramble_rotations += (last_letter := random.choice([move for move in 'UDFBRL' if move != last_letter]))
            scramble_rotations += random.choice(["", "2", "'"]) + ' '
        scramble_rotations = scramble_rotations.strip()
        self.execute(scramble_rotations, in_place=True)
        return self, scramble_rotations
