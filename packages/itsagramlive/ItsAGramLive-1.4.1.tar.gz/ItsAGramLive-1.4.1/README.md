![GitHub](https://img.shields.io/github/license/harrypython/itsagramlive)
![PyPI](https://img.shields.io/pypi/v/itsagramlive)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/harrypython/itsagramlive?label=Version)

# It's A Gram Live

It's A Gram Live is a Python script that create a Instagram Live and provide you a rtmp server and stream key to streaming using sofwares like [OBS-Studio](https://obsproject.com/) or [XSplit Broadcaster](https://www.xsplit.com/).

## Installation

```bash
pip install ItsAGramLive
```

## Usage

```python
from ItsAGramLive import ItsAGramLive

live = ItsAGramLive()

# or if you want to pre-define the username and password without args
# live = ItsAGramLive(
#    username='foo',
#    password='bar'
# )

live.start()
```

```bash
python3 live_broadcast.py -u yourInstagramUsername -p yourPassword -proxy user:password@ip:port
```

The output will give you the RTMP Server address and the Stream key (automatically copied to your clipboard)

## Commands

- **info**
  Show details about the broadcast
- **mute comments**
  Prevent viewers from commenting
- **unmute comments**
  Allow viewers do comments
- **viewers**
  List viewers
- **chat**
  Send a comment
- **comments**
  Get the list of comments
- **wave**
  Wave to a viewer
- **stop**
  Terminate broadcast

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[ GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)

## Buy me a coffee

<a href="https://www.buymeacoffee.com/harrypython" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 37px !important;" ></a>

## Instagram Bot
Check my Instagram Bot: [BurbnBot](https://github.com/harrypython/BurbnBot)
