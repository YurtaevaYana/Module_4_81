def is_palindrom(string):
    return string == string[::-1]
print(is_palindrom('abcddcba'))