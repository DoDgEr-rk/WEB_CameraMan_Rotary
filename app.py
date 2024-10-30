from flask import Flask, render_template, request, redirect, url_for, session
import random
import os
import signal

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Use a secret key for session management


@app.route('/IMS', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Опитай да вземеш номера на камерите от първия формуляр
            camera_num_input = request.form.get('camera_num')
            camera_nums_input = request.form.get('camera_nums')

            if camera_nums_input:
                # Въведен е списък с номера на камерите
                camera_nums = [int(num.strip()) for num in camera_nums_input.split(',') if num.strip().isdigit()]
                if not camera_nums:
                    raise ValueError("You must enter at least one valid camera number.")
                random.shuffle(camera_nums)
                session['cameras'] = camera_nums
            elif camera_num_input:
                # Въведен е един брой
                all_camera_num = int(camera_num_input)
                if all_camera_num <= 0:
                    raise ValueError("Number of cameras must be greater than zero.")

                # Генериране на списък от случайни камери
                cameras = random.sample(range(1, all_camera_num + 1), all_camera_num)
                session['cameras'] = cameras

            return redirect(url_for('enter_names'))

        except ValueError as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')


@app.route('/enter_names', methods=['GET', 'POST'])
def enter_names():
    if 'cameras' not in session:
        return redirect(url_for('index'))

    cameras = session['cameras']  # Вземи списъка с камери от сесията
    all_camera_num = len(cameras)  # Определи броя на камерите

    if request.method == 'POST':
        try:
            # Събери имената от формата
            name_list = [request.form.get(f'name_{i}', '') for i in range(all_camera_num)]

            # Провери дали имаме достатъчно имена
            if len(name_list) != all_camera_num or any(name.strip() == '' for name in name_list):
                raise ValueError("Not enough names provided or some names are empty.")

            final_list = [f'{name_list[i]} on camera {cameras[i]}' for i in range(all_camera_num)]

            # Изчисти данните от сесията
            session.pop('cameras', None)

            return render_template('result.html', final_list=final_list)

        except ValueError as e:
            return render_template('enter_names.html', cameras=cameras, error=str(e))

    return render_template('enter_names.html', cameras=cameras, all_camera_num=all_camera_num)  # Предай и броя на камерите


@app.route('/exit', methods=['POST'])
def exit():
    # Clear the session data
    session.pop('camera_num', None)
    session.pop('cameras', None)
    return redirect(url_for('bye_bye'))


@app.route('/bye_bye')
def bye_bye():
    return render_template('bye_bye.html')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "Server shutting down..."


def shutdown_server():
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
