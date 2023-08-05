# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deadbeats']
install_requires = \
['datetime>=4.3,<5.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['deadbeats = deadbeats:main']}

setup_kwargs = {
    'name': 'deadbeats',
    'version': '0.3.1',
    'description': '',
    'long_description': '# DEADBEATS\n\nAn easy to use Slack messaging library for research.\n\n## Usage\n\n```python\nfrom deadbeats import DEADBEATS\n# set environment variables as below\n# SLACK_ACCESS_TOKEN=xxxx-xxxxxxxxxxxxx-xxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx (Get your own Slack API access token)\n# SLACK_CHANNEL_ID=deadbeats (set slack channel id whatever you like!)\n\n\n# or you can set configurations manually.\nDEADBEATS.set_access_token("SLACK_ACCESS_TOKEN")\nDEADBEATS.set_channel_id("SLACK_CHANNEL_ID")\n\n\n# `DEADBEATS.wrap` sends a message at the beginning and end of the function.\n# `DEADBEATS.wrap` catch every errors and raise it after sending a error message.\n@DEADBEATS.wrap\ndef main():\n    # A simple "heartbeating" message.\n    DEADBEATS.ping()\n\n\n    # Start threading!\n    # All subsequent messages will be sent to the thread.\n    DEADBEATS.start_thread()\n\n\n    # You can add extra information like below.\n    params = {"loss": 0.5, "val_loss": 1.6, "acc": 100.0}\n    DEADBEATS.ping(text="message whatever you like", params=params, additional="info", huga="huga")\n\n\n    # If you want to stop threading, you can use this method.\n    # This method reset "thread_ts" of a instance variable, which is a id of thread.\n    DEADBEATS.reset_thread()\n```\n\n## With PyTorch Lightning\n\n```python\nfrom deadbeats import DEADBEATS\n\nclass MyModel(pl.LightningModule):\n\n    ...\n\n    def on_train_start(self):\n        DEADBEATS.start_thread()\n\n    ...\n\n    def validation_epoch_end(self, outputs):\n        avg_loss = torch.stack([x[\'val_loss\'] for x in outputs]).mean()\n\n        DEADBEATS.ping(val_loss = avg_loss, current_epoch = self.current_epoch)\n\n        return {\'val_loss\': avg_loss}\n\n    ...\n\n    # custom training function\n    @DEADBEATS.wrap\n    def fit(self, trainer):\n        trainer.fit(self)\n\n```\n\n\n## messages like below\n\n![example](.github/images/example_message.png)\n\n\n\nThis library is named after the wonderful work of [Mori Calliope](https://www.youtube.com/channel/UCL_qhgtOy0dy1Agp8vkySQg), [DEAD BEATS](https://youtu.be/6ydgEipkUEU), and inspired by [hugginface/knockknock](https://github.com/huggingface/knockknock).\n\n',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpprc/deadbeats',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
