def getLineNumNode(node:'Node'):
    return node.getLine()

class Node:
    __slots__=("_children", "_data", "_line")
    def __init__(self, data, line, *children) -> None:
        self._data=data
        self._line=line
        self._children=None
        for child in children:
            self.addChild(child)
    
    def addChild(self, child:'Node'):
        try:
          self._children.append(child)
        except:
          self._children=list()
          self._children.append(child)

    def getLatestChild(self) -> 'Node':
        try:
          return self._children[-1]
        except:
          return None
        
    def compareData(self, data) -> bool:
        return self._data==data

    def getData(self):
        return self._data

    def getLine(self):
        return self._line

    def getLevel(self):
        return self._data.count("#") if self._data.startswith('#') else 7 if self._data.startswith('-') else 8
    
    def searchByLine(self, line):
        if (self._line==line):
            return self
        elif (self._children is None):
            return None
        for child in self._children:
            node=child.searchByLine(line)
            if (node is not None):
                return node
        return None

    def getImages(self):
        if (self._children is None and self.getLevel()==8):
            return self
        elif (self._children is not None):
            ret=list()
            for node in self._children:
                try:
                    ret.extend(node.getImages())
                except:
                    ret.append(node.getImages())
            return ret
        return None

    def getChildrenData(self):
        return [node.getData() for node in self._children]

    def parentOf(self, data):
        return data in self.getChildrenData()

    def searchInChildrenByData(self, data):
        try:
            for node in self._children:
                if (node.getData()==data):
                    return node
        except: pass
        return None

    def updateLineNum(self, line_num, inc):
        if (self._line>=line_num):
            self._line+=inc
        try:
            for node in self._children:
                node.updateLineNum(line_num, inc)
        except:
            pass

    def orderNodesByLineNumber(self):
        ret: list=[self]
        try:
            for child in self._children:
                ret.extend(child.orderNodesByLineNumber())
        except:
            pass
        return ret

    def __str__(self) -> str:
        ret:str=""
        ret+= (f"Level {self.getLevel()}: line -> {self._line} data: {self._data}.")
        try:
            for node in self._children:
                ret+=str(node)+'\n'
        except:
            pass
        return ret
    
        

class Tree:
    __slots__=("_parent_node")
    def __init__(self, parent:Node):
        self._parent_node=parent
    
    def getParent(self) -> Node:
        return self._parent_node

    def getLatestNode(self) -> Node:
        last=self._parent_node
        next=last.getLatestChild()
        while ( next is not None ):
            last=next
            next=next.getLatestChild()
        return last
    
    def getLevelLatest(self, level):
        act=1
        node=self._parent_node
        while ((node is not None) and (level>act)):
            node=node.getLatestChild()
            act=node.getLevel()
        return node
    
    def searchByLineNumber(self, line_num):
        return self._parent_node.searchByLine(line_num)

    def getImages(self):
        return self._parent_node.getImages()
    
    def addNewImage(self, image_hierarchy):
        node=self._parent_node
        for image in (image_hierarchy):
            new_node=node.searchInChildrenByData(image)
            if (new_node is not None):
                node=new_node
            else:
                inc=1
                line_num=node.getLine()
                if (image.startswith('!')):
                    inc+=1
                    self.updateLineNum(line_num+1, inc+2)
                else:
                    self.updateLineNum(line_num+1, inc)
                new_node=Node(image, (line_num+inc))
                node.addChild(new_node)
                node=new_node

    def updateLineNum(self, line_num, inc):
        self._parent_node.updateLineNum(line_num, inc)

    def makeFile(self):
        print (None)

    def orderNodesByLineNumber(self):
        ret=self._parent_node.orderNodesByLineNumber()
        ret.sort(key=getLineNumNode)
        return ret
        
    def __str__(self) -> str:
        return (str(self._parent_node))
