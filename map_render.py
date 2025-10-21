import folium
import base64
from io import BytesIO
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_map', methods=['POST'])
def generate_map():
    data = request.json
    locations = data.get('locations')

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
    for loc in locations:
        folium.Marker(location=loc['coordinates'], popup=loc['label']).add_to(m)

    # Save map to an image in memory
    img_buffer = BytesIO()
    m.save(img_buffer, close_file=False)
    img_buffer.seek(0)

    # Encode the image to base64 for transfer
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return jsonify({'map_image_base64': img_base64})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
