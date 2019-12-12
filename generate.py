from collections import defaultdict
import random



class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._tree = ""


    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules


    def gen(self, symbol):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            return " ".join(self.gen(s) for s in expansion)

    def gen_tree(self, symbol):
        if self.is_terminal(symbol): return symbol
        else:
            return "({} {})".format(symbol, ' '.join(self.gen_tree(s) for s in self.random_expansion(symbol)))


    def random_sent(self, tree=False):
        if tree:
            return self.gen_tree("ROOT")
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


    #


if __name__ == '__main__':

    import sys
    try:
        n = int(sys.argv[sys.argv.index('-n') + 1])
    except:
        n = 1
    pcfg = PCFG.from_file(sys.argv[1])
    for i in range(n):
        print(pcfg.random_sent(tree='-t' in sys.argv))

