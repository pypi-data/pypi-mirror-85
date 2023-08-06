class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.p1 = None

    def traversal(self):
        printval = self.head
        while printval is not None:
            print(printval.data , end="->")
            printval = printval.next

    def AtBegining(self, data):
        pnode = Node(data)

        # Update the new nodes next val to existing node
        pnode.next = self.head
        self.head = pnode

    def AtEnd(self, data):
        pnode = Node(data)
        if self.head is None:
            self.head = pnode
            return
        last = self.head
        while (last.next):
            last = last.next
        last.next = pnode

    def Inbetween(self, middle_node, newdata):
        if middle_node is None:
            print("The mentioned node is absent")
            return
        printval1 = 1
        printval = self.head
        while printval1 < middle_node:
            printval = printval.next
            printval1 = printval1+1
        NewNode = Node(newdata)
        NewNode.next = printval.next
        printval.next = NewNode

    def RemoveNode(self, Removekey):

        HeadVal = self.head

        if (HeadVal is not None):
            if (HeadVal.data == Removekey):
                self.head = HeadVal.next
                HeadVal = None
                return

        while (HeadVal is not None):
            if HeadVal.data == Removekey:
                break
            prev = HeadVal
            HeadVal = HeadVal.next

        if (HeadVal == None):
            return

        prev.next = HeadVal.next

        HeadVal = None

# class Initialize:
#     def __init__(self):
#         self.list1 = LinkedList()

li = LinkedList()


def create(val):

    if li.head == None:

        li.head = Node(val)
        li.p1 = li.head


    else:

        n = Node(val)
        li.p1.next = n
        li.p1 = li.p1.next




def insertBegin(val):

    if li.head is None:
        print("Create A Node First")
    else:
        li.AtBegining(val)

def insertAtEnd(val):
    if li.head is None:
        print("Create A Node First")
    else:
        li.AtEnd(val)

def insertMiddle(position,data):
    if li.head is None:
        print("Create A Node First")
    else:
        li.Inbetween(position,data)

def removeNode(val):
    if li.head is None:
        print("Create A Node First")
    else:
        li.RemoveNode(val)

def traversal():
    print(li.traversal())


# create("hi")
# create("how")
# create("r")
# create("u")
# begin("bro")
# AtEnd(55)
#
# middle(3,"hehe")
# traversal()
# RemoveNode("hehe")