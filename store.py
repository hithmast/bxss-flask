from flask import Flask, request, jsonify, render_template
from datetime import datetime
import logging

app = Flask(__name__)

# Replace with your desired IP address or use '0.0.0.0' to listen on all interfaces
IP_ADDRESS = '0.0.0.0'

# Set up logging to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

log_entries = []

def log_request(value, ip_address):
    try:
        now = datetime.now()
        log_entry = {
            'timestamp': now.strftime('%d.%m.%Y. %H:%M:%S'),
            'ip': ip_address,
            'value': value
        }
        with open('results.txt', 'a') as fp:
            fp.write(f"[{log_entry['timestamp']}][{ip_address}] {value}\n")
        
        # Append the log entry to the HTML file
        with open('results.html', 'a') as html_fp:
            html_fp.write(render_template('results_template.html', log_entries=[log_entry]))
        
        return True
    except Exception as e:
        logging.error("Error logging request: %s", e)
        return False


@app.route("/store/<value>", methods=['POST'])
def store_value(value):
    try:
        ip_address = request.remote_addr

        # Log the incoming request
        logging.info("Received request from IP: %s", ip_address)

        if log_request(value, ip_address):
            return jsonify(result='ok'), 201
        else:
            logging.error("Error processing request")
            return jsonify(result='error'), 500
    except Exception as e:
        logging.error("Error processing request: %s", e)
        return jsonify(result='error'), 500

@app.route("/results")
def view_results():
    return render_template('results.html', log_entries=log_entries)

if __name__ == '__main__':
    # Run the app using a production server (e.g., Gunicorn) for better performance
    app.run(host=IP_ADDRESS)
