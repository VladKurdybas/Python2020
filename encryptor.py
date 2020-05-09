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


def cipher(name: str) -> Union[Caesar, Vigenere, Vernam]:
    if name == 'caesar':
        return Caesar()
    elif name == 'vigenere':
        return Vigenere()
    elif name == 'vernam':
        return Vernam()
    else:
        print("")
        sys.exit()


def read(file: Optional[str]) -> str:
    if file is None:
        return str(input())

    else:
        try:
            with open(file, 'r') as opened_file:
                return opened_file.read()
        except FileNotFoundError:
            print(file, "Doesn't exist")
            sys.exit()


def write(file: Optional[str], text: str) -> None:
    if file is None:
        print(text)
    else:
        try:
            with open(file, 'w') as opened_file:
                opened_file.write(text)
        except FileNotFoundError:
            print(file, "Doesn't exist")
            sys.exit()


def analyze(args: argparse.Namespace) -> None:
    if args.program_objective == 'encode':
        obj = cipher(args.cipher)
        write(args.output_file, obj.encode(read(args.input_file), args.key))

    elif args.program_objective == 'decode':
        obj2 = cipher(args.cipher)
        write(args.output_file, obj2.decode(read(args.input_file), args.key))

    elif args.program_objective == 'train':
        obj3 = Hacker()
        obj3.learn(read(args.text_file), args.text_file)

    elif args.program_objective == 'hack':
        obj4 = Hacker()
        write(args.output_file,
              obj4.hack(read(args.input_file), str(args.model_file)))
    else:
        print("This command not found.")


def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="User database utility")
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser("encode", help="Encode")
    parser_encode.set_defaults(program_objective='encode')

    parser_encode.add_argument('--cipher', help='Encryption type')
    parser_encode.add_argument('--key', help='Encryption key')
    parser_encode.add_argument('--input-file', help='Input file')
    parser_encode.add_argument('--output-file', help='Output file')

    parser_decode = subparsers.add_parser("decode", help="Decode")
    parser_decode.set_defaults(program_objective="decode")

    parser_decode.add_argument('--cipher', help='Encryption type')
    parser_decode.add_argument('--key', help='Encryption key')
    parser_decode.add_argument('--input-file', help='Input file')
    parser_decode.add_argument('--output-file', help='Output file')

    parser_train = subparsers.add_parser("train", help="Train")
    parser_train.set_defaults(program_objective='train')

    parser_train.add_argument('--text-file', help='Text file')
    parser_train.add_argument('--model-file', help='Model file')

    parser_hack = subparsers.add_parser("hack", help="Hack")
    parser_hack.set_defaults(program_objective="hack")

    parser_hack.add_argument('--input-file', help='Input file')
    parser_hack.add_argument('--output-file', help='Output file')
    parser_hack.add_argument('--model-file', help='Model file')

    args = parser.parse_args()

    return args


def main():
    analyze(arg_parser())


if __name__ == '__main__':
    main()
