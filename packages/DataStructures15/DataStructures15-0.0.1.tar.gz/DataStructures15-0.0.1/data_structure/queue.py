class Queue:

  def __init__(self):
      self.queue = list()

  def insert(self,dataval):
      if dataval not in self.queue:
          self.queue.insert(0,dataval)
          return f"{dataval} inserted"
      return False

  def remove(self):
      if len(self.queue) > 0:
          return self.queue.pop()
      return ("No elements in Queue!")


  def size(self):
      return len(self.queue)

