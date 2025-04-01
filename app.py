from flask import Flask, request, send_file
import vobject
import tempfile
import os

app = Flask(__name__)

@app.route('/generate-vcf', methods=['POST'])
def generate_vcf():
    data = request.json
    numbers = data.get("numbers", "").split(",")
    
    if not numbers:
        return {"error": "No numbers provided"}, 400

    # Create a VCF file
    vcf_content = ""
    for number in numbers:
        number = number.strip()
        if number:
            vcard = vobject.vCard()
            tel = vcard.add('tel')
            tel.value = number
            vcf_content += vcard.serialize()

    # Save to a temporary file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".vcf")
    temp.write(vcf_content.encode())
    temp.close()

    # Send file to user
    return send_file(temp.name, as_attachment=True, download_name="contacts.vcf")

if __name__ == '__main__':
    app.run(debug=True)
