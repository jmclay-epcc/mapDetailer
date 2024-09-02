import os
from PIL import Image
from torch.utils.data import Dataset
from super_image import Trainer, TrainingArguments, EdsrModel, EdsrConfig
from torchvision.transforms import Compose, ToTensor

class LocalDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.lr_dir = os.path.join(root_dir, 'lr')
        self.hr_dir = os.path.join(root_dir, 'hr')
        
        # List all files in lr and hr directories
        self.lr_image_paths = [os.path.join(self.lr_dir, img) for img in os.listdir(self.lr_dir)
                            if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'))]
        self.hr_image_paths = [os.path.join(self.hr_dir, img) for img in os.listdir(self.hr_dir)
                            if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'))]
        
        # Assuming lr and hr images are named similarly
        self.lr_image_paths.sort()
        self.hr_image_paths.sort()
        
        if len(self.lr_image_paths) != len(self.hr_image_paths):
            raise ValueError("Mismatch between number of LR and HR images.")

    def __len__(self):
        return len(self.lr_image_paths)
    
    def __getitem__(self, idx):
        lr_img_path = self.lr_image_paths[idx]
        hr_img_path = self.hr_image_paths[idx]
        
        try:
            lr_image = Image.open(lr_img_path).convert('RGB')
            hr_image = Image.open(hr_img_path).convert('RGB')
        except (IOError, OSError) as e:
            print(f"Error opening image {lr_img_path} or {hr_img_path}: {e}")
            raise e
        
        if self.transform:
            lr_image = self.transform(lr_image)
            hr_image = self.transform(hr_image)
        
        return lr_image, hr_image
    

# Define transformations
transform = Compose([
    ToTensor()
])

# Update dataset initialization
train_dataset = LocalDataset(root_dir='./data/train', transform=transform)
eval_dataset = LocalDataset(root_dir='./data/val', transform=transform)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=100,
)

config = EdsrConfig(
    scale=2,
)
model = EdsrModel(config)

# Update the Trainer usage if needed
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  # Use Dataset, not DataLoader
    eval_dataset=eval_dataset     # Use Dataset, not DataLoader
)

trainer.train()
