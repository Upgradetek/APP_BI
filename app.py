# # app.py

# from flask import Flask, render_template, request
# import sys
# from io import StringIO
# import traceback
# import inspect
# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_code = request.form['code']

#         try:
#             # Capture standard output
#             sys.stdout = StringIO()

#             # Execute the user's code
#             exec(user_code)

#             # Get the result from standard output
#             result = sys.stdout.getvalue()

#             return render_template('index.html', result=result, error=None, user_code=user_code)
#         except Exception  as e:
#            _, _, tb = sys.exc_info()
#            frame = tb.tb_frame
#            line_number = tb.tb_lineno
#            column_number = inspect.currentframe().f_lineno  # Use inspect to get the column

#            # Construct the error message
#            ch = f"Error at line {line_number}, column {column_number}: {e}"

#            return render_template('index.html', result=None, error=ch, user_code=user_code)
#         # except ValueError:
#         #     ch = "Error: Invalid value. Ensure you provide the correct input type."
#         #     return render_template('index.html', result=None, error=ch, user_code=user_code)
#         # except NameError as e:
#         #     ch = f"Error: {e}. Check if all variables are defined before use."
#         #     return render_template('index.html', result=None, error=ch, user_code=user_code)
#         # except Exception as e:
#         #     ch= f"Unexpected error: {e}. Please review your code."
#         #     return render_template('index.html', result=None, error=ch, user_code=user_code)
#         # except Exception as e:
#         #     # Handle errors during code execution
#         #     return render_template('index.html', result=None, error=str(e), user_code=user_code)
#         finally:
#             # Reset standard output
#             sys.stdout = sys.__stdout__

#     # Render the initial page
#     return render_template('index.html', result=None, error=None)


# if __name__ == '__main__':
#     app.run(debug=True)

################################################################################################################################

from flask import Flask, render_template, request
import sys
import traceback
import tokenize
import io

app = Flask(__name__)


def get_column_number(user_code, tb_lasti):
    lines = user_code.split('\n')
    offset = 0

    for i, line in enumerate(lines):
        offset += len(line) + 1  # +1 for the newline character
        if offset > tb_lasti:
            # Now, tokenize the current line to get precise column information
            line_tokens = list(tokenize.tokenize(
                io.BytesIO(line.encode('utf-8')).readline))

            for token in line_tokens:
                if token.start[1] <= tb_lasti - (offset - len(line)) <= token.end[1]:
                    # Adjust column number calculation to get the start of the token
                    return token.start[1], i + 1

    return 0, 0


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_code = request.form['code']

        try:
            # Capture standard output
            sys.stdout = io.StringIO()

            # Execute the user's code
            exec(user_code)

            # Get the result from standard output
            result = sys.stdout.getvalue()

            return render_template('index.html', result=result, error=None, user_code=user_code)
        except Exception as e:
            tb = e.__traceback__
            co = tb.tb_next.tb_frame.f_code if tb.tb_next else tb.tb_frame.f_code
            lineno = tb.tb_lineno if tb.tb_next else co.co_firstlineno

            # Get precise column information
            column_number, line_number = get_column_number(
                user_code, tb.tb_lasti)

            error_type = type(e).__name__

            # Construct the error message without duplication
            ch = f"Error: {e}\nFile '<string>', line {lineno}, column {column_number}\n{error_type}: {e}"
            # ch=dir(e)
            # print(e.args)
            # print(e.with_traceback)
            # ch =str(e[0][0]['code']) + str(e[0][0]['message'])

            return render_template('index.html', result=None, error=ch, user_code=user_code)

    # Render the initial page
    return render_template('index.html', result=None, error=None)


if __name__ == '__main__':
    app.run(debug=True)


########################################################################################################################################


# from flask import Flask, render_template, request
# import sys
# import traceback
# import tokenize
# import io
# from connecteDB import connecte
# from testquestion import question_to_sql 
# app = Flask(__name__)


# def get_column_number(user_code, tb_lasti):
#     lines = user_code.split('\n')
#     offset = 0

#     for i, line in enumerate(lines):
#         offset += len(line) + 1  # +1 for the newline character
#         if offset > tb_lasti:
#             # Now, tokenize the current line to get precise column information
#             line_tokens = list(tokenize.tokenize(
#                 io.BytesIO(line.encode('utf-8')).readline))

#             for token in line_tokens:
#                 if token.start[1] <= tb_lasti - (offset - len(line)) <= token.end[1]:
#                     # Adjust column number calculation to get the start of the token
#                     return token.start[1], i + 1

#     return 0, 0


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_code = request.form['code']

#         try:
#             print(user_code)
#             sql_query = question_to_sql(user_code)
#             result = connecte(sql_query)
#             # result = sql_query

#             return render_template('index.html', result=result, error=None, user_code=user_code)
#         except Exception as e:
#             tb = e.__traceback__
#             co = tb.tb_next.tb_frame.f_code if tb.tb_next else tb.tb_frame.f_code
#             lineno = tb.tb_lineno if tb.tb_next else co.co_firstlineno

#             # Get precise column information
#             column_number, line_number = get_column_number(
#                 user_code, tb.tb_lasti)

#             error_type = type(e).__name__

#             # Construct the error message without duplication
#             ch = f"Error: {e}\nFile '<string>', line {lineno}, column {column_number}\n{error_type}: {e}"
#             # ch=dir(e)
#             # print(e.args)
#             # print(e.with_traceback)
#             # ch =str(e[0][0]['code']) + str(e[0][0]['message'])

#             return render_template('index.html', result=None, error=ch, user_code=user_code)

#     # Render the initial page
#     return render_template('index.html', result=None, error=None)


# if __name__ == '__main__':
#     app.run(debug=True)
