from random import choice,randint

class Color:
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[97m'
	GRAY = '\033[37m'
	BLACK = '\033[30m'

class Background:
	RED = '\033[101m'
	GREEN = '\033[102m'
	YELLOW = '\033[103m'
	BLUE = '\033[104m'
	MAGENTA = '\033[105m'
	CYAN = '\033[106m'
	WHITE = '\033[107m'
	GRAY = '\033[100m'
	BLACK = '\033[40m'

class Style:
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	DIM = '\033[2m'
	BLINK = '\033[5m'
	REVERSE = '\033[7m'
	HIDDEN = '\033[8m'

RESET = '\033[0m'
ERASE = '\x1b[1A\x1b[2K'

def _build_color(number): return f'\033[38;5;{number}m'

def _build_background(number): return f'\033[48;5;{number}m'

def _check_type(var,what,name,style=False):
	if not var: return True
	if not style and isinstance(var,int) and var not in range(257): raise ValueError(f'{name} number must be between 0 and 256.')
	if isinstance(var,str) and var not in what.__dict__.values(): raise TypeError(f"{name} must be a {name} in {' or '.join(c for c in what.__dict__ if c == c.upper())}")
	if not style and isinstance(var,(int,str)): return True
	if style and isinstance(var,(str)): return True
	if not style: raise TypeError(f'{name} must be an integer (between 0 and 256) or a {name} type')
	raise TypeError(f'{name} must be a {name} type')

def paint(string,color=None,background=None,style=None):
	# type checking
	_check_type(color,Color,'Color')
	_check_type(background,Background,'Background')
	if style: 
		if type(style) is not tuple: style = (style,)
		for s in style: _check_type(s,Style,'Style',True)
	# build color from ints
	if isinstance(color,int): color = _build_color(color)
	if isinstance(background,int): background = _build_background(background)
	# to string
	color = color or ''
	background = background or ''
	style = ''.join(style) if style else ''
	return f'{color}{style}{background}{string}{RESET}'

def random(string=None,color=None,background=None,style=None):
	if color: color = choice([c for k,c in Color.__dict__.items() if k == k.upper()])
	if background: background = choice([b for k,b in Background.__dict__.items() if k == k.upper()])
	if style: style = tuple(set([choice([s for k,s in Style.__dict__.items() if k == k.upper()]) for _ in range(randint(1,4))]))
	return paint(string,color,background,style)

def sample(mode,complete=False):
	red = paint(' RED ',Color.RED) if mode == 'color' else paint(' RED ',Color.BLACK,Background.RED)
	green = paint(' GREEN ',Color.GREEN) if mode == 'color' else paint(' GREEN ',Color.BLACK,Background.GREEN)
	yellow = paint(' YELLOW ',Color.YELLOW) if mode == 'color' else paint(' YELLOW ',Color.BLACK,Background.YELLOW)
	blue = paint(' BLUE ',Color.BLUE) if mode == 'color' else paint(' BLUE ',Color.BLACK,Background.BLUE)
	magenta = paint(' MAGENTA ',Color.MAGENTA) if mode == 'color' else paint(' MAGENTA ',Color.BLACK,Background.MAGENTA)
	cyan = paint(' CYAN ',Color.CYAN) if mode == 'color' else paint(' CYAN ',Color.BLACK,Background.CYAN)
	white = paint(' WHITE ',Color.WHITE) if mode == 'color' else paint(' WHITE ',Color.BLACK,Background.WHITE)
	gray = paint(' GRAY ',Color.GRAY) if mode == 'color' else paint(' GRAY ',Color.BLACK,Background.GRAY)
	black = paint(' BLACK ',Color.BLACK,Background.WHITE) if mode == 'color' else paint(' BLACK ',Color.WHITE,Background.BLACK)
	bold = paint(' BOLD ',style=Style.BOLD)
	underline = paint(' UNDERLINE ',style=Style.UNDERLINE)
	dim = paint(' DIM ',style=Style.DIM)
	blink = paint(' BLINK ',style=Style.BLINK)
	reverse = paint(' REVERSE ',style=Style.REVERSE)
	hidden = paint(' HIDDEN ',background=Background.WHITE,style=Style.HIDDEN)
	if mode in ('color','background'): print(f'{red} {green} {yellow} {blue} {magenta} {cyan} {white} {gray} {black}\n\n{_sample_all(mode) if complete else ""}')
	elif mode == 'style': print(f'{bold} {underline} {dim} {blink} {reverse} {hidden}')
	else: raise ValueError('mode must be color, background or style')

def _sample_all(mode):
	if mode == 'color': return ''.join([paint(f'{i:>5}',i) for i in range(4)])+'\n'+''.join([paint('{:>5}{}'.format(i+3,'\n' if not i%6 and i != 252 else ''),i+3) for i in range(1,253)])
	else: return ''.join([paint(f'{i:>4} ',background=i) for i in range(4)])+'\n'+''.join([paint('{:>4} {}'.format(i+3,'\n' if not i%6 and i != 252 else ''),background=i+3) for i in range(1,253)])

def erase(lines=1): print(ERASE*lines)
