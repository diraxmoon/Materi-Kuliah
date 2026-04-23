class node:
    def __init__(self, data):
        self.data = data
        self.next = None

class linkedlist:
    def __init__(self):
        self.head = None

    def add__list(self, data):
        new_node = node(data)
        new_node.next = self.head
        self.head = new_node        

    def display(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> " )
            temp = temp.next

    def delete__list(self, data):
        temp = self.head
        while temp:
            if temp.data == data:
                temp.next = temp.next.next
                break
            
            temp = temp.next
            print("Data Tidak Ditemukan")

    def search__list(self, data):
        temp = self.head
        while temp:
            if temp.data == data:
                print("Data Ditemukan")
                break
            temp = temp.next
            print("Data Tidak Ditemukan")
ll = linkedlist()
ll.add__list(30)
print("Cetak Linked List")
ll.display()
ll.add__list(20)
ll.add__list(10)
print("Cetak Linked List")
ll.display()
ll.delete__list(10)
print("Cetak Linked List")
ll.display()
ll.search__list(20)
ll.display()