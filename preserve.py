
# test ok
@app.route('/ai/test/upoad', methods=['POST'])
def testUpload():
    file = request.files["image"]
    image = Image.open(io.BytesIO(file.read()))
    
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = np.expand_dims(image_array, axis=3)

    print(image_array.shape)

    image = image.convert('L')
    image.save(secure_filename(file.filename))
    return jsonify('success')
