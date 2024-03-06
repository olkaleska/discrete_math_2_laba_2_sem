"""Алгоритм Гофмана"""

class Node:
    """Клас вузла, щоб могти збудувати дерево"""
    def __init__(self, let=None, frequency=None):
        self.let = let
        self.frequency = frequency
        self.left = None
        self.right = None
        self.cod = ''

    @staticmethod
    def create_tree(fric_dict):
        """
        Створюємо дерево з існу.чих вузлів
        Тобто першопочатково кожна вершина у нас є вузлом, і далі ми формуємо вже повністю дерево
        """
        nodes = []
        for let, freq in fric_dict.items():
            nodes.append(Node(let, freq))
        saved_nodes = nodes.copy()
        # маємо всі наші ноди
        while len(nodes) > 1:
            nodes.sort(key=lambda x: -x.frequency)
            left = nodes.pop()
            right = nodes.pop()
            # обрали два найменші значення
            higher_node = Node("-", left.frequency + right.frequency)
            higher_node.left = left
            higher_node.right = right
            # попризначали "дітей"
            nodes.append(higher_node)
            saved_nodes.append(higher_node)
        saved_nodes.sort(key=lambda x: -x.frequency)
        return saved_nodes

class Huffman:
    """Алгоритм Гофмана"""
    def encode(self, text: str) -> tuple[str, dict[str, str]]:
        """
        1) сортуємо літери за частотою їх трапляння
        """
        # fric_dict = {el:(text.count(el), round(text.count(el)/len(text), 2)) for el in text}
        # fric_dict = dict(sorted(fric_dict.items(), key=lambda x: (x[1][0], x[0])))
        # fric_dict = {el:round(text.count(el)/len(text), 2) for el in text}
        fric_dict = {el:text.count(el) for el in text}
        fric_dict = dict(sorted(fric_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))
        our_nodes = Node.create_tree(fric_dict)
        for el in our_nodes[:-2]:
            el.left.cod += '0'
            el.right.cod += '1'
        result = text
        for el in our_nodes:
            result = result.replace(el.let, el.cod)
        print(result)
        return result
        

if __name__=="__main__":
    example = Huffman()
    example.encode("Привііііітттттттт прив")

