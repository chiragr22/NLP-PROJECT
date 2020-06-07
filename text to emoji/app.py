from flask import Flask, render_template, request, url_for, redirect
import text_to_emoji
app = Flask(__name__)
@app.route('/') 
def run_app(): 
    return render_template('index.html')
@app.route('/result')
def result():
    question = request.args.get('jsdata')
    print(question)
    answer = ""
    possible_emojis = {}
    words_set = []
    if question:
        emojis_dict = text_to_emoji.load_emojis_json('emojis.json')
        answer, possible_emojis, words_set = text_to_emoji.text_to_emoji(emojis_dict, question)

    return render_template('result.html', answer=answer, possible_emojis=possible_emojis, words_set=words_set)

if __name__ == '__main__':
    app.run(debug=True) 