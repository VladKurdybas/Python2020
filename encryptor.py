import argparse
import string
from typing import Any, Union, Optional
import sys
import pickle

lower = string.ascii_lowercase
upper = string.ascii_uppercase


class Caesar:
    """Шифр Цезаря"""

    def encode(self, input_text: str, key_1: Union[int, str],
               type_work: int = 1) -> str:
        global lower
        global upper
        try:
            key = int(key_1)
        except TypeError:
            print("Key entered incorrectly, check key entry.",
                  "For Caesar's cipher, the key is number.")
            sys.exit()
        new = ''
        quantity = 26

        def edit(letr: int, type_letter: int) -> int:
            new_letter = (letr + key * type_work) % type_letter
            return new_letter

        for letter in input_text:
            if set(letter) & (set(lower)):
                new += lower[edit(lower.index(letter), quantity)]
            elif set(letter) & (set(upper)):
                new += upper[edit(upper.index(letter), quantity)]
            else:
                new += letter
        return new

    def decode(self, input_text: str, key: Union[int, str]) -> str:
        return self.encode(input_text, key, type_work=-1)


class Vigenere:
    """Шифр Виженера"""

    def encode(self, input_text: str, key: str, type_work: int = 1) -> str:
        """Шифп Винжера"""
        index = 0
        index_len = len(key)
        global lower
        global upper
        new = ''
        quantity = 26
        test = set(lower) | set(upper)
        if len(test | set(key)) > len(test):
            print("Key entered incorrectly, "
                  "check character correctness")
            sys.exit()

        def edit(new_letter: int, index: str, type_letter: int) -> int:
            key_num = lower.index(index)
            new_letter = (new_letter + key_num * type_work) % type_letter
            if new_letter < 0:
                new_letter += type_letter
            return new_letter

        for letter in input_text:
            if set(letter) & (set(lower)):
                new += (lower[edit(lower.index(letter), key[index].lower(),
                                   quantity)])
                index = (index + 1) % index_len
            elif set(letter) & (set(upper)):
                new += (upper[edit(upper.index(letter), key[index].lower(),
                                   quantity)])
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

        def edit(new_letter: int, index: str) -> int:
            key_num: int = my_code_Bodo.index(index)
            new_letter = new_letter ^ key_num
            return new_letter

        for letter in range(len(input_text)):
            let = input_text[letter].lower()
            if set(let) & set(my_code_Bodo):
                bodo = my_code_Bodo.index(let)
                new += my_code_Bodo[edit(bodo, key[letter].lower())]
            else:
                new += (input_text[letter])
        return new

    def decode(self, input_text: str, key: str) -> str:
        return self.encode(input_text, key)


class Hacker:
    def learn(self, input_text: str, file: Any, mod=True) -> Any:
        learn_dict = {a: 0.0 for a in (string.ascii_lowercase)}
        letter_num = 0
        for letter in input_text:
            let = letter.lower()
            if set(let) & set(learn_dict.keys()):
                learn_dict[let] += 1
                letter_num += 1
        for key in learn_dict:
            learn_dict[key] = learn_dict[key] / (letter_num / 100)
        if mod:
            with open(file, 'wb') as f:
                pickle.dump(learn_dict, f)
        else:
            return learn_dict

    def hack(self, input_text: str, model_file: str) -> str:
        quantity: int = 26
        caes = Caesar()
        max_sum: float = 100
        my_index: int = 0
        try:
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
        except FileNotFoundError:
            print(model_file, "doesn't exist")
            sys.exit()
        else:
            f.close()
        gist = self.learn(input_text, None, mod=False)
        for chenger in range(quantity):
            sum_gis: float = 0
            for index in range(quantity):
                try:
                    modl = float(model[lower[index]])
                except TypeError:
                    print("Check the File model, "
                          "it should contain only numbers of type float")
                    sys.exit()
                else:
                    my_gist = float(gist[lower[(index + chenger) % quantity]])
                    sum_gis += abs(my_gist - modl)
            if sum_gis < max_sum:
                max_sum = sum_gis
                my_index = chenger

        return caes.decode(input_text, my_index)


def read(file: Optional[str]) -> str:
    if file is None:
        return str(input())
    else:
        with open(file, 'r') as opened_file:
            return opened_file.read()


def write(file: Optional[str], text: str) -> None:
    if file is None:
        print(text)
    else:
        with open(file, 'w') as opened_file:
            opened_file.write(text)


def analyze(objective: str, text: str, cipher: str = None,
            key: str = '', output: str = '', model: str = '') -> None:
    if objective == 'encode':
        if cipher == 'caesar':
            obj = Caesar()
            write(output, obj.encode(text, key))
        elif cipher == 'vigenere':
            obj1 = Vigenere()
            write(output, obj1.encode(text, key))

        elif cipher == 'vernam':
            obj2 = Vernam()
            write(output, obj2.encode(text, key))
    elif objective == 'decode':
        if cipher == 'caesar':
            obj3 = Caesar()
            write(output, obj3.decode(text, key))
        elif cipher == 'vigenere':
            obj4 = Vigenere()
            write(output, obj4.decode(text, key))
        elif cipher == 'vernam':
            obj5 = Vernam()
            write(output, obj5.decode(text, key))
    elif objective == 'train':
        obj6 = Hacker()
        obj6.learn(text, model)

    elif objective == 'hack':
        obj7 = Hacker()
        write(output, obj7.hack(text, str(model)))
    else:
        print("This command not found.")


def main():
    parser = argparse.ArgumentParser(description="User database utility")
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
    text: str = read(args.input_file)
    objective: str = args.program_objective
    cipher: str = args.cipher
    key: str = args.key
    out: str = args.output_file
    model: str = args.model_file
    analyze(objective, text, cipher=cipher, key=key, output=out, model=model)


if __name__ == '__main__':
    main()
