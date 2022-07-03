import os
import argparse
import hashlib
from collections import defaultdict


class Handler:

    def __init__(self):
        self.sizes = defaultdict(list)
        self.duplicates = {}
        self.hashes = defaultdict(list)
        self.parser = argparse.ArgumentParser(description='input path here')
        self.parser.add_argument('path', default=None, nargs='?')
        self.args = self.parser.parse_args()
        self.path = self.args.path

    def cmd(self) -> None:
        if not self.path:
            print('Directory is not specified')
            return
        self.menu()
        return

    def file_walk(self, fle_format) -> None:
        for root, dirs, files in os.walk(self.path, topdown=True):
            for fle in files:
                if fle.endswith(f'.{fle_format}') or not fle_format:
                    self.sizes[os.path.getsize(f'{root}\\{fle}')].append(f'{root}\\{fle}')
        return

    def print_order(self, order=0) -> None:
        for key, val in sorted(self.sizes.items(), reverse=bool(order)):
            print(f'{key} bytes')
            print('\n'.join(val))
        return

    def hash(self, order=0):
        for key, val in self.sizes.items():
            for fle in val:
                with open(fle, 'rb') as f:
                    h = hashlib.md5()
                    h.update(f.read())
                self.hashes[(key, h.hexdigest())].append(fle)
        i = 1
        prev = -1
        for key, val in sorted(self.hashes.items(), reverse=bool(order)):
            if len(val) < 2:
                continue
            if key[0] != prev:
                print(f'{key[0]} bytes')
            prev = key[0]
            print(f'Hash: {key[1]}', sep='\n')
            for fle in val:
                print(f'{i}. {fle}')
                self.duplicates[i] = (key[0], fle)
                i += 1
        return

    def removing(self):
        while True:
            print('Enter files to delete:')
            try:
                to_del = [int(i) for i in input().split()]
                if len(to_del) == 0:
                    raise Exception
                space = 0
                for elem in to_del:
                    os.remove(self.duplicates[elem][1])
                    space += self.duplicates[elem][0]
                print(f'Total freed up space: {space} bytes')
                return
            except Exception:
                print('Wrong format')
                continue

    def menu(self) -> None:
        print('Enter file format:')
        fle_format = input()
        self.file_walk(fle_format)
        while True:
            print('Size sorting options:\n1. Descending\n2. Ascending')
            order = input()
            if order == '1':
                f_ord = 1
                self.print_order(f_ord)
                break
            if order == '2':
                f_ord = 0
                self.print_order(f_ord)
                break
            print('Wrong option')
        while True:
            print('Check for duplicates?')
            answer = input()
            if answer == 'yes':
                self.hash(f_ord)
                break
            if answer == 'no':
                break
            print('Wrong option')
        while True:
            print('Delete files?')
            ans = input()
            if ans == 'yes':
                self.removing()
                break
            if ans == 'no':
                break
            print('Wrong option')
        return


if __name__ == '__main__':
    handler = Handler()
    handler.cmd()
