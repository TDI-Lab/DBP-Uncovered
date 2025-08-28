#Flask: Flask operations
#render_template: for rendering the html template
#json: for reading the questions from the json file
#os: reading the questions.json file

from flask import Flask, render_template, url_for, request, jsonify, session, redirect
import json
import os
import mysql.connector
from mysql.connector import Error 
from db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from topsis import *
import pandas
import numpy


#Opening Flask app names "app"
app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

user_answers_store = None

#Load question the json file
def load_questions():
    with open('questions.json', 'r') as file:
        return json.load(file)

#Load action_reaction questions
def load_action_data():
    with open('action_reaction_questions.json', 'r') as file:
        return json.load(file)

#Load action mapping data
def load_action_mapping():
    with open('action_mapping.json', 'r') as file:
        return json.load(file)

# Load challenge questions from separate JSON files
def load_challenge_questions():
    challenge_data = []
    
    # Load each challenge page from separate JSON files
    for page_num in range(1, 6):  # Pages 1-5
        filename = f'challenge_page{page_num}.json'
        try:
            with open(filename, 'r') as file:
                page_data = json.load(file)
                challenge_data.append(page_data)
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Skipping page {page_num}")
            continue
    
    return challenge_data

#Normalize the ratings for the TOPSIS
def normalize_ratings(ratings: dict) -> dict:
    total = sum(ratings.values())
    if total == 0:
        return {k: 0 for k in ratings}  # Avoid division by zero
    return {k: round(v / total, 8) for k, v in ratings.items()}

DBP_ranking_dict = {
        "THM": 1,
        "IDBP": 1,
        "BrDBP": 1,
        "HAA": 2,
        "HAN": 3,
        "CB": 4,
        "NS": 5,
        "HAL": 6,
        "HAM": 7,
        "HNM": 8,
        "HBQ": 9,
        "PDBP": 10,
        "HP": 11,
        "BPA": 12,
        "VOC": 12,
        "HDBP": 12,
        "AOX": 12
}

    
action_cat_ranking_dict = {
        "RW": 1,
        "CA": 1,
        "PN": 1,
        "PC": 1,
        "FL": 1,
        "BL": 1,
        "CK": 1,
        "A_other": 1
}

    
dec_matrix_settings = {
       "input_file": "./input/input_data_topsis_IQR_merge-DBP_all-DBP.xlsx",
        "cost_time_setting": "IQR",
        "collect_DBP": "all-DBP"
}


def topsis(r_dict: dict):
    weight_settings = {"all_DBP": {"type": 1,"weight": r_dict["effc_w"]},"cost_tier": {"type": 1,"weight": r_dict["cost_w"]},
                   "time_tier": {"type": 1,"weight": r_dict["time_w"]},"repeat_tier": {"type": 1,"weight": r_dict["freq_w"]}}

    # Load data file
    input_filename = dec_matrix_settings['input_file']

    input_data_df = pd.read_excel(input_filename,index_col = [0])
    input_data_df = input_data_df.drop(columns=["all_Other"], errors="ignore")
        
    #logging.info(f"Starting TOPSIS run: {"expert-weights"}")
        
    # Check the data for zero columns (i.e., all entries zero)
    input_data_df = check_data(input_data_df, map_acronyms = False)
        
    # Set DBP weight distributions
    weight_settings = distribute_DBP_weights(input_data_df, weight_settings, 
                                                DBP_ranking_dict, 
                                                 DBP_merged = True)
        
        # Check settings for criteria
    input_data_df, crit_type_dict = check_criteria(input_data_df, 
                                                       weight_settings, 
                                                       action_cat_ranking_dict)
    for col in input_data_df.columns:
        if col not in weight_settings:
            logging.warning(f"⚠️ Column '{col}' not found in weight settings!")


        # Check settings for weights and retrieve direct weights dictionary
    weight_dict = check_weights(weight_settings)
        
        # Do TOPSIS
    out_df = do_TOPSIS(input_data_df, weight_dict, crit_type_dict)
    return out_df['Score']

# Index route of the app
@app.route('/')
def index():
    quiz_data = load_questions()
    return render_template('index.html', quiz_data=quiz_data)

@app.route('/dashboard')
def dashboard():
    #tiles = dashboard_tiles()

    tiles = [
        {
            "title": "House health",
            "description": "Easy Fixes to Keep Your Home & Water Healthy",
            "icon": "house",
            "url": url_for("house_health")
        },
        {
            "title": "DBP Escape Room Challenge",
            "description": "Go through the escape room to learn about DBP and save your town",
            "icon": "fas fa-door-open",
            "url": url_for("challenge")
        },
        {
            "title": "Action Reaction",
            "description": "Get personalized list of actions to reduce DBPs at home",
            "icon": "fas fa-list",
            "url": url_for("action_reaction")
        },
        {
            "title": "Results",
            "description": "Login to check your recommended actions list",
            "icon": "file-text",
            "url": url_for("login")
        }
    ]
    return render_template("dashboard.html", tiles=tiles)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to their results
    if session.get('user_id'):
        return redirect(url_for('my_surveys'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append("Username is required")
        
        if not password:
            errors.append("Password is required")
        
        if errors:
            return jsonify({
                'status': 'error',
                'errors': errors
            })
        
        # Check user credentials
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                # Login successful
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                # Get user's most recent survey
                cursor.execute(
                    "SELECT id FROM answers WHERE user_id = %s ORDER BY answered_at DESC LIMIT 1",
                    (user['id'],)
                )
                recent_survey = cursor.fetchone()
                
                if recent_survey:
                    session['response_id'] = recent_survey['id']
                    redirect_url = url_for('action_reaction_results')
                else:
                    redirect_url = url_for('my_surveys')
                
                app.logger.info(f"User {username} logged in successfully")
                
                return jsonify({
                    'status': 'success',
                    'redirect_url': redirect_url
                })
            else:
                return jsonify({
                    'status': 'error',
                    'errors': ['Invalid username or password']
                })
                
        except Error as e:
            app.logger.error(f"Database error during login: {e}")
            return jsonify({
                'status': 'error',
                'errors': ['Database error occurred. Please try again.']
            })
        finally:
            cursor.close()
            conn.close()
    
    return render_template('login.html')

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if there are pending survey answers
    pending_answers = session.get('pending_survey_answers')
    app.logger.info("Into Register")

    # If user is already logged in, redirect them away from registration
    if session.get('user_id'):
        app.logger.info("User already logged in, redirecting to dashboard")
        return redirect(url_for('dashboard'))
    

    if not pending_answers:
        # If no pending answers, redirect to survey
        return redirect(url_for('action_reaction'))
    
    if request.method == 'POST':
        data = request.get_json()
        app.logger.info("Into POST")
        username = data.get('username', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(username) > 100:
            errors.append("Username must be less than 100 characters")
        
        if not password:
            errors.append("Password is required")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters long")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        # Check if username already exists
        if not errors:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            try:
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    errors.append("Username already exists. Please choose a different one.")
                
            except Error as e:
                app.logger.error(f"Database error checking username: {e}")
                errors.append("Database error occurred. Please try again.")
            finally:
                cursor.close()
                conn.close()
        
        if errors:
            return jsonify({
                'status': 'error',
                'errors': errors
            })
        
        # Create user account and link survey answers
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Hash the password
            password_hash = generate_password_hash(password)
            
            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            conn.commit()
            
            user_id = cursor.lastrowid
            
            # insert the survey answers with the user_id
            cols = "user_id, " + ", ".join(
                [f"q{i}" for i in range(1, 17)]
                + ["ti", "cost", "freq", "effc"]
            )
            placeholders = ", ".join(["%s"] * 21)  # 21 values including user_id
            sql = f"INSERT INTO answers ({cols}) VALUES ({placeholders})"
            
            # Prepare values with user_id at the beginning
            answer_values = [user_id] + pending_answers
            
            cursor.execute(sql, answer_values)
            conn.commit()
            
            response_id = cursor.lastrowid
            
            # Store user info and response ID in session
            session['user_id'] = user_id
            session['username'] = username
            session['response_id'] = response_id
            
            # Clear pending answers from session
            session.pop('pending_survey_answers', None)

            app.logger.info(f"New user created: {username} (ID: {user_id}), response_id: {response_id}")
            
            return jsonify({
                'status': 'success',
                'redirect_url': url_for('action_reaction_results')
            })
            
        except Error as e:
            conn.rollback()
            app.logger.error(f"Database error creating user and linking answers: {e}")
            return jsonify({
                'status': 'error',
                'errors': ['Failed to create account and save survey data. Please try again.']
            })
        finally:
            cursor.close()
            conn.close()
    
    return render_template('register.html')

# action_reaction
@app.route('/action_reaction', methods=['GET', 'POST'])
def action_reaction():
    global user_answers_store
    if request.method == 'POST':
        data = request.get_json()
        user_answers_store = data['answers']
        
        try:
            selected_values = [item['selected'] for item in user_answers_store]
        except (KeyError, TypeError):
            raise ValueError("Expected a list of dicts each with a 'selected' key")
        
        if len(selected_values) != 20:
            raise ValueError(f"Expected 18 answers, got {len(selected_values)}")
        # Check if user is already logged in
        user_id = session.get('user_id')
        
        if user_id:
            # User is already logged in, save survey directly to their account
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            try:
                # Insert the survey answers with the existing user_id
                cols = "user_id, " + ", ".join(
                    [f"q{i}" for i in range(1, 17)]
                    + ["ti", "cost", "freq", "effc"]
                )
                placeholders = ", ".join(["%s"] * 21)
                sql = f"INSERT INTO answers ({cols}) VALUES ({placeholders})"
                
                # Prepare values with user_id at the beginning
                answer_values = [user_id] + selected_values
                
                cursor.execute(sql, answer_values)
                conn.commit()
                
                response_id = cursor.lastrowid
                
                # Update session with new response ID
                session['response_id'] = response_id
                
                app.logger.info(f"Survey saved for existing user {user_id}, response_id: {response_id}")
                
                return jsonify({
                    'status': 'success',
                    'redirect_url': url_for('action_reaction_results')
                })
                
            except Error as e:
                conn.rollback()
                app.logger.error(f"Database error saving survey for existing user: {e}")
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to save survey data. Please try again.'
                })
            finally:
                cursor.close()
                conn.close()
        else:
            # User is not logged in, store answers temporarily and redirect to registration
            session['pending_survey_answers'] = selected_values
     
        return jsonify({
            'status': 'success',
            'redirect_url': url_for('register')
        })
    
    action_data = load_action_data()
    return render_template('action_reaction.html', action_data=action_data)

def map_codes_to_colored_actions(codes_series, user_response):
    """
    Map codes from series to colored actions based on user responses
    """
    # Load required data
    action_mapping = load_action_mapping()
    action_questions = load_action_data()
    
    # Create a mapping from code to action details
    code_to_action = {item['code']: item for item in action_mapping}
    
    #print(user_response['q2'])
    # Get all numbers that should be green (user answered "Yes")
    green_numbers = set()
    
    # Process first 16 questions (the ones with relations)
    for i in range(16):  # Questions 1-16 have relations
        question_key = f"q{i+1}"
        if question_key in user_response and user_response[question_key] == "Yes":
            # Find the corresponding question in action_questions
            question_data = next((q for q in action_questions if q['id'] == i+1), None)
            #print(question_data)
            if question_data and 'relation' in question_data:
                #print(question_data['relation'])
                green_numbers.update(question_data['relation'])
    #print(green_numbers)
    # Map codes to colored actions
    colored_actions = []
    
    # Convert series to list if it's a pandas Series
    if hasattr(codes_series, 'tolist'):
        codes_list = codes_series.tolist()
    else:
        codes_list = list(codes_series)
    
    for code in codes_list:
        if code in code_to_action:
            action_info = code_to_action[code]
            action_number = action_info['number']
            color = 'green' if action_number in green_numbers else 'red'
            
            colored_actions.append({
                'code': code,
                'action': action_info['action'],
                'number': action_number,
                'color': color
            })
        else:
            # Handle case where code is not found in mapping
            colored_actions.append({
                'code': code,
                'action': f"Unknown action for code: {code}",
                'number': 0,
                'color': 'red'
            })
    
    return colored_actions

# action-reaction-results
@app.route('/action-reaction-results')
def action_reaction_results():
    response_id = session.get('response_id')
    user_id = session.get('user_id')
    username = session.get('username')
    
    if not response_id or not user_id:
        # If no response ID or user not registered, redirect to survey
        return redirect(url_for('action_reaction'))
    
    # Fetch the user's responses from database with user verification
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    

    try:
        # Get the user's responses - verify it belongs to the logged-in user
        sql = "SELECT * FROM answers WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (response_id, user_id))
        user_response = cursor.fetchone()
        
        if not user_response:
            app.logger.warning(f"No response found for response_id {response_id} and user_id {user_id}")
            return redirect(url_for('action_reaction'))
        
        # Extract only the additional information (ti, cost, freq, effc)
        additional_info = extract_additional_info(user_response)
        additional_info_disp = extract_additional_info_disp(user_response)
        # Get your actual data (replace this with your actual data processing)
        data_series = get_user_data_series(user_response, additional_info)
        

        # Map codes to colored actions based on user responses
        colored_actions = map_codes_to_colored_actions(data_series, user_response)
        # Convert Series to DataFrame for HTML display
        # df_html = convert_series_to_html(data_series)

        # Get user information
        cursor.execute("SELECT username, created_at FROM users WHERE id = %s", (user_id,))
        user_info = cursor.fetchone()
        
    except Exception as e:
        app.logger.error(f"Error in action_reaction_results: {e}")
        return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()
    
    return render_template('action_reaction_results.html', 
                         response_id=response_id,
                         username=username,
                         user_info=user_info,
                         additional_info=additional_info_disp,
                         colored_actions = colored_actions,
                         data_series = data_series)

def get_user_data_series(user_response, additional_info):
    pref_dict = {k: v for d in additional_info for k, v in d.items()}
    rating_norm = normalize_ratings(pref_dict)
    s = topsis(rating_norm)
    s.name = "Recommended Actions"
    return s

def convert_series_to_html(data_series):
    """Convert pandas Series to HTML table format"""
    try:
        # Convert Series to DataFrame
        if isinstance(data_series, pd.Series):
            # Create DataFrame from Series
            df = data_series.to_frame()
            
            # If the series doesn't have a name, give it one
            if df.columns[0] == 0:  # Default numeric column name
                df.columns = ['Recommended Actions']
            
            app.logger.info(f"Converted Series to DataFrame with shape: {df.shape}")
            
        elif isinstance(data_series, pd.DataFrame):
            df = data_series
            app.logger.info(f"Already a DataFrame with shape: {df.shape}")
            
        else:
            # Fallback: create DataFrame from list or other data
            df = pd.DataFrame({'Recommended Actions': data_series})
            app.logger.info(f"Created DataFrame from other data type: {type(data_series)}")
        
        # Convert to HTML
        html_table = df.to_html(
            classes='dataframe-table', 
            index=False, 
            border=0, 
            escape=False,
            table_id='results-table'
        )
        
        return html_table
        
    except Exception as e:
        app.logger.error(f"Error converting data to HTML: {e}")
        return "<p>Error: Unable to display results</p>"

#Extract preferences data for diplaying in the html
def extract_additional_info_disp(user_response):
    """Extract only the additional information fields"""
    additional_info = []
    
    # Process additional information fields
    additional_fields = [
        ('ti', 'Time Investment'),
        ('cost', 'Cost Consideration'),
        ('freq', 'Frequency'),
        ('effc', 'Effectiveness')
    ]
    
    for field_key, field_label in additional_fields:
        if field_key in user_response and user_response[field_key] is not None:
            additional_info.append({
                'label': field_label,
                'value': user_response[field_key]
            })
    
    return additional_info

#Extract the Preferences from the database
def extract_additional_info(user_response):
    """Extract only the additional information fields"""
    additional_info = []
    
    # Process additional information fields
    additional_fields = [
        ('ti', 'time_w'),
        ('cost', 'cost_w'),
        ('freq', 'freq_w'),
        ('effc', 'effc_w')
    ]
    
    for field_key, field_label in additional_fields:
        if field_key in user_response and user_response[field_key] is not None:
            additional_info.append({
                field_label : int(user_response[field_key])
            })
    
    return additional_info


# New route to view user's survey history
@app.route('/my-surveys')
def my_surveys():
    user_id = session.get('user_id')
    username = session.get('username')
    
    if not user_id:
        return redirect(url_for('action_reaction'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all surveys for this user
        sql = """
        SELECT id, answered_at
        FROM answers 
        WHERE user_id = %s 
        ORDER BY answered_at DESC
        """
        cursor.execute(sql, (user_id,))
        surveys = cursor.fetchall()
        
    except Error as e:
        app.logger.error(f"Database error fetching user surveys: {e}")
        surveys = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template('my_surveys.html', surveys=surveys, username=username)

# Route to view a specific survey result
@app.route('/survey-result/<int:survey_id>')
def view_survey_result(survey_id):
    user_id = session.get('user_id')
    username = session.get('username')
    
    if not user_id:
        return redirect(url_for('login'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get the specific survey - verify it belongs to the logged-in user
        sql = "SELECT * FROM answers WHERE id = %s AND user_id = %s"
        cursor.execute(sql, (survey_id, user_id))
        user_response = cursor.fetchone()
        
        if not user_response:
            return redirect(url_for('my_surveys'))
        
        # Extract only the additional information (ti, cost, freq, effc)
        additional_info = extract_additional_info(user_response)
        additional_info_disp = extract_additional_info_disp(user_response)
        #df = topsis(r_dict)
        # Get your actual data (replace this with your actual data processing)
        data_series = get_user_data_series(user_response, additional_info)
        

        # Map codes to colored actions based on user responses
        colored_actions = map_codes_to_colored_actions(data_series, user_response)
        # Convert Series to HTML
        # df_html = convert_series_to_html(data_series)
        
        # Set this response as the current one in session for navigation
        session['response_id'] = survey_id
        
    except Exception as e:
        app.logger.error(f"Error in view_survey_result: {e}")
        return redirect(url_for('my_surveys'))
    finally:
        cursor.close()
        conn.close()
    
    return render_template('action_reaction_results.html', 
                         response_id=survey_id,
                         username=username,
                         colored_actions = colored_actions,
                         additional_info=additional_info_disp,
                         data_series = data_series,
                         from_history=True) 


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard'))

#Defining the route for the house health
@app.route('/house_health')
def house_health():
    return render_template('house_health.html')

#Defining the route for the escape room challenge
@app.route('/challenge')
def challenge():
    challenge_data = load_challenge_questions()
    return render_template('challenge.html', challenge_data=challenge_data)


if __name__ == '__main__':
    app.run(debug=True)
