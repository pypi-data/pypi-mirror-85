import PIL.Image
import numpy as np
import torch
import torchvision.transforms.functional as tvf

imagenet_stats = dict(mean=[0.485, 0.456, 0.406],
                      std=[0.229, 0.224, 0.225])


class UnNormalize_(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, tensor):
        for t, m, s in zip(tensor, self.mean, self.std):
            t.mul_(s).add_(m)
        return tensor


def tfm_vis_img(tensor, size=None, unnormalize_img=UnNormalize_(**imagenet_stats)):
    unnormalized = unnormalize_img(tensor.detach().clone())
    img = tvf.to_pil_image(unnormalized, mode='RGB')
    if size is not None:
        img = tvf.resize(img, size, interpolation=PIL.Image.NEAREST)
    return np.array(img)


def tfm_vis_mask(tensor, size=None):
    img = tvf.to_pil_image(tensor.detach().type(torch.IntTensor), mode='I')
    if size is not None:
        img = tvf.resize(img, size, interpolation=PIL.Image.NEAREST)
    return np.array(img)


DEFAULT_KWARGS_IMG = {'interpolation': 'nearest'}
DEFAULT_KWARGS_MASK = {'interpolation': 'nearest', 'cmap': 'tab20', 'vmin': 0, 'vmax': 20}


class ImgShow:
    def __init__(self, ax=None, size=None,
                 tfm_img=tfm_vis_img, tfm_mask=tfm_vis_mask,
                 show_kwargs_img=None, show_kwargs_mask=None):
        """
        Class for visualization of tensors representing images.
        Sample usage:
        >>> from pytorch_nn_tools.visual import ImgShow
        >>> import matplotlib.pyplot as plt # doctest: +SKIP
        >>> ish = ImgShow(ax=plt) # doctest: +SKIP
        >>> _ = ish.show_image(torch.rand(3, 10, 20)) # doctest: +SKIP
        """
        if show_kwargs_mask is None:
            show_kwargs_mask = DEFAULT_KWARGS_MASK
        if show_kwargs_img is None:
            show_kwargs_img = DEFAULT_KWARGS_IMG
        self.ax = ax
        self.size = size
        self.tfm_img = tfm_img
        self.tfm_mask = tfm_mask
        self.show_kwargs_img = show_kwargs_img
        self.show_kwargs_mask = show_kwargs_mask

    def with_axes(self, ax):
        return ImgShow(ax=ax, size=self.size, tfm_img=self.tfm_img, tfm_mask=self.tfm_mask,
                       show_kwargs_img=self.show_kwargs_img,
                       show_kwargs_mask=self.show_kwargs_mask)

    def with_size(self, size):
        return ImgShow(ax=self.ax, size=size, tfm_img=self.tfm_img, tfm_mask=self.tfm_mask,
                       show_kwargs_img=self.show_kwargs_img,
                       show_kwargs_mask=self.show_kwargs_mask
                       )

    def show_image(self, tensor):
        self._check_axes()
        img = self.tfm_img(tensor, size=self.size)
        self.ax.imshow(img, **self.show_kwargs_img)
        return self

    def show_mask(self, tensor):
        self._check_axes()
        img = self.tfm_mask(tensor, size=self.size)
        self.ax.imshow(img, **self.show_kwargs_mask)
        return self

    def _check_axes(self):
        if self.ax is None:
            raise ValueError("Axes are not initialized for ImageShow object")
