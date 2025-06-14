from sympy.combinatorics import Permutation, SymmetricGroup

mod = 5
G = SymmetricGroup(4)


# Generate all elements and sort lexicographically by 1-based permutation tuples
def get_1based_perm_tuple(p):
    """Convert SymPy permutation to 1-based tuple for sorting."""
    return tuple([x + 1 for x in p(list(range(4)))])


unsorted_elements = list(G.generate())
elements_list = sorted(unsorted_elements, key=get_1based_perm_tuple)
element_to_index = {el: idx for idx, el in enumerate(elements_list)}

# Conjugacy class representatives (0-based cycles)
class_reps = [
    Permutation([], size=4),  # Identity
    Permutation(0, 1),  # (1,2)
    Permutation(0, 1)(2, 3),  # (1,2)(3,4)
    Permutation(0, 1, 2),  # (1,2,3)
    Permutation(0, 1, 2, 3),  # (1,2,3,4)
]

# Character table in order: trivial, sign, 2D, standard, 3D
characters = [
    [1, 1, 1, 1, 1],  # Trivial
    [1, -1, 1, 1, -1],  # Sign
    [2, 0, 2, -1, 0],  # 2D
    [3, 1, -1, 0, -1],  # Standard
    [3, -1, -1, 0, 1],  # 3D
]

class_sizes = [1, 6, 3, 8, 6]  # Match class_reps order


def get_class_index(g):
    """Find conjugacy class index for element g."""
    for i, rep in enumerate(class_reps):
        if g in G.conjugacy_class(rep):
            return i
    return -1


order_G = 24
inv_order_mod5 = pow(order_G % mod, -1, mod)  # 24⁻¹ ≡ 4 mod5

central_idempotents = []
for chi in characters:
    idempotent = [0] * order_G
    for g in elements_list:
        class_idx = get_class_index(g)
        coeff = (chi[0] * chi[class_idx] * inv_order_mod5) % mod
        idx = element_to_index[g]
        idempotent[idx] = coeff
    central_idempotents.append(idempotent)

# Print results
for i, eid in enumerate(central_idempotents, start=1):
    print(f"e{i} =", tuple(eid))
