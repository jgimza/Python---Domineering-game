from flask import Flask, flash, redirect, request, url_for, render_template
from wtforms import Form, IntegerField, RadioField, validators
from Board import Board
from Player import Player
from Computer import Computer

app = Flask(__name__) 

board = None
total = None
players = None
turn = 0
piony = []
poziomy = []
cpu = 0
difficulty = 0
coliterr2 = 0
coliterr4 = 0
coliterr6 = 0
coliterr8 = 0

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/zasady')
def zasady():
		return render_template('zasady.html')
@app.route('/gra')
def gra():
    return render_template('gra.html')
	
@app.route('/start', methods=['GET', 'POST'])
def start():
    form = GameSettings(request.form)
    if request.method == 'POST' and form.validate():
        global board
        board = Board(form.szerokosc.data, form.wysokosc.data)
        global players
        global cpu
        global difficulty
        diff_reset()
        if (form.typ_gry.data == 'cpu'):
            players = [Player(), Computer()]
            cpu = 1
            if (form.poziom_trudnosci.data == 'ez'):
                difficulty = '1'
            elif (form.poziom_trudnosci.data == 'hd'):
                difficulty = '2'
        else:
            players = [Player(), Player()]
            cpu = 0
        turn_reset()
        reset_hard_moves()
        global piony
        piony = [(x,y) for x in range(0,form.wysokosc.data-1) for y in range (0,form.wysokosc.data)]
        global poziomy
        poziomy = [(x,y) for x in range (0,form.szerokosc.data) for y in range (0,form.szerokosc.data-1)]
        return redirect(url_for('nowagra'))
    return render_template('start.html', form = form)
	

@app.route('/nowagra')
@app.route('/nowagra/<string:direction>/<int:row>/<int:col>')
def nowagra(direction=None, row=None, col=None):
	global coliterr2
	global coliterr4
	global coliterr6
	global coliterr8
	total = board.szerokosc * board.wysokosc
	if cpu == 0:
		if turn % 2 == 0:
			if (row,col) in piony and row is not None and col is not None and direction == 'vertical':
				board.pionowa[row][col] = True
				remove_move_pion(row, col)
				players[0].get_score()
				turn_switch()
				if len(poziomy) == 0:
					return redirect(url_for('game_over'))
				
		elif turn % 2 != 0:
			if (row,col) in poziomy and row is not None and col is not None and direction == 'horizontal':
				board.pozioma[row][col] = True
				remove_move_poziom(row, col)
				players[1].get_score()
				turn_switch()
				if len(piony) == 0:
					return redirect(url_for('game_over2'))
					
	elif cpu == 1:
		if turn % 2 == 0:
			if (row,col) in piony and row is not None and col is not None and direction == 'vertical':
				board.pionowa[row][col] = True
				remove_move_pion(row, col)
				players[0].get_score()
				turn_switch()
				if len(poziomy) == 0:
					p1win = True
					return redirect(url_for('game_over'))
					
				if difficulty == '1':
					direction = 'horizontal'
					for (row, col) in poziomy:
						if row is not None and col is not None and direction == 'horizontal':
							board.pozioma[row][col] = True
							remove_move_poziom(row, col)
							players[1].get_score()
							turn_switch()
							if len(piony) == 0:
								return redirect(url_for('game_over2'))
							break
				
				elif difficulty =='2':
					direction = 'horizontal'
					row = board.wysokosc-2
					col = coliterr2
					if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
						board.pozioma[row][col] = True
						remove_move_poziom(row, col)
						players[1].get_score()
						turn_switch()
					elif (row,col) not in poziomy or row is None or col is None:
						coliterr2 = coliterr2+2
						col = coliterr2
						if (row, col) in poziomy and row is not None and col is not None and direction =='horizontal':
							board.pozioma[row][col] = True
							remove_move_poziom(row, col)
							players[1].get_score()
							turn_switch()
						elif (row,col) not in poziomy or row is None or col is None:
							row = board.wysokosc-4
							col = coliterr4
							if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
								board.pozioma[row][col] = True
								remove_move_poziom(row, col)
								players[1].get_score()
								turn_switch()
							elif (row,col) not in poziomy or row is None or col is None:
								coliterr4 = coliterr4+2
								col = coliterr4
								if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
									board.pozioma[row][col] = True
									remove_move_poziom(row, col)
									players[1].get_score()
									turn_switch()
								elif (row,col) not in poziomy or row is None or col is None:
									row = board.wysokosc-6
									col = coliterr6
									if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
										board.pozioma[row][col] = True
										remove_move_poziom(row, col)
										players[1].get_score()
										turn_switch()
									elif (row,col) not in poziomy or row is None or col is None:
										coliterr6 = coliterr6+2
										col = coliterr6
										if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
											board.pozioma[row][col] = True
											remove_move_poziom(row, col)
											players[1].get_score()
											turn_switch()
										elif (row,col) not in poziomy or row is None or col is None:
											row = board.wysokosc-8
											col = coliterr8
											if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
												board.pozioma[row][col] = True
												remove_move_poziom(row, col)
												players[1].get_score()
												turn_switch()
											elif (row,col) not in poziomy or row is None or col is None:
												coliterr8 = coliterr8+2
												col = coliterr8
												if (row,col) in poziomy and row is not None and col is not None and direction =='horizontal':
													board.pozioma[row][col] = True
													remove_move_poziom(row, col)
													players[1].get_score()
													turn_switch()
												elif (row,col) not in poziomy or row is None or col is None:
													for (row, col) in poziomy:
														if (row,col) in poziomy and row is not None and col is not None and direction == 'horizontal':
															board.pozioma[row][col] = True
															remove_move_poziom(row, col)
															players[1].get_score()
															turn_switch()
															if len(piony) == 0:
																return redirect(url_for('game_over2'))
															break
	return render_template('nowagra.html', board=board, players=players, total=total, turn=turn, piony=piony, poziomy=poziomy, difficulty=difficulty, coliterr2=coliterr2, coliterr4=coliterr4, coliterr6=coliterr6, coliterr8=coliterr8, cpu=cpu)

def reset_hard_moves():
	global coliterr2
	global coliterr4
	global coliterr6
	global coliterr8
	coliterr2 = 0
	coliterr4 = 0
	coliterr6 = 0
	coliterr8 = 0
	
def remove_move_pion(a, b):
	global piony
	global poziomy
	if ((a,b)) in piony:
		piony.remove((a,b))
	if ((a+1,b)) in piony:
		piony.remove((a+1,b))
	if ((a-1,b)) in piony:
		piony.remove((a-1,b))
	if ((a,b)) in poziomy:
		poziomy.remove((a,b))
	if ((a+1,b)) in poziomy:
		poziomy.remove((a+1,b))
	if ((a,b-1)) in poziomy:
		poziomy.remove((a,b-1))
	if ((a+1,b-1)) in poziomy:
		poziomy.remove((a+1,b-1))

def remove_move_poziom(a, b):
	if ((a,b)) in poziomy:
		poziomy.remove((a,b))
	if ((a,b-1)) in poziomy:
		poziomy.remove((a,b-1))
	if ((a,b+1)) in poziomy:
		poziomy.remove((a,b+1))
	if ((a-1,b)) in piony:
		piony.remove((a-1,b))
	if ((a-1,b+1)) in piony:
		piony.remove((a-1,b+1))
	if ((a,b)) in piony:
		piony.remove((a,b))
	if ((a,b+1)) in piony:
		piony.remove((a,b+1))

def diff_reset():
	global difficulty
	difficulty = 0
		
@app.route('/gameover')
def game_over():
    return render_template('gameover.html', players=players)
	
@app.route('/gameover2')
def game_over2():
    return render_template('gameover2.html', players=players)
	
def turn_switch():
	global turn	
	turn = turn +1
	
def turn_reset():
	global turn
	turn = 0
	
	
class GameSettings(Form):
	typ_gry = RadioField('Gracz', choices = [('cpu', 'Komputer'),('hum', 'Człowiek')])
	poziom_trudnosci = RadioField('Poziom trudności (komputer)', [validators.Optional()], choices =[('ez', 'Łatwy'),('hd','Trudny')])
	wysokosc = IntegerField('Wysokosc', [validators.NumberRange(min=5, max=8)])
	szerokosc = IntegerField('Szerokosc', [validators.NumberRange(min=5, max=8)])
	
	def validate(self):
		if not Form.validate(self):
			return False

		a = self.wysokosc.data
		b = self.szerokosc.data
		if a == b:
			return True
		else:
			return False

app.run()