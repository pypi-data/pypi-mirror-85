import json
import logging
from pathlib import Path
from typing import Union, Optional

import torch


class CheckpointSaver:
    def __init__(self, path: Union[Path, str], logger=None):
        """
        Saves and loads checkpoints of the model together with optimizer and scheduler.
        """
        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, model, optimizer, scheduler, epoch: int):
        """
        Saves the state of the model, optimizer and scheduler to the files corresponding to the given epoch index.
        """
        name_model = self._name_model(epoch)
        self._save_to_fname(model, name_model)

        name_optimizer = self._name_optimizer(epoch)
        self._save_to_fname(optimizer, name_optimizer)

        name_scheduler = self._name_scheduler(epoch)
        self._save_to_fname(scheduler, name_scheduler)

        meta = {
            'epoch': epoch,
            'model': name_model,
            'scheduler': name_scheduler,
            'optimizer': name_optimizer
        }
        path_meta = self.path.joinpath(self._name_meta(epoch))
        with path_meta.open("w") as f:
            json.dump(meta, f)

        self.logger.debug(f"saved meta data {meta} to {path_meta}")

    def load(self, model, optimizer, scheduler, epoch: int):
        """
        Loads the state of the model, optimizer and scheduler from the files corresponding to the given epoch index.
        """
        path_meta = self.path.joinpath(self._name_meta(epoch))
        with path_meta.open() as f:
            meta = json.load(f)

        name_model = meta['model']
        name_optimizer = meta['optimizer']
        name_scheduler = meta['scheduler']

        self._load_module_with_update('model', model, self.path.joinpath(name_model))
        self._load_module_optional('optimizer', optimizer, self.path.joinpath(name_optimizer))
        self._load_module_optional('scheduler', scheduler, self.path.joinpath(name_scheduler))

    def find_last(self, start_epoch, end_epoch) -> Optional[int]:
        for epoch in range(end_epoch, start_epoch - 1, -1):
            path = self.path.joinpath(self._name_meta(epoch))
            if path.exists():
                return epoch
        return None

    def _save_to_fname(self, module, fname: str):
        torch.save(module.state_dict(), self.path.joinpath(fname))

    def _name_meta(self, epoch: int) -> str:
        return "epoch_{epoch:05d}.meta.json".format(epoch=epoch)

    def _name_scheduler(self, epoch: int) -> str:
        return "epoch_{epoch:05d}.scheduler.pth".format(epoch=epoch)

    def _name_optimizer(self, epoch: int) -> str:
        return "epoch_{epoch:05d}.optimizer.pth".format(epoch=epoch)

    def _name_model(self, epoch: int) -> str:
        return "epoch_{epoch:05d}.pth".format(epoch=epoch)

    def _load_module_with_update(self, module_name: str, dst_module, path: Path):
        self.logger.debug(f"loading {module_name} from {path}")
        pretrained_dict = torch.load(path)
        module_dict = dst_module.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in module_dict}
        module_dict.update(pretrained_dict)
        dst_module.load_state_dict(module_dict)

    def _load_module_optional(self, module_name: str, dst_module, path: Path):
        if path.exists():
            self.logger.debug(f"loading {module_name} state from {path}")
            module_dict = torch.load(path)
            dst_module.load_state_dict(module_dict)
        else:
            self.logger.debug(f"{module_name} state not found")
