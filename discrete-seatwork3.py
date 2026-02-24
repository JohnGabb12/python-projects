__ = lambda ____: ____ if ____ in "ABCDE" else (lambda: exec("raise ValueError('Invalid function output. Please enter one of A, B, C, D, E.')"))()
___ = [__(input(f"Output of function {i}: ").upper()) if i != 0 else exec("print('Co-domain (A, B, C, D, E)')") for i in range(int(input("Number of functions: "))+1)]
_ = [len(set(___[1:])) == len(___[1:]), set(___[1:]) == set("A B C D E".split(' '))]
print(f"It is {'not ' if not _[0] else ''}injective.\nIt is {'not ' if not _[1] else ''}surjective.\nIt is {'not ' if not (_[0] and _[1]) else ''}bijective.")