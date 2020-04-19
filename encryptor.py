import argparse
import string
from typing import Any
import sys


class Caesar:
    """Шифр Цезаря"""

    def encode(self, input_text: str, key_1: Any, type_work: int = 1) -> str:
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        try:
            key = int(key_1)
        except BaseException:
            print("Key entered incorrectly, check key entry.",
                  "For Caesar's cipher, the key is number.")
            sys.exit()
        new = ''
        quantity = 26

        def editor(letr: int, type_letter: int) -> int:
            new_letter = (letr + key * type_work) % type_letter
            if new_letter < 0:
                new_letter += type_letter
            return new_letter

        for letter in input_text:
            if set(letter) & (set(lower)):
                new += (lower[editor(lower.index(letter), quantity)])
            elif set(letter) & (set(upper)):
                new += (upper[editor(upper.index(letter), quantity)])
            else:
                new += letter
        return new

    def decode(self, input_text: str, key: Any) -> str:
        return self.encode(input_text, key, type_work=-1)


class Vigenere:
    """Шифр Виженера"""

    def encode(self, input_text: str, key: str, type_work: int = 1) -> str:
        """Шифп Винжера"""
        index = 0
        index_len = len(key)
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        new = ''
        quantity = 26
        test = set(lower) | set(upper)
        if len(test | set(key)) > len(test):
            print("Key entered incorrectly, "
                  "check character correctness")
            sys.exit()

        def editor(new_letter: int, index: str, type_letter: int) -> int:
            key_num = lower.index(index)
            new_letter = (new_letter + key_num * type_work) % type_letter
            if new_letter < 0:
                new_letter += type_letter
            return new_letter

        for letter in input_text:
            if set(letter) & (set(lower)):
                new += (lower[editor(lower.index(letter),
                                     key[index].lower(), quantity)])
                index = (index + 1) % index_len
            elif set(letter) & (set(upper)):
                new += (upper[editor(upper.index(letter),
                                     key[index].lower(), quantity)])
                index = (index + 1) % index_len
            else:
                new += letter
        return new

    def decode(self, input_text: str, key: str) -> str:
        return self.encode(input_text, key, type_work=-1)


class Vernam:
    """Шифп Вернама, не сохраняет регистра"""

    def encode(self, input_text: str, key: str) -> str:
        my_code_Bodo = ' .,!a:jkexgm?zhlysbrutcqiwfnovdp'
        if ((len(input_text) is not len(key))
                or (len(set(key) | set(my_code_Bodo)) > len(my_code_Bodo))):
            print("Key entered incorrectly, "
                  "check character correctness, and length")
            sys.exit()
        new: str = ''

        def editor(new_letter: int, index: str) -> int:
            key_num: int = my_code_Bodo.index(index)
            new_letter = new_letter ^ key_num
            return new_letter

        for letter in range(len(input_text)):
            let = input_text[letter].lower()
            if set(let) & set(my_code_Bodo):
                new += my_code_Bodo[editor(my_code_Bodo.index(let),
                                           key[letter].lower())]
            else:
                new += (input_text[letter])
        return new

    def decode(self, input_text: str, key: str) -> str:
        return self.encode(input_text, key)


class Hacker:
    def learner(self, input_text: str, file: Any, mod=True) -> Any:
        learn_dict = {a: 0 for a in (string.ascii_lowercase)}
        letter_num = 0
        gistogram = ''
        for letter in input_text:
            let = letter.lower()
            if not (set(let) & set(learn_dict.keys()) == set()):
                learn_dict.update({let: learn_dict.get(let) + 1})
                letter_num += 1
        for key in learn_dict.keys():
            gistogram += (str(learn_dict.get(key) / (letter_num / 100)) + ' ')
        if mod:
            try:
                f = open(file)
            except FileNotFoundError:
                print(file, "doesn't exist")
                sys.exit()
            else:
                f.write(gistogram)
        else:
            return list(gistogram.split())

    def hack(self, input_text: str, model: list) -> str:
        quantity: int = 26
        caes = Caesar()
        max_sum: float = 100
        my_index: int = 0
        gist = self.learner(input_text, None, mod=False)
        for chenger in range(quantity):
            sum_gis: float = 0
            for index in range(quantity):
                try:
                    modl = float(model[index])
                except TypeError:
                    print("Check the File model, "
                          "it should contain only numbers of type float")
                    sys.exit()
                else:
                    sum_gis += abs((float(gist[(index + chenger) % quantity]) -
                                    modl))
            if sum_gis < max_sum:
                max_sum = sum_gis
                my_index = chenger

        return caes.decode(input_text, my_index)


def reader(file: str) -> str:
    if file is None:

        return str(input())
    else:
        try:
            f = open(file)
        except FileNotFoundError:
            print(file, "doesn't exist")
            sys.exit()
        else:
            return f.read()


def writer(file: str, text: str) -> None:
    if file is None:
        print(text)
    else:
        try:
            fil = open(file, "w")
        except FileNotFoundError:
            print(file, "doesn't exist")
            sys.exit()
        else:
            fil.write(text)


def analyzer(objective: str, text: str, cipher: str = None,
             key: str = None, output: str = None, model: str = None) -> None:
    if objective == 'encode':
        if cipher == 'caesar':
            obj = Caesar()
            writer(output, obj.encode(text, key))
        elif cipher == 'vigenere':
            obj1 = Vigenere()
            writer(output, obj1.encode(text, key))

        elif cipher == 'vernam':
            obj2 = Vernam()
            writer(output, obj2.encode(text, key))
    elif objective == 'decode':
        if cipher == 'caesar':
            obj3 = Caesar()
            writer(output, obj3.decode(text, key))
        elif cipher == 'vigenere':
            obj4 = Vigenere()
            writer(output, obj4.decode(text, key))
        elif cipher == 'vernam':
            obj5 = Vernam()
            writer(output, obj5.decode(text, key))
    elif objective == 'train':
        obj6 = Hacker()
        obj6.learner(text, model)

    elif objective == 'hack':
        obj7 = Hacker()
        writer(output, obj7.hack(text, list(reader(model).split())))
    else:
        print("This command not found.")


parser = argparse.ArgumentParser()
parser.add_argument('program_objective',
                    type=str,
                    help="What the program should do")
parser.add_argument('--cipher',
                    type=str,
                    help='Encryption type')
parser.add_argument('--key',
                    type=str,
                    help='Encryption key')
parser.add_argument('--input-file',
                    type=str,
                    help='Input file')
parser.add_argument('--output-file',
                    type=str,
                    help='Output file')
parser.add_argument('--model-file',
                    type=str,
                    help='Model file')
args = parser.parse_args()
text: str = reader(args.input_file)
objective: str = args.program_objective
cipher: str = args.cipher
key: str = args.key
inp: str = args.input_file
out: str = args.output_file
model: str = args.model_file
analyzer(objective, text, cipher=cipher, key=key, output=out, model=model)
