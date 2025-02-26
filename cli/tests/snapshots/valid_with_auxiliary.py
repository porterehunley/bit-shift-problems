test={'a': 1, 'b': 2}

def helper(a: int) -> int:
  return a * 2



def loose_equals(a, b):
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if x != y:
                return False
        return True
    else:
        return a == b

test={'a': 1, 'b': 2}

def helper(a: int) -> int:
  return a * 2


def add(a: int, b: int) -> int:
  return a + b

output=add(**test)

def add_truth(a: int, b: int) -> int:
  return a + b


expected=add_truth(**test)

is_expected= loose_equals(output, expected)
print(is_expected)