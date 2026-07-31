"""
Specimen label check digit — modulus 11, weights 2-7 applied right to left.
Reference: specimen_label_allocation.csv, check_digit_scheme column.
"""

def check_digit(number_str: str) -> str:
    """number_str: the digits of the label BEFORE the check digit (e.g. '480000')."""
    digits = [int(d) for d in number_str]
    weights = [2, 3, 4, 5, 6, 7]  # applied right to left
    total = 0
    for digit, weight in zip(reversed(digits), weights):
        total += digit * weight
    remainder = total % 11
    check = 11 - remainder
    if check == 11:
        check = 0
    if check == 10:
        return "X"
    return str(check)

def is_valid(number_str: str, given_check: str) -> bool:
    return check_digit(number_str) == given_check


TEST_CASES = [
    # (description, number, given_check, expect_valid)
    ("Valid: range start, TM01",              "480000", "1", True),
    ("Valid: hits remainder-10 -> X case",     "480001", "X", True),
    ("Valid: range end, TM01",                 "480899", "1", True),
    ("Invalid: wrong check digit typed",       "480010", "0", False),  # correct is 9
    ("Invalid: adjacent-digit transposition",  "480001", "9", False),  # 480010's check
                                                                        # applied to 480001
    ("Invalid: single-digit substitution",     "480011", "9", False),  # correct differs
                                                                        # from 480010's 9
    ("Boundary: one past TM01 range (480900 is TM02's start)", "480900", None, None),
]

if __name__ == "__main__":
    print("=== Check digit computation ===")
    for n in ["480000", "480001", "480899", "481000", "480010", "480011", "480900"]:
        print(f"BSN {n} -> {check_digit(n)}")

    print()
    print("=== Validation test cases ===")
    for desc, number, given, expected in TEST_CASES:
        if given is None:
            print(f"{desc}: (range-membership case, no check-digit assertion here)")
            continue
        result = is_valid(number, given)
        status = "PASS" if result == expected else "FAIL <<<<<"
        print(f"{desc}: is_valid({number}, {given}) = {result}, expected {expected} [{status}]")
