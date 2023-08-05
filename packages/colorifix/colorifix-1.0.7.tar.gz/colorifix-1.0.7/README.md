# Setup

```
pip3 install colorifix
```

# Requirements
* Python 3.6+

# Import
```python
from colorifix.colorifix import paint, random, sample
from colorifix.colorifix import Color, Background, Style
```

# Usage
There are 2 main functions, one to color a string and one to randomize color, background and style of a string.
```python
from colorifix.colorifix import paint, random
from colorifix.colorifix import Color, Background, Style

paint('String to color',color=Color.RED)
paint('String to color',background=Background.GREEN,style=(Style.BOLD,Style.UNDERLINE))
paint('String to color',color=34,background=27)

random('YOLO',color=True,background=True)
random('YOLO',color=True,style=True)
random('YOLO',background=True)
```

# Colors
You can choose from the default colors for text and background  
`RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`, `GRAY` and `BLACK`
or a number between 0 and 256.  

For styles you can choose from  
`BOLD`, `UNDERLINE`, `DIM`, `BLINK`, `REVERSE` and `HIDDEN`.  

### Sample
To disaply all different colors you can use the function `sample`
```python
from colorifix.colorifix import sample

sample('color')            # default colors
sample('background')
sample('style')
sample('color',True)       # all colors
sample('background',True)
```