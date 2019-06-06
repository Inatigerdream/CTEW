#autograd

import torch
from torch.autograd import Variable

x = Variable(torch.ones(2,2), requires_grad=True)
print(x)

y = x + 2
print(y)

# y was created as a result from an operation so it has grad_fn
print(y.grad_fn)

z = y * y * 3
out = z.mean()
print(z, out)

#backpropagation

out.backward()

print(x.grad)

# "crazy" example 2
x = torch.randn(3)
x = Variable(x, requires_grad=True)

y = x * 2
while y.data.norm() < 1000:
    y = y * 2

print(y)

# "crazy" example 3
gradients = torch.FloatTensor([0.1, 1.0, 0.0001])
y.backward(gradients)

print(x.grad)
