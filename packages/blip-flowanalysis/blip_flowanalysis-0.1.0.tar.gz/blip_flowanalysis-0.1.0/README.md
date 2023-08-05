# Blip Flow Analysis
Blip Flow Analysis provides a solution for chatbot constructors to identify problems in flow structure 
that can be originated from bad structuring or poor organization.

# Installation
Use [pip](https://pip.pypa.io/en/stable/) to install:

```shell script
pip install blip_flowanalysis
```

# Usage
Using the `MissingTrackigns` analyse:
```python
import blip_flowanalysis as bfa

# replace __chatbot_as_json__ param for your json bot
bot = bfa.Flow(__chatbot_as_json__)
analyser = bfa.MissingTrackings(minimum=1)

# return `True` if the chatbot has at least `minimum` tracking
print(analyser.analyse(bot)) 
```

# Author
[Take Data&Analytics Research](anaytics.dar@take.net)

# License
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)