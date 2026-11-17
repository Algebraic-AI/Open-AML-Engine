# Algebraic AI - 2025
# Go to github.com/Algebraic-AI for full license details.

from .. import CSegment
from .. import lowerOrEqual
from ..io import logInfo
import random


def prioritizeByOutOfContextSet(atoms, OutK):
    random.shuffle(atoms)
    atoms.sort(key=lambda at: len(at.ucs & OutK))
    return atoms


def selectAtomsFromNegativeDuplesAndExplicit(
    atoms, negativeDuples, startWith, repeat, contextConstantSet
):
    assert isinstance(contextConstantSet, CSegment)

    if len(atoms) == 0:
        return atoms, [], False

    negativeDuplesCopy = negativeDuples.copy()
    random.shuffle(negativeDuplesCopy)

    asetCopy = atoms.copy()
    random.shuffle(asetCopy)

    OutK = contextConstantSet.copy()
    asetCopy = prioritizeByOutOfContextSet(asetCopy, OutK)

    selection = startWith.copy()
    if selection:
        raise NotImplementedError()

    while asetCopy:
        at = asetCopy[0]
        asetCopy = asetCopy[1:]

        discriminative = False
        aux = []
        for nr in negativeDuplesCopy:
            if not lowerOrEqual(nr.L, nr.R, [at]):
                discriminative = True
            else:
                aux.append(nr)
        negativeDuplesCopy = aux

        if discriminative:
            selection.append(at)
            newOutK = OutK - at.ucs
            if len(newOutK) != len(OutK) and negativeDuplesCopy:
                OutK = newOutK
                asetCopy = prioritizeByOutOfContextSet(asetCopy, OutK)

        if not negativeDuplesCopy:
            break

    if negativeDuplesCopy:
        inconsistent = True
    else:
        inconsistent = False

    logInfo(
        f"atom set reduced from {len(atoms)} to {len(selection)} "
        f"using a negative duple set of size {len(negativeDuples)}"
    )

    if repeat:
        if len(atoms) != len(selection):
            logInfo("repeat...")
            selection, rest, inconsistent = selectAtomsFromNegativeDuples(
                selection,
                negativeDuples,
                startWith,
                repeat,
            )
            asetCopy.extend(rest)

    return selection, asetCopy, inconsistent


def selectAtomsFromNegativeDuples(atoms, negativeDuples, startWith, repeat):
    if len(atoms) == 0:
        return atoms, [], False

    random.shuffle(negativeDuples)

    inconsistent = False
    asetCopy = atoms.copy()

    random.shuffle(asetCopy)

    selection = startWith.copy()
    for nr in negativeDuples:
        if lowerOrEqual(nr.L, nr.R, selection):
            discriminated = False
            for j, at in enumerate(asetCopy):
                if not lowerOrEqual(nr.L, nr.R, [at]):
                    selection.append(asetCopy[j])
                    del asetCopy[j]

                    discriminated = True
                    break

            if not discriminated:
                inconsistent = True

    logInfo(
        f"atom set reduced from {len(atoms)} to {len(selection)} "
        f"using a negative duple set of size {len(negativeDuples)}"
    )

    if repeat:
        if len(atoms) != len(selection):
            logInfo("repeat...")
            selection, rest, inconsistent = selectAtomsFromNegativeDuples(
                selection, negativeDuples, startWith, repeat
            )
            asetCopy.extend(rest)

    return selection, asetCopy, inconsistent
