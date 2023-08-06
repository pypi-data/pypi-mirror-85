import ntpath
import uuid

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def gen_uuid(lst_length):
  output = []
  for i in range(0, lst_length):
    output.append(str(uuid.uuid4()))

  if len(output) == 1:
    return output[0]
  else:
    return output