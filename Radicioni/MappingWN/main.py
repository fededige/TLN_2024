from nltk.corpus import framenet as fn
from nltk.corpus.reader.framenet import PrettyList

luca_bonamico = [159, 302, 2837, 792, 2668]
luca_cena = [2971, 560, 2840, 797, 1894]
federico = [1683, 366, 1601, 414, 1591]

if __name__ == '__main__':
    f = fn.frame(luca_bonamico[0])
    luca_bonamico_frame = []
    luca_cena_frame = []
    federico_frame = []

    for frame_id in luca_bonamico:
        luca_bonamico_frame.append(fn.frame(frame_id))

    for frame_id in luca_cena:
        luca_cena_frame.append(fn.frame(frame_id))

    for frame_id in federico:
        federico_frame.append(fn.frame(frame_id))

    for f in luca_bonamico_frame:
        print("\n", f.name)
        print('\n____ FEs ____')
        FEs = f.FE.keys()
        for fe in FEs:
            fed = f.FE[fe]
            print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))

        print('\n____ LUs ____')
        LUs = f.lexUnit.keys()
        for lu in LUs:
            print(lu)

