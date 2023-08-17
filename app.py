from flask import Flask, request, jsonify
import numpy as np
from scipy.spatial.distance import cosine

app = Flask(__name__)

# Function to calculate fingerprint similarity


def fingerprint_similarity(hex_fingerprint1, hex_fingerprint2):
    # Convert integer array to hex string array
    hex_string1 = [hex(byte)[2:].zfill(2) for byte in hex_fingerprint1]
    hex_string2 = [hex(byte)[2:].zfill(2) for byte in hex_fingerprint2]

    # Convert hex string array to float array
    float_array1 = np.array([int(hex_byte, 16) for hex_byte in hex_string1])
    float_array2 = np.array([int(hex_byte, 16) for hex_byte in hex_string2])

    # Calculate cosine similarity
    similarity = 1 - cosine(float_array1, float_array2)

    return similarity

# Compare fingerprints and return matching ID or "not found"


@app.route('/compare', methods=['POST'])
def compare_fingerprints():
    try:
        data = request.json
        fingerprint1_list = data['fingerprint_list']
        fingerprint2 = np.array(data['fingerprint2'])
        threshold = 0.65
        matching_id = None

        for fingerprint_id, fingerprint in fingerprint1_list.items():
            similarity_score = fingerprint_similarity(
                fingerprint, fingerprint2)
            if similarity_score >= threshold:
                matching_id = fingerprint_id
                break

        if matching_id:
            result = {
                "match": True,
                "id": matching_id
            }
        else:
            result = {
                "match": False,
                "id": "not found"
            }

        return jsonify(result)

    except Exception as e:
        error_message = {
            "error": "Invalid input format or internal error"
        }
        return jsonify(error_message), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
