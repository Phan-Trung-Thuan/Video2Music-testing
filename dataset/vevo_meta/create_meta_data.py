import os
import json

pwd = os.path.join('./dataset', 'vevo_meta')
chordPath = os.path.join(pwd, 'chord.json')
chordRootPath = os.path.join(pwd, 'chord_root.json')
chordAttPath = os.path.join(pwd, 'chord_att.json')

chordInvPath = os.path.join(pwd, 'chord_inv.json')
chordRootInvPath = os.path.join(pwd, 'chord_root_inv.json')
chordAttInvPath = os.path.join(pwd, 'chord_att_inv.json')

def invert_json(input_path, output_path):
    with open(input_path, 'r') as fi:
        data = json.load(fi)

    ans = {}
    for key, value in data.items():
        ans[str(value)] = key

    with open(output_path, 'w') as fo:
        json.dump(ans, fo, indent=4)

invert_json(chordPath, chordInvPath)
invert_json(chordRootPath, chordRootInvPath)
invert_json(chordAttPath, chordAttInvPath)