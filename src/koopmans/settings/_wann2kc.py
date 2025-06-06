from typing import Any, Dict, List

from ase_koopmans.io.espresso import w2kcw_keys

from ._utils import SettingsDict, kcw_defaults


class Wann2KCSettingsDict(SettingsDict):
    """Settings for a wann2kcw calculator."""

    def __init__(self, **kwargs) -> None:

        # Get rid of any nested kwargs
        flattened_kwargs: Dict[str, Any] = {}
        for k, v in kwargs.items():
            if isinstance(v, dict):
                flattened_kwargs.update(**v)
            else:
                flattened_kwargs[k] = v

        super().__init__(valid=[k for block in w2kcw_keys.values() for k in block],
                         defaults={'calculation': 'wann2kcw', **kcw_defaults},
                         are_paths=['outdir', 'pseudo_dir'],
                         **flattened_kwargs)

    @property
    def _other_valid_keywords(self) -> List[str]:
        return ['kgrid']

    def __setitem__(self, key: str, value: Any):
        if key == 'kgrid':
            assert isinstance(value, list)
            assert len(value) == 3
            for i, x in enumerate(value):
                self.__setitem__(f'mp{i + 1}', x)
        else:
            return super().__setitem__(key, value)
