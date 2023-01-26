decNumbers = [523, 458, 399, 878, 1001, 1112, 2056]
binNumbers = []
octNumbers = []
hexNumbers = []
hex_dict = {0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'A',
            11: 'B',
            12: 'C',
            13: 'D',
            14: 'E',
            15: 'F'
            }

for num in decNumbers:
    binary = ''
    while num > 0:
        binary = str(num % 2) + binary
        num = num // 2
    binNumbers.append(binary)

for nummer in decNumbers:
    octal = ''
    while nummer > 0:
        octal = str(nummer % 8) + octal
        nummer = nummer // 8
    octNumbers.append(octal)

for numero in decNumbers:
    hexadecimal = ''
    while numero > 0:
        hex = str(numero % 16)
        hexadecimal = hex_dict[hex] + hexadecimal
        numero = numero // 16
    hexNumbers.append(hexadecimal)

print('Binary: ', binNumbers)
print('Octal: ', octNumbers)
print('Hexadecimal: ', hexNumbers)
