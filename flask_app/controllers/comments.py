from flask_app import app
from flask import request, session, jsonify, redirect, render_template
from flask_app.models.comment import Comment


@app.route('/comments/create', methods = ['POST'])
def create_comment():
    if 'user_id' in session:
        status = 'Fail'
        if Comment.validate(request.form):
            data = {
                **request.form,'poster_id' : session['user_id']
            }
            Comment.save(data)
            status = request.form['profile_id']
        return jsonify({'status' : status, 'ride_id' : request.form['ride_id']})
    return redirect('/')

@app.route('/comments/<int:comment_id>/<int:ride_id>/delete')
def delete_comment(comment_id, ride_id):
    if 'user_id' in session:
        comment = Comment.getById({'id' : comment_id})
        if comment :
            if comment.poster_id == session['user_id']:
                Comment.delete({'id' : comment_id})
                return redirect(f'/users/view/{comment.profile_id}/{ride_id}')
            # else :
            #     hacker = User.get_by_id({'id' : session['user_id']})
            #     if hacker.warning<1 : #TRUE MEANS IT'S HIS FIRST TIME
            #         User.add_warning({'id' : session['user_id']}) #ADD A WARNING
            #         ip_address = request.remote_addr
            #         return render_template('hackAttempt.html', hacker=hacker, book_id = comment.book_id, ip_address=ip_address)
            #     else:
            #         #Blacklist The Hacker
            #         Like.deleteByUser({'user_id' : hacker.id})
            #         Comment.deleteByUser({'user_id' : hacker.id})
            #         Book.deleteByUser({'user_id' : hacker.id})
            #         User.delete({'id' : hacker.id})
            #         Blacklist.save({'email': hacker.email})
            #         session.clear()
            #         return redirect('/')
        else :
            return render_template('404.html')
    return redirect('/')

@app.route('/comments/<int:comment_id>/edit/<string:comment>')
def edit_comment(comment_id, comment):
    status = 'Fail'
    data = {
        'id' : comment_id,
        'comment' : comment
    }
    if comment:
        comment = Comment.getById({'id' : comment_id})
        if Comment.edit(data) == None:
            status = comment.profile_id
    return jsonify({'status' : status})