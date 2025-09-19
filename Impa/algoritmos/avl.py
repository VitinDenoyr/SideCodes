# ---------------------------------------AVL---------------------------------------

class Node:
    def __init__(self,val,l = None,r = None):
        self.val = val
        self.qt = 1
        self.bal = 0
        self.left = l
        self.right = r

class AVL:
    def __init__(self, h = None):
        self.head = h
        
    # Busca
    
    def _count(self, x, y):
        if y == None:
            return 0
        if x == y.val:
            return y.qt
        elif x > y.val:
            return self._count(x,y.right)
        else:
            return self._count(x,y.left)
        
    def count(self, x):
        return self._count(x,self.head)
    
    # Representação
    
    def _print(self, y):
        if y == None: return
        self._print(y.left)
        print(f'  [{y.val}]{f' x {y.qt}' if y.qt > 1 else ''}, balance = {y.bal}, L = {None if y.left == None else y.left.val}, R = {None if y.right == None else y.right.val}')
        self._print(y.right)
    
    def print(self, y = None):
        if self.head == None:
            print("Empty Tree")
        elif y == None:
            print("Tree:")
            self._print(self.head)
            
    # Balanceamento
    
    def _balanceLeft(self, y):
        z = y.left
        if z.bal == 1:
            # Balanço LL
            y.left = z.right
            z.right = y
            z.bal = y.bal = 0
            return z
        elif z.bal == -1:
            # Balanço LR
            m = z.right
            z.right = m.left; y.left = m.right
            m.left = z; m.right = y
            if m.bal == -1:
                z.bal = 1
            else:
                z.bal = 0
            if m.bal == 1:
                y.bal = -1
            else:
                y.bal = 0
            m.bal = 0
            return m
        else:
            # Balanço LL Neutro
            y.left = z.right
            z.right = y
            y.bal = 1
            z.bal = -1
            return z
        
    def _balanceRight(self, y):
        z = y.right
        if z.bal == -1:
            # Balanço RR
            y.right = z.left
            z.left = y
            z.bal = y.bal = 0
            return z
        elif z.bal == 1:
            # Balanço RL
            m = z.left
            z.left = m.right; y.right = m.left
            m.right = z; m.left = y
            if m.bal == 1:
                z.bal = -1
            else:
                z.bal = 0
            if m.bal == -1:
                y.bal = 1
            else:
                y.bal = 0
            m.bal = 0
            return m
        else:
            # Balanço RR Neutro
            y.right = z.left
            z.left = y
            y.bal = -1
            z.bal = 1
            return z
        
    # Atualização de balanceamentos
        
    def _updateInsertionBalance(self, y, dif):
        res = False
        if y.bal == 0:
            y.bal += dif
            res = True
        elif y.bal + dif == 0:
            y.bal = 0
        else:
            if dif == 1:
                y = self._balanceLeft(y)
            else:
                y = self._balanceRight(y)
        return y, res
    
    def _updateRemovalBalance(self, y, dif):
        res = False
        if y.bal == 0:
            y.bal += dif
        elif y.bal + dif == 0:
            y.bal = 0
            res = True
        else:
            if dif == 1:
                y = self._balanceLeft(y)
            else:
                y = self._balanceRight(y)
        return y, res
    
    # Substituição para Remoção
    
    def _getReplacement(self, y):
        if y.left != None:
            y.left, replacement, res = self._getReplacement(y.left)
            if res == True:
                y, res = self._updateRemovalBalance(y, -1)
            return y, replacement, res
        else:
            k = y.right
            y.right = None
            y.bal = 0
            return k, y, True
    
    # Inserção
    
    def _insert(self, x, y):
        res = False
        if y == None:
            return Node(x), True
        if x == y.val:
            y.qt += 1
            return y, False
        elif x < y.val:
            y.left, res = self._insert(x, y.left)
            if res:
                y, res = self._updateInsertionBalance(y, 1)
        else:
            y.right, res = self._insert(x, y.right)
            if res:
                y, res = self._updateInsertionBalance(y, -1)
        return y, res
    
    def insert(self, x):
        if self.head == None:
            self.head = Node(x)
        else:
            self.head, _ = self._insert(x, self.head)
    
    # Remoção
    
    def _remove(self, x, y):
        if y == None:
            return y, False
        res = False
        if y.val > x:
            y.left, res = self._remove(x, y.left)
            if res:
                y, res = self._updateRemovalBalance(y, -1)
        elif y.val < x:
            y.right, res = self._remove(x, y.right)
            if res:
                y, res = self._updateRemovalBalance(y, 1)
        else:
            if y.qt > 1:
                y.qt -= 1
                return y, False
            else: 
                if y.left == None and y.right == None:
                    return None, True
                elif y.left == None:
                    return y.right, True
                elif y.right == None:
                    return y.left, True
                else:
                    y.right, replacement, res = self._getReplacement(y.right)
                    if res:
                        y, res = self._updateRemovalBalance(y, 1)
                    replacement.left = y.left
                    replacement.right = y.right
                    replacement.bal = y.bal
                    return replacement, res
        return y, res
                            
    def remove(self, x):
        if self.head != None:
            self.head, _ = self._remove(x, self.head)
    
# ---------------------------------------------------------------------------------