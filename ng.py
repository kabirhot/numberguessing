from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = 'numberguessing_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    session['number'] = random.randint(1, 10)
    session['attempts'] = 0
    return jsonify({'status': 'started'})

@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.json
    guess = data.get('guess')
    
    if 'number' not in session:
        return jsonify({'error': 'Game not started'}), 400
    
    try:
        guess = int(guess)
        if guess < 1 or guess > 10:
            return jsonify({'error': 'Please enter a number between 1 and 10'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400
    
    session['attempts'] = session.get('attempts', 0) + 1
    number = session['number']
    
    if guess == number:
        return jsonify({
            'result': 'correct',
            'message': f'Congratulations! You guessed it right in {session["attempts"]} attempts!',
            'attempts': session['attempts']
        })
    elif guess < number:
        return jsonify({
            'result': 'low',
            'message': 'Too low! Try again.',
            'attempts': session['attempts']
        })
    else:
        return jsonify({
            'result': 'high',
            'message': 'Too high! Try again.',
            'attempts': session['attempts']
        })

@app.route('/reset', methods=['POST'])
def reset_game():
    session.clear()
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


