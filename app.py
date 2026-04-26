import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# إعداد الـ API بالمفتاح الجديد بتاعك
genai.configure(api_key="AIzaSyBYSB-nRsvYXpT0WulSA46EAnxZV2Dc32Y")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/build', methods=['POST'])
def build():
    try:
        data = request.json
        p_name = data.get('name', 'My Game')
        p_desc = data.get('details', 'A fun game')
        
        # استخدام موديل 1.5 فلاش السريع
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # البرومبت "الذكي" لإجبار Gemini على استخدام Phaser.js
        prompt = f"""
        Create a complete single-file HTML5 game titled '{p_name}'.
        Technical Stack: Phaser.js (CDN: https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js).
        Game Logic: {p_desc}.
        Requirements:
        - Must be a single HTML file including CSS and JavaScript.
        - Use Phaser Arcade Physics for movement and collisions.
        - Responsive canvas size.
        - Professional game structure (Preload, Create, Update).
        - No markdown, no conversational text, ONLY raw HTML code.
        """

        response = model.generate_content(prompt)
        
        # تنظيف الكود من أي علامات زائدة
        clean_code = response.text.replace("```html", "").replace("```", "").strip()
        
        return jsonify({"code": clean_code})

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return jsonify({"code": f"<h1>خطأ في السيرفر</h1><p>{str(e)}</p>"}), 500

if __name__ == '__main__':
    app.run(debug=True)