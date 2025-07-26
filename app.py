from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.calculation import calculate_equivalent_exposure, round_shutter_speed, round_iso

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['base_shutter_speed'] = request.form.get('base_shutter_speed')
        session['base_f_value'] = request.form.get('base_f_value')
        session['base_iso'] = request.form.get('base_iso')
        return redirect(url_for('calculate'))
    return render_template('index.html')


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    # セッションから基準設定を取得
    base_shutter_speed = session.get('base_shutter_speed')
    base_f_value = session.get('base_f_value')
    base_iso = session.get('base_iso')

    # 基準設定がない場合はトップにリダイレクト
    if not (base_shutter_speed and base_f_value and base_iso):
        flash('基準設定がありません。最初に設定してください。')
        return redirect(url_for('index'))

    result = None

    if request.method == 'POST':
        # 基準設定を変更したい時
        if 'change_base' in request.form:
            session.clear()
            return redirect(url_for('index'))

        shutter_speed = request.form.get('shutter_speed')
        f_value = request.form.get('f_value')
        iso = request.form.get('iso')

        # 入力チェックと計算ロジック
        inputs = [shutter_speed, f_value, iso]

        # 入力の空欄じゃない数を数える
        filled_count = sum(1 for i in inputs if i != '')

        if filled_count < 2:
            flash('シャッタースピード、F値、ISO感度のうち2つを入力してください。')
        elif filled_count > 2:
            flash('入力は2つだけ入力してください。')
        else:
            result = calculate_equivalent_exposure(base_shutter_speed, base_f_value, base_iso, shutter_speed, f_value, iso)
            if result and result[0]:
                result = (int(result[0]), result[1], int(result[2]))

    return render_template('calculate.html', result=result, base_shutter_speed=base_shutter_speed, base_f_value=base_f_value, base_iso=base_iso)
