from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

app = Flask(__name__)

# 업로드된 파일 저장 경로
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 게시물 데이터를 저장할 JSON 파일 경로
DATA_FILE = 'data.json'

# 게시물 데이터 로드 함수
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# 게시물 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 홈 페이지 - 공지사항 가져오기
@app.route('/')
def index():
    data = load_data()
    notices = {post_id: post for post_id, post in data.items() if post.get('category') == '공지사항'}
    return render_template('index.html', notices=notices)

# 동아리 소개 페이지
@app.route('/dongsogae')
def dongsogae():
    return render_template('dongsogae.html')

# 운영진 페이지
@app.route('/web3')
def web3():
    return render_template('web3.html')

# 게시판 페이지
@app.route('/board')
def board():
    data = load_data()
    return render_template('board.html', data=data)

# 문의 페이지
@app.route('/dm')
def dm():
    return render_template('dm.html')

# 이미지 파일을 서빙하는 라우트
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 게시물 상세 페이지
@app.route('/post/<int:post_id>')
def post(post_id):
    data = load_data()
    post_data = data.get(str(post_id))
    if post_data:
        return render_template('post.html', post=post_data)
    else:
        return "게시물을 찾을 수 없습니다.", 404

# 게시물 업로드 페이지
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        file = request.files['file']

        # 파일 저장 처리
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

        # 게시물 데이터 저장
        data = load_data()
        post_id = str(len(data) + 1)  # 게시물 ID는 숫자로 설정
        data[post_id] = {
            'title': title,
            'content': content,
            'category': category,
            'file': file.filename
        }
        save_data(data)

        return redirect(url_for('board'))

    return render_template('upload.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
