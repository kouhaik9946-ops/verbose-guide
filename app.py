from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# قاعدة البيانات الفقهية الشاملة مع البدائل المصاغة
SHARIA_RULES = [
    {
        "id": "Riba_Interest",
        "category": "Riba",
        "title": "ربا الديون / اشتراط فائدة محدودة",
        "keywords": ["فائدة", "فوائد", "نسبة سنوية", "apr", "interest", "أرباح مضمونة", "زيادة مشروطة"],
        "context_patterns": [r"فائدة\s*قدرها", r"زيادة\s*بنسبة", r"أرباح\s*مضمونة"],
        "advice": "الشرع يحرم الاشتراط المالي المسبق على القروض أو الزيادات المشروطة فـ أصل الدين.",
        "redraft": "التزام الطرفين بدفع المبالغ المستحقة دون أي زيادة أو فائدة مشروطة، وفق أحكام عقد القرض الحسن أو المرابحة بمرابحة معلومة."
    },
    {
        "id": "Riba_Delay",
        "category": "Penalty",
        "title": "شرط جزائي جائر / غرامة تأخير نقدية",
        "keywords": ["غرامة تأخير", "تأخير السداد", "عن كل يوم تأخير", "تعويض الدائن", "1.5%", "2%", "غرامة مالية"],
        "context_patterns": [r"غرامة\s*تأخير", r"عن\s*كل\s*يوم\s*تأخير", r"فائدة\s*تأخير"],
        "advice": "لا يجوز للدائن أخذ غرامات مالية ناتجة عن تأخير الديون لنفسه لأنها ربا جاهلية.",
        "redraft": "في حالة تأخر الطرف الثاني عن السداد بغير عذر شرعي، يلتزم بدفع مبلغ مقطوع قدره (حدد المبلغ) يُصرف بالكامل للجهات الخيرية ولا يستفيد منه الدائن."
    },
    {
        "id": "Gharar_Price",
        "category": "Gharar",
        "title": "غرر / جهالة فاحشة في الثمن أو الأجل",
        "keywords": ["سعر غير محدد", "حسب تقدير", "سعر السوق وقت التسليم", "غير محددة", "أجل غير محدد"],
        "context_patterns": [r"سعر\s*غير\s*محدد", r"حسب\s*تقدير\ window", r"سعر\s*السوق"],
        "advice": "الشرع يستوجب وضوح الثمن والمبيع والأجل وقت عقد البيع نفي للجهالة والنزاع.",
        "redraft": "يتفق الطرفان على أن الثمن الإجمالي المحدد والنهائي للمبيع هو (حدد المبلغ بالضبط) ويدفع بتاريخ (حدد الأجل بالضبط)."
    },
    {
        "id": "Gharar_Unpossessed",
        "category": "Gharar",
        "title": "بيع ما لا يملك / بيع المعدوم",
        "keywords": ["قبل حيازته", "قبل امتلاكه", "قبل القبض", "بيع المعدوم"],
        "context_patterns": [r"قبل\s*حيازته", r"قبل\s*امتلاكه"],
        "advice": "نهى النبي صلى الله عليه وسلم عن بيع الإنسان ما ليس عنده أو قبل قبضه وحيازته الضامنة.",
        "redraft": "يلتزم البائع بتمليك المبيع وقبضه قبضاً حقيقياً أو حكمياً قبل إبرام عقد البيع النهائي مع المشتري."
    }
]

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    detected_issues = []
    
    for rule in SHARIA_RULES:
        found_words = []
        
        # 1. فحص الكلمات المفتاحية
        for word in rule["keywords"]:
            if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE) or word in text:
                found_words.append(word)
                
        # 2. فحص نمط السياق الذكي
        for pattern in rule["context_patterns"]:
            if re.search(pattern, text, re.IGNORECASE):
                found_words.append("تحليل السياق: " + pattern.replace(r'\s*', ' '))
                
        if found_words:
            detected_issues.append({
                "id": rule["id"],
                "category": rule["category"],
                "title": rule["title"],
                "matched_words": list(set(found_words)),
                "advice": rule["advice"],
                "redraft": rule["redraft"]
            })
            
    total_rules = len(SHARIA_RULES)
    flagged_rules = len(detected_issues)
    score = max(0, int(((total_rules - flagged_rules) / total_rules) * 100))
    
    return jsonify({
        "status": "success",
        "score": score,
        "issues": detected_issues
    })

if __name__ == '__main__':
    print("🚀 السيرفر المطور خدام دابا على: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)