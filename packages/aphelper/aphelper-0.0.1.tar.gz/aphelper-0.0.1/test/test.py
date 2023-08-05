from aphelper import core

class Test:
    def __init__(self):
        ah = core.ArgparseHelper(def_file='test/test.jsonc', parent=self)
        ah.execute()

    def test(self, args):
        print('test')

if __name__ == '__main__':
    Test()