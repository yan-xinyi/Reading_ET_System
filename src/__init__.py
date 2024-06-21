import math
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import os
import warnings
from eye.functions import *

app = Flask(__name__)
warnings.filterwarnings("ignore")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '@12345678@')


# Log in
@app.route("/login")
def login():
    return render_template('login.html')


# Log out
@app.route("/login")
def logout():
    return render_template('login.html')


# The user information (here, information is submitted to the frontend using POST, cannot be directly retrieved this definition using a URL).
@app.route("/confirm_user", methods=['post'])
def use_login():
    # Retrieve page information
    user_id = request.form.get('user_id').strip()
    user_pwd = request.form.get('user_pwd').strip()

    # Admin login redirects to a new management page
    if user_id == 'admin' and user_pwd == '000000':
        session['user_id'] = 'Admission'
        session.permanent = True  # Valid for an extended period, specifically one month
        return redirect(url_for("admin_page"))

    # Search for user information
    result = get_password_by_id(user_id)
    if result == None:
        return render_template("login.html", state="Username does not exist!")
    elif user_pwd != result[1]:
        return render_template("login.html", state="Incorrect user password!")
    else:
        session['user_id'] = request.form.get('user_id')
        session.permanent = True  # Valid for an extended period, specifically one month
        return redirect(url_for("index_page"))


# Index page
@app.route('/')
@app.route('/index')
def index_page():
    # Verify login status
    if 'user_id' not in session.keys():
        return redirect(url_for("login"))

    # Retrieve personal information
    user_name = session['user_id']
    # personal_info = get_personal_info(session['user_id']

    # Number of records displayed on the page
    show_num = 5

    # Initial page
    if len(request.args) == 0:
        # Current page
        curr_page = 1
        datas = get_task_list(user_name, 'all')
        item_nums = len(datas)
        all_pages = math.ceil(item_nums / show_num)
        # Display all data
        session['show'] = 'all'
        # Data passed to the frontend
        items = []
        for rank, item in enumerate(datas[0: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            score = 0
            for i, s_item in enumerate(item):
                if i != 2:
                    temp.append(s_item)
                else:
                    temp.append(s_item)
                    pretime = int(0.3 * int(s_item))
                    temp.append(pretime)
            # Check the structure and determine if it has been read based on the 6th item
            items.append(temp)
        return render_template('index.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "datalist": items
        })
    else:
        # Display annotated data
        if request.args.get('show') == 'true':
            session['show'] = 'true'
        elif request.args.get('show') == 'false':
            session['show'] = 'false'
        elif request.args.get('show') == 'all':
            session['show'] = 'all'
        # Current page number
        curr_page = int(request.args.get('curr_page')) \
            if request.args.get('curr_page') != None else 1
        if curr_page == 0:
            curr_page = 1
        # Retrieve data
        datas = get_task_list(user_name, session['show'])
        # Total data count
        item_nums = len(datas)
        # Total number of pages
        all_pages = math.ceil(item_nums / show_num)
        # If the current page exceeds the maximum number of pages, reset to the maximum page number
        if curr_page > all_pages: curr_page = all_pages
        # Process annotated data
        items = []
        for rank, item in enumerate(datas[(curr_page - 1) * show_num: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            score = 0
            for i, s_item in enumerate(item):
                if i != 2:
                    temp.append(s_item)
                else:
                    temp.append(s_item)
                    pretime = int(0.3 * int(s_item))
                    temp.append(pretime)
            items.append(temp)
        return render_template('index.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "show": session['show'],
            "datalist": items
        })


@app.route('/admin')
def admin_page():
    # Check if logged in
    if 'user_id' not in session.keys():
        return redirect(url_for("login"))

    # Retrieve personal information
    user_name = session['user_id']
    # personal_info = get_personal_info(session['user_id']

    # Verify admin identity
    if user_name != "管理员":
        return redirect(url_for("login"))

    # Number of records displayed on the page
    show_num = 5

    # Initial page
    if len(request.args) == 0:
        # Current page
        curr_page = 1
        datas = get_task_list_admin('all')
        item_nums = len(datas)
        all_pages = math.ceil(item_nums / show_num)
        # Display all data
        session['show'] = 'all'
        # Data passed to the frontend
        items = []
        # The enumerate function can obtain the index and content of a list or array
        # Use a for loop to get the information that needs to be displayed on the current page and pass it to the frontend
        # Data format: data index,
        for rank, item in enumerate(datas[0: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            for i, s_item in enumerate(item):
                temp.append(s_item)
            # Inspect the structure and determine if it has been read based on the 6th item
            items.append(temp)
        return render_template('admin.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "datalist": items
        })
    else:
        # Display annotated data
        if request.args.get('show') == 'true':
            session['show'] = 'true'
        elif request.args.get('show') == 'false':
            session['show'] = 'false'
        elif request.args.get('show') == 'all':
            session['show'] = 'all'
        # Current page number
        curr_page = int(request.args.get('curr_page')) \
            if request.args.get('curr_page') != None else 1
        if curr_page == 0: curr_page = 1
        # Retrieve data
        datas = get_task_list_admin(session['show'])
        # Total data count
        item_nums = len(datas)
        # Total number of pages
        all_pages = math.ceil(item_nums / show_num)
        # If the current page exceeds the maximum number of pages, reset it to the maximum page number
        if curr_page > all_pages: curr_page = all_pages
        # Process annotated data
        items = []
        for rank, item in enumerate(datas[(curr_page - 1) * show_num: curr_page * show_num]):
            temp = [(curr_page - 1) * show_num + rank + 1]
            for i, s_item in enumerate(item):
                temp.append(s_item)
            items.append(temp)
        return render_template('admin.html', re_datas={
            "item_nums": item_nums,
            "all_pages": all_pages,
            "curr_page": curr_page,
            "show": session['show'],
            "datalist": items
        })

# Calibration page 1
@app.route('/check_page', methods=['GET'])
def check_page():
    a_id = request.args.get('a_id')
    session['artical_id'] = a_id
    return render_template('check.html')


# Calibration page 2
@app.route('/check2_page')
def check2_page():
    return render_template('check2.html')


# New reading page
# The entire content of the article needs to be passed to the frontend at once, regardless of whether
@app.route('/newcollect_page')
def newcollect_page():
    # Retrieve all sentences of the article based on session and save to 'passage' (list)
    u_id = session['user_id']
    a_id = session['artical_id']
    passage = get_sentence(a_id)
    passage_ids = get_sentence_id(a_id)
    # Retrieve the article title (string)
    # Calculate the total number of sentences
    all_s = len(passage)
    title = get_title(a_id)
    # When first entering, session status is 'first'
    if len(request.args) == 0:
        # Modify task information in the task table (modify 'state' and 'readtime' on first entry)
        change_state(u_id, a_id)
        # Currently on the first sentence
        curr_s = 1
        print(u_id)
        print(passage)
        print(passage_ids)
        print(title)
        # Pass the entire article data to the frontend
        return render_template('newcollect.html', re_datas={
            "u_id": u_id,
            "a_id": a_id,
            "all_s": all_s,
            "title": title,
            "sentence": passage,
            "sentence_id": passage_ids,
            "curr_s":curr_s
        })


# Reset task
@app.route('/resetTask', methods=['POST'])
def reset_task():
    a_id = request.form.get("a_id")  # Article ID
    u_id = request.form.get("u_id")  # User ID
    a_id = a_id[1:-1]
    u_id = u_id[1:-1]
    reset_state = reset_task_info(a_id, u_id)
    if reset_state == 1:
        return jsonify({"state": "Reset successful, please refresh the page!"})
    else:
        return jsonify({"state": "Reset failed, please try again!"})


# Save eye-tracking data
@app.route('/saveData', methods=['POST'])
def save_eyedata():
    # Retrieve information from the frontend
    sid = request.form.get("s_id")  # Sentence ID
    uid = request.form.get("u_id")  # User ID
    wordid = request.form.get("wordid")  # Current word
    x = request.form.get("x")  # X-axis coordinate
    y = request.form.get("y")  # Y-axis coordinate
    time = request.form.get("time")  # Time of eye movement coordinate point
    # Print information for viewing
    # print(sid)
    # print(uid)
    # print(wordid)
    # print(x)
    # print(y)
    # Adjust format
    time = time[1:-1]
    print(time)
    # Retrieve current time
    time2 = datetime.datetime.now()
    print(time2)
    # Save to database and return save status
    result = save_eyedata_info(sid, uid, wordid, x, y, time)
    # Return to frontend upon successful save
    if result == 1:
        return jsonify({"state": "Success, please refresh the page!"})
    else:
        return jsonify({"state": "Failed, please try again!"})


# Validation question page loads and passes fetched data to frontend
@app.route('/answer')
def answer_page():
    # Retrieve user ID and article ID from session
    u_id = session['user_id']
    a_id = session['artical_id']
    # Retrieve answer options for the question from the database's artistic table
    options = get_options(a_id)
    # Split options into array format (test code in functions)
    options = options.split("；")
    options = options[:-1]
    # Randomize order (randomly swap positions of any two elements twice)
    print(options)
    options = exchange_options(options)
    options = exchange_options(options)
    print(options)
    # Pass uid, aid, and options to answer page
    return render_template('answer.html', options_datas={
        "options": options,
        "u_id": u_id,
        "a_id": a_id
    })


# Save answer to validation question and return to task list
@app.route('/saveAnswer', methods=['POST'])
def save_answer():
    # Retrieve information from frontend (uid, aid, answer)
    aid = request.form.get("a_id")  # Article ID
    uid = request.form.get("u_id")  # User ID
    answer_index = int(request.form.get("answer_index"))  # User's answer index
    options = request.form.get("options")  # User's answer
    options = options[0:-1].split(",")
    option = options[answer_index][6:-5]
    print(aid)
    print(uid)
    print(option)
    # Save the above information in the database
    result = save_u_answer(aid, uid, option)
    if result == 1:
        return jsonify({"state": "Saved successfully!"})
    else:
        return jsonify({"state": "Failed to save, please do not submit repeatedly!"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=("eye-tracking.top.pem", "eye-tracking.top.key"))
