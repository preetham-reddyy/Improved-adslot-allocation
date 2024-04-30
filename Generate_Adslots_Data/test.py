class YourSampler(torch.utils.data.sampler.Sampler):
    def __init__(self, mask, data_source):
        self.mask = mask
        self.data_source = data_source

    def __iter__(self):
        mask = mask[torch.randperm(mask.size()[0])]
        return iter([i.item() for i in torch.nonzero(mask)])

    def __len__(self):
        return len(self.data_source)

mnist = datasets.MNIST(root=dataroot, train=True, download=True, transform = transform)    
mask = [1 if mnist[i][1] == 5 else 0 for i in range(len(mnist))]
mask = torch.tensor(mask)   
sampler = YourSampler(mask, mnist)
trainloader = torch.utils.data.DataLoader(mnist, batch_size=batch_size,sampler = sampler, shuffle=False, num_workers=workers)

class YourSampler(torch.utils.data.sampler.Sampler):
    def __init__(self, mask, data_source):
        self.mask = mask
        self.data_source = data_source

    def __iter__(self):
        # mask = mask[torch.randperm(mask.size()[0])]
        return iter([i.item() for i in torch.nonzero(mask)])

    def __len__(self):
        return len(self.data_source)

mnist = datasets.MNIST(root=dataroot, train=True, download=True, transform = transform)    
mask = [1 if mnist[i][1] == 5 else 0 for i in range(len(mnist))]
mask = torch.tensor(mask) 
temp = torch.randperm(mask.size()[0])
mask = mask[temp]
mnist = mnist[temp]
 
sampler = YourSampler(mask, mnist)
trainloader = torch.utils.data.DataLoader(mnist, batch_size=batch_size,sampler = sampler, shuffle=False, num_workers=workers)

