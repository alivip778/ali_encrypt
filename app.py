from flask import Flask, render_template_string, request, send_file
import os, base64, zipfile, shutil, time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# واجهة الموقع بتصميمك (Ali Encryption)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>Ali Encryption Expert</title>
    <style>
        body { background-color: #000; color: #00ffff; font-family: 'Courier New', Courier, monospace; text-align: center; padding-top: 50px; }
        .container { border: 2px solid #ff00ff; display: inline-block; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px #ff00ff; }
        pre { color: #00ffff; font-weight: bold; }
        h1 { color: #00ffff; text-shadow: 2px 2px #ff00ff; }
        .dev { color: #ffff00; margin-bottom: 20px; }
        input[type="file"] { margin: 20px; color: #fff; background: #333; padding: 10px; border-radius: 5px; }
        input[type="submit"] { background: #00ff00; color: #000; border: none; padding: 15px 30px; cursor: pointer; font-weight: bold; font-size: 1.1em; border-radius: 5px; }
        input[type="submit"]:hover { background: #00cc00; transform: scale(1.05); }
        .footer { margin-top: 20px; color: #ff00ff; border-top: 1px solid #ff00ff; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <pre>
    _      _      _ 
   / \    | |    (_)
  / _ \   | |     _ 
 / ___ \  | |___ | |
/_/   \_\ |_____||_|
        </pre>
        <h1>[ Ali Encryption Expert ]</h1>
        <p class="dev">Telegram: @afrfa6</p>
        
        <form method="post" enctype="multipart/form-data">
            <p>اختر ملف البايثون لتشفيره بأسلوب علي:</p>
            <input type="file" name="file" accept=".py" required><br>
            <input type="submit" value="بدء التشفير الآمن">
        </form>
        
        <div class="footer">Ali-Certified Protection System</div>
    </div>
</body>
</html>
"""

def ali_encrypt_engine(target_file_path, original_name):
    """محرك التشفير الخاص بك مدمج هنا"""
    ali_pack = os.path.join(UPLOAD_FOLDER, "ali_secure.bin")
    
    # 1. ضغط الملف
    with zipfile.ZipFile(ali_pack, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.write(target_file_path, arcname="ali_core.py")
    
    # 2. تحويل لـ Base64
    with open(ali_pack, "rb") as f:
        Ali_Encoded = base64.b64encode(f.read()).decode('utf-8')
    
    os.remove(ali_pack)

    # 3. بناء السكربت النهائي (نفس منطقك)
    output_filename = f"Ali_Secure_{original_name}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    
    secret_script = f"""# --- Encrypted by @afrfa6 ---
import os, base64, zipfile, shutil, subprocess, sys
Ali = "{Ali_Encoded}"
Ali_WorkSpace = ".Ali_Private_Zone"
def Ali_Executor():
    Ali_Raw = base64.b64decode(Ali)
    if not os.path.exists(Ali_WorkSpace): os.makedirs(Ali_WorkSpace)
    Ali_Data_Vault = os.path.join(Ali_WorkSpace, "Ali_Vault.dat")
    with open(Ali_Data_Vault, "wb") as f: f.write(Ali_Raw)
    with zipfile.ZipFile(Ali_Data_Vault, 'r') as ali_zip: ali_zip.extractall(Ali_WorkSpace)
    Ali_Entry = os.path.join(Ali_WorkSpace, "ali_core.py")
    try: subprocess.run([sys.executable, Ali_Entry], check=True)
    except: pass
    finally: shutil.rmtree(Ali_WorkSpace)
if __name__ == "__main__": Ali_Executor()
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(secret_script)
        
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files: return "لا يوجد ملف"
        file = request.files['file']
        if file.filename == '': return "لم يتم اختيار ملف"
        
        if file:
            temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(temp_path)
            
            # تشغيل المحرك الخاص بك
            encrypted_file_path = ali_encrypt_engine(temp_path, file.filename)
            
            # إرسال الملف المشفر للمستخدم
            return send_file(encrypted_file_path, as_attachment=True)
            
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("\n[+] السيرفر شغال يا علي..")
    print("[+] افتح هذا الرابط بالمتصفح: http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080)
