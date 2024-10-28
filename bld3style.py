from cube import Cube3

"""
    AAB
    DWB
    DCC
EEF IIJ MMN QQR
HOF LGJ PRN TBR
HGG LKK POO TSS
    UUV
    XYV
    XWW
"""

SPEFFZ_CORNERS = {
    'A': 'UBL', 'B': 'UBR', 'C': 'UFR', 'D': 'UFL',
    'E': 'LUB', 'F': 'LUF', 'G': 'LDF', 'H': 'LDB',
    'I': 'FUL', 'J': 'FUR', 'K': 'FDR', 'L': 'FDL',
    'M': 'RUF', 'N': 'RUB', 'O': 'RDB', 'P': 'RDF',
    'Q': 'BUR', 'R': 'BUL', 'S': 'BDL', 'T': 'BDR',
    'U': 'DFL', 'V': 'DFR', 'W': 'DBR', 'X': 'DBL',
}
SPEFFZ_EDGES = {
    'A': 'UB', 'B': 'UR', 'C': 'UF', 'D': 'UL',
    'E': 'LU', 'F': 'LF', 'G': 'LD', 'H': 'LB',
    'I': 'FU', 'J': 'FR', 'K': 'FD', 'L': 'FL',
    'M': 'RU', 'N': 'RB', 'O': 'RD', 'P': 'RF',
    'Q': 'BU', 'R': 'BL', 'S': 'BD', 'T': 'BR',
    'U': 'DF', 'V': 'DR', 'W': 'DB', 'X': 'DL',
}

cube = Cube3()
SPEFFZ_CORNERS = {a: cube.order_faces(p, orientation=p[0]) for a, p in SPEFFZ_CORNERS.items()}
SPEFFZ_EDGES = {a: cube.order_faces(p, orientation=p[0]) for a, p in SPEFFZ_EDGES.items()}
SPEFFZ_CORNER_COLORS = {a: cube[p].colors(orientation=cube[p][p[0]]) for a, p in SPEFFZ_CORNERS.items()}
SPEFFZ_EDGE_COLORS = {a: cube[p].colors(orientation=cube[p][p[0]]) for a, p in SPEFFZ_EDGES.items()}
SPEFFZ_CORNERS_L = {p: a for a, p in SPEFFZ_CORNERS.items()}
SPEFFZ_EDGES_L = {p: a for a, p in SPEFFZ_EDGES.items()}
SPEFFZ_CORNER_COLORS_L = {c: a for a, c in SPEFFZ_CORNER_COLORS.items()}
SPEFFZ_EDGE_COLORS_L = {c: a for a, c in SPEFFZ_EDGE_COLORS.items()}

def move_piece(piece: Cube3.Piece, ref_orientation, dest):
    assert piece[ref_orientation] is not None
    target_color = piece[ref_orientation] # pick color at ref orientation, and find rotation that matches it to the destination
    for rotation in "x y y y x x x y y z y".split():
        if piece[dest[0]] == target_color: break
        piece = piece.rotate(rotation)
    while sorted(piece.position()) != sorted(dest): # match the rest of the colors
        piece = piece.rotate(dest[0])

def commute_pair(cube: Cube3, type, a, b, buffer='C', inverse=False):
    match type:
        case 'corner': lookup = SPEFFZ_CORNERS
        case _: lookup = SPEFFZ_EDGES
    a_pos = lookup[a]
    b_pos = lookup[b]
    buf_pos = lookup[buffer]
    a_piece = cube[a_pos]
    b_piece = cube[b_pos]
    buf_piece = cube[buf_pos]
    move_piece(a_piece, a_pos[0], buf_pos if inverse else b_pos)
    move_piece(b_piece, b_pos[0], a_pos if inverse else buf_pos)
    move_piece(buf_piece, buf_pos[0], b_pos if inverse else a_pos)
    return cube

def edge_corner_parity(cube: Cube3, corner_target, corner_buffer='C', edge_buffer='C', parity_buffer='B'):
    ctar_pos = SPEFFZ_CORNERS[corner_target]
    cbuf_pos = SPEFFZ_CORNERS[corner_buffer]
    ebuf_pos = SPEFFZ_EDGES[edge_buffer]
    pbuf_pos = SPEFFZ_EDGES[parity_buffer]
    ctar_piece = cube[ctar_pos]
    cbuf_piece = cube[cbuf_pos]
    ebuf_piece = cube[ebuf_pos]
    pbuf_piece = cube[pbuf_pos]
    move_piece(ctar_piece, ctar_pos[0], cbuf_pos)
    move_piece(cbuf_piece, cbuf_pos[0], ctar_pos)
    move_piece(ebuf_piece, ebuf_pos[0], pbuf_pos)
    move_piece(pbuf_piece, pbuf_pos[0], ebuf_pos)
    return cube

def execute_sequence(c, edge_sequence, corner_sequence, corner_buffer='C', edge_buffer='C', parity_buffer='B', inverse=False):
    functions = []
    def commute_wrapper(type, a, b, buffer, inverse):
        def f(c):
            return commute_pair(c, type, a, b, buffer=buffer, inverse=inverse)
        return f
    for pair in edge_sequence.split():
        functions.append(commute_wrapper('edge', pair[0], pair[1], buffer=edge_buffer, inverse=inverse))
    for pair in corner_sequence.split():
        if len(pair) == 1:
            functions.append(lambda c: edge_corner_parity(c, pair, corner_buffer=corner_buffer, edge_buffer=edge_buffer, parity_buffer=parity_buffer))
            continue
        functions.append(commute_wrapper('corner', pair[0], pair[1], buffer=edge_buffer, inverse=inverse))
    for f in functions[::-1 if inverse else 1]:
        c = f(c)
    return c

def _trace_helper(cube: Cube3, start, buffer_priority, position_lookup, letter_lookup, verbose=0):
    def invert_lookup(d, value):
        return next(k for k,v in d.items() if v==value)

    # Sequence the corner pieces
    letter_sequence = []
    twisted_positions = []
    unsolved_buffers = buffer_priority.copy()
    cycle = None
    curr_pos = position_lookup[start]
    while unsolved_buffers:
        if verbose: print('unchecked', unsolved_buffers, 'sequence', letter_sequence, 'twisted', twisted_positions, 'buffer', start)
        # If current piece is the buffer, find a new piece
        if sorted(cube[curr_pos].colors()) == sorted(invert_lookup(letter_lookup, start)):
            
            # complete the cycle
            #if cycle: letter_sequence.append(cycle)
            if cycle: 
                letter_sequence.append(letter_lookup[cube[curr_pos].colors(orientation=cube[curr_pos][curr_pos[0]])])
                unsolved_buffers.remove(cycle)
            cycle = None
            
            # Go through unsolved corners until a piece is in the wrong position
            while unsolved_buffers:
                curr_pos = unsolved_buffers[0]

                # check flip
                solved_colors = invert_lookup(letter_lookup, invert_lookup(position_lookup, curr_pos))
                correct_position = sorted(cube[curr_pos].colors()) == sorted(solved_colors)
                solved = cube[curr_pos][curr_pos[0]] == solved_colors[0]
                if not correct_position: break
                unsolved_buffers.pop(0)
                if not solved: twisted_positions.append(cube.order_faces(curr_pos))
            if not unsolved_buffers: break

            cycle = curr_pos
            letter_sequence.append(invert_lookup(position_lookup, curr_pos))
            start = letter_sequence[-1]

        # Iterate to the next piece
        curr_letter = letter_lookup[cube[curr_pos].colors(orientation=cube[curr_pos][curr_pos[0]])]
        letter_sequence.append(curr_letter)

        curr_pos = position_lookup[curr_letter]
        unsolved_buffers = [p for p in unsolved_buffers if sorted(p) != sorted(curr_pos)]

    #if cycle: letter_sequence.append(cycle)
    return letter_sequence, twisted_positions
    

def speffz_sequence(cube: Cube3, 
                    edge_buffer='C', 
                    corner_buffer='C', 
                    parity_buffer='B',
                    edge_priority=['UF', 'UB', 'UR', 'UL', 'FR', 'FL', 'DR', 'DL', 'DF', 'BR', 'BL', 'DB'],
                    corner_priority=['UFR', 'UBR', 'UFL', 'RDF', 'FDL', 'RDB', 'UBL', 'BDL'],
                    verbose=0):
    
    edge_priority = [p for p in edge_priority if sorted(p)!=sorted(SPEFFZ_EDGES[edge_buffer])]
    corner_priority = [p for p in corner_priority if sorted(p)!=sorted(SPEFFZ_CORNERS[corner_buffer])]

    # Scan corners
    corner_sequence, twisted_corners = _trace_helper(cube,
                                                      start=corner_buffer, 
                                                      buffer_priority=corner_priority, 
                                                      position_lookup=SPEFFZ_CORNERS, 
                                                      letter_lookup=SPEFFZ_CORNER_COLORS_L,
                                                      verbose=verbose)
    if verbose: print('corner sequence', corner_sequence, 'twisted', twisted_corners)

    # Check Parity
    parity = len(corner_sequence)%2 == 1
    
    # Resolve Corner Twists
    if twisted_corners:
        # Count number of UD tiles on the sides to tally direction of final corner rotation
        tally = 0
        twisted_pairs = []
        for f in 'FBRL':
            face = cube.get_face(f)
            for i, j in [(0,0),(0,2),(2,0),(2,2)]:
                if face[i][j].position() not in twisted_corners or face[i][j][f] not in [cube[d][d] for d in 'UD']: continue
                twisted_pairs.append([SPEFFZ_CORNERS_L[face[i][j].position(orientation=f)], # The UD face
                                      SPEFFZ_CORNERS_L[face[i][j].position(orientation='D' if i else 'U')]]) # The face in the UD position
                if not parity: tally += -1 if i==j else 1
        # Get the last remembered letter
        if not corner_sequence:
            pass # TODO in the rare case all corners are twisted/solved, set corner sequence to an arbitrary pair of same letters not equal to the same as the first or last piece in the twisted sequence
        last_position = SPEFFZ_CORNERS[corner_sequence.pop()]

        # Based on the tally, rotate the last letter in the sequence (only applies if parity)
        ordered_position = cube.order_faces(last_position)
        # Final rotation from sorted order is curr rotation + desired rotation * corner parity
        direction = ordered_position[(ordered_position.index(last_position[0]) + tally * (2*(sum([f in 'UFL' for f in last_position])%2)-1))%3]
        rotated_letter = SPEFFZ_CORNERS_L[cube.order_faces(last_position, orientation=direction)]
        if verbose: print('twisted sequence', twisted_pairs, 'parity', parity, 'parity twist', tally%3, 'adjusted letter', rotated_letter)

        # Insert the twist paris before the adjusted last letter, and after if parity exists
        if parity: corner_sequence.append(rotated_letter)
        for pair in twisted_pairs: corner_sequence += pair
        if not parity: corner_sequence.append(rotated_letter)
    if verbose: print('corner sequence', corner_sequence)

    # If corner parity, swap colors of edge and parity buffer
    color_lookup = SPEFFZ_EDGE_COLORS_L.copy()
    if parity:
        edge_color = SPEFFZ_EDGE_COLORS[edge_buffer]
        buffer_flip = edge_color[::-1]
        parity_color = SPEFFZ_EDGE_COLORS[parity_buffer]
        parity_flip = parity_color[::-1]
        color_lookup[buffer_flip], color_lookup[parity_flip] = color_lookup[parity_flip], color_lookup[buffer_flip]
        color_lookup[edge_color], color_lookup[parity_color] = color_lookup[parity_color], color_lookup[edge_color]

    # Scan edges
    edge_sequence, flipped_edges = _trace_helper(cube,
                                                    start=edge_buffer, 
                                                    buffer_priority=edge_priority, 
                                                    position_lookup=SPEFFZ_EDGES, 
                                                    letter_lookup=color_lookup,
                                                    verbose=verbose)
    if verbose: print('edge sequence', edge_sequence, 'flipped',  flipped_edges)
    
    
    # Resolve Corner Twists
    if flipped_edges:
        # Count number of UD tiles on the sides to tally direction of final corner rotation
        flipped_pairs = []
        for flip_position in flipped_edges:
            flipped_pairs.append([next(l for l, p in SPEFFZ_EDGES.items() if p==flip_position),
                                  next(l for l, p in SPEFFZ_EDGES.items() if p==flip_position[::-1])])
            
        # Get the last remembered letter, flipped if parity exists in flipped edges
        if not edge_sequence:
            pass # TODO in the rare case all corners are twisted/solved, set corner sequence to an arbitrary pair of same letters not equal to the same as the first or last piece in the twisted sequence
        last_position = SPEFFZ_EDGES[edge_sequence.pop()]
        last_letter = next(l for l, p in SPEFFZ_EDGES.items() if p==last_position[::-1 if len(flipped_pairs)%2 else None])
        if verbose: print('flipped', flipped_pairs, 'last letter', last_letter)

        # Insert the twist paris before the adjusted last letter, and after if parity exists
        for pair in flipped_pairs: edge_sequence += pair
        edge_sequence.append(last_letter)

    return {
        'corners': ' '.join(''.join(corner_sequence[i:i+2]) for i in range(0, len(corner_sequence), 2)),
        'edges': ' '.join(''.join(edge_sequence[i:i+2]) for i in range(0, len(edge_sequence), 2))
    }

def commutator(cube: Cube3, A, B, setup=''):
    return cube.execute(setup).execute(A).execute(B).execute(A, True).execute(B, True).execute(setup, True)