# from flask import Flask, render_template, request, redirect, url_for
#
# app = Flask(__name__)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         try:
#             all_camera_num = int(request.form.get('camera_num', 0))
#             if all_camera_num <= 0:
#                 raise ValueError("Number of cameras must be greater than zero.")
#
#             # Generate list of cameras
#             cameras = list(range(1, all_camera_num + 1))
#
#             # Collect names from the form
#             name_list = [request.form.get(f'name_{i}', '') for i in range(all_camera_num)]
#
#             # Check if we have all required names
#             if len(name_list) != all_camera_num:
#                 raise ValueError("Not enough names provided.")
#
#             # Create final list of name and camera assignments
#             final_list = [f'{name_list[i]} Na kamera {cameras[i]}' for i in range(all_camera_num)]
#
#             return render_template('result.html', final_list=final_list)
#         except ValueError as e:
#             return render_template('index.html', error=str(e))
#
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, debug=True)
