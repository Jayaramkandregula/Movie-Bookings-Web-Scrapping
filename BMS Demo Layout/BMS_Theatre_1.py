from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Read the seat data from a DataFrame

df = pd.read_csv("The_Greatest_of_All_Time_PVR_INOX_Megaplex_Mall_of_Asia__Bangalore_Wed-18 Sep_06-15 PM-2D.csv")

# Convert the DataFrame to a list of dictionaries for easy manipulation
seats = df.to_dict(orient='records')


# Home route to render the seat layout
@app.route('/')
def home():
    return render_template('index.html', seats=seats)


# API route to handle seat selection/deselection
@app.route('/toggle-seat', methods=['POST'])
def toggle_seat():
    seat_info = request.json
    row = seat_info['row']
    column = seat_info['column']

    # Toggle availability based on row and column
    for seat in seats:
        if seat['Row'] == row and seat['Column'] == column:
            seat['Availability Status'] = 'Available' if seat['Availability Status'] == 'Unavailable' else 'Unavailable'
            break

    return jsonify({'status': 'success', 'seats': seats})


# API route to calculate metrics
@app.route('/metrics', methods=['GET'])
def metrics():
    selected_seats = [seat for seat in seats if seat['Availability Status'] == 'Unavailable']

    # Calculate metrics
    total_count = len(selected_seats)
    gold_count = len([s for s in selected_seats if 'GOLD' in s['Seat Class']])
    prime_count = len([s for s in selected_seats if 'PRIME' in s['Seat Class']])

    gold_revenue = sum(s['Price'] for s in selected_seats if 'GOLD' in s['Seat Class'])
    prime_revenue = sum(s['Price'] for s in selected_seats if 'PRIME' in s['Seat Class'])

    metrics = {
        'total_count': total_count,
        'gold_count': gold_count,
        'prime_count': prime_count,
        'gold_revenue': gold_revenue,
        'prime_revenue': prime_revenue
    }

    return jsonify(metrics)


if __name__ == '__main__':
    app.run(debug=True)


