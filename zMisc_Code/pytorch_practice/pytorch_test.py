from __future__ import print_function
import torch

#construct a 5x3 matrix uninitialized
x = torch.Tensor(5,3)
print(x)

#construct a randomly initialized matrix
x = torch.rand(5,3)
print(x)
print(x.size())

#operations
#addition
y = torch.rand(5,3)
print(x + y)

#addition v2
print(torch.add(x,y))

#give output tensor
result = torch.Tensor(5,3)
torch.add(x,y,out=result)
print(result)

#resize with torch.view
x = torch.randn(4,4)
y = x.view(16)
z = x.view(-1, 8) #use -1 to infer size from other dimensions
print(x, y, z)
print(x.size(), y.size(), z.size())


# convert numpy array to pytorch tensor
import numpy as np

a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)