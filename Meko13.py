import time
import requests
from datetime import datetime

# 1. مفاتيح الربط الخاصة بتليجرام
TELEGRAM_TOKEN = "8542873270:AAFKWzfSDbcjM8uM1FBl4JOBtraXjoC9-PY"
CHAT_ID = "5319309377"

def send_to_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try: 
        requests.post(url, json=payload, timeout=10)
    except: 
        pass

# إعدادات الخوارزمية
STREAK_LIMIT = 3  
under_streak = 0

# ✅ رابط الـ API المباشر للموبايل لتفادي حظر الـ Cloudflare بالكامل
API_URL = "https://1xbet.com"

last_tracked_match_id = None
waiting_for_result = False
last_known_score = ""  

print("🔥 تم تشغيل النسخة الفولاذية المتخطية للحماية... فحص مباشر!")

while True:
    try:
        params = {
            'sport': 104, 
            'championship': 2496733, 
            'lng': 'ar', 
            'cyber': True
        } 
        
        # محاكاة كاملة لتطبيق أندرويد رسمي لمنع قفل الاتصال
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(API_URL, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('Value', [])
            
            if matches and isinstance(matches, list):
                current_match = matches[0] if isinstance(matches, list) else matches
                match_id = current_match.get('CI')
                team1 = current_match.get('O1E', 'الفريق الأول')
                team2 = current_match.get('O2E', 'الفريق الثاني')
                championship_name = current_match.get('LE', 'إف سي 26 - بطولة العالم')
                
                scores = current_match.get('SC', {}).get('FS', {})
                home_goals = int(scores.get('S1', 0))
                away_goals = int(scores.get('S2', 0))
                total_goals = home_goals + away_goals
                current_score_str = f"{home_goals}-{away_goals}"
                
                # ─── ميزة 1: إشعار ببدء مباراة جديدة ───
                if match_id != last_tracked_match_id and not waiting_for_result:
                    last_tracked_match_id = match_id
                    last_known_score = current_score_str
                    توقيت_البدء = datetime.now().strftime('%I:%M %p')
                    
                    رسالة_البدء = (
                        f"🎮 *مـبـاراة جـديـدة بـدأت الآن لايـف* 🎮\n\n"
                        f"🏆 *البطولة:* {championship_name}\n"
                        f"⚔️ *المواجهة:* `{team1}` vs `{team2}`\n"
                        f"🔢 *النتيجة الافتتاحية:* {home_goals} - {away_goals}\n"
                        f"🕒 *توقيت البدء:* {توقيت_البدء}\n\n"
                        f"📡 البوت يراقب المباراة ويرسل الأهداف فوراً..."
                    )
                    send_to_telegram(رسالة_البدء)
                    
                    if total_goals < 2:
                        under_streak += 1
                    else:
                        under_streak = 0
                    
                    if under_streak >= STREAK_LIMIT:
                        رسالة_تليجرام = (
                            f"🚨 *إشارة ذهبية مضمومة من البوت الفتاك* 🚨\n\n"
                            f"📊 *حالة الخوارزمية:* غياب الأهداف مستمر لـ {under_streak} جولات!\n"
                            f"⚔️ *المباراة القادمة:* {team1} vs {team2}\n"
                            f"⚽ *التوقع:* [ Over 1.5 Goals ]\n"
                            f"💡 *نصيحة أخوية:* جمد قلبك يا غالي الماتش ده بتاعنا!"
                        )
                        send_to_telegram(رسالة_تليجرام)
                        under_streak = 0 
                        waiting_for_result = True 

                # ─── ميزة 2: إشعار فور تغير النتيجة لايف ───
                elif match_id == last_tracked_match_id and current_score_str != last_known_score:
                    last_known_score = current_score_str
                    
                    رسالة_تحديث_النتيجة = (
                        f"⚽ *هـــددف جـــديـــد سُـــجـــل الآن!* ⚽\n\n"
                        f"⚔️ *المباراة:* {team1} vs {team2}\n"
                        f"🔥 *النتيجة المحدثة:* `{home_goals} - {away_goals}`\n"
                        f"🔢 *إجمالي الأهداف:* {total_goals}"
                    )
                    send_to_telegram(رسالة_تحديث_النتيجة)

                final_teams = f"{team1} vs {team2}"
                final_home = home_goals
                final_away = away_goals
                final_goals = total_goals
                
                print(f"🎮 متابعة لايف: {team1} vs {team2} | النتيجة: {current_score_str}")
                
                # ─── ميزة 3: إرسال النتيجة عند نهاية اللقاء ───
                if waiting_for_result and match_id != last_tracked_match_id:
                    توقيت_النهاية = datetime.now().strftime('%I:%M %p')
                    حالة_الرهان = "✅ مـبـرووك الـرهـان كـسـب!" if final_goals >= 2 else "❌ الـرهـان مـعـوّض الـجـالـة الـجـايـة"
                    
                    رسالة_النتيجة = (
                        f"🏁 *الـمـبـاراة انـتـهـت الآن* 🏁\n\n"
                        f"⚔️ *المواجهة:* {final_teams}\n"
                        f"🔢 *النتيجة النهائية:* {final_home} - {final_away} (إجمالي الأهداف: {final_goals})\n"
                        f"🕒 *توقيت القاهرة:* {توقيت_النهاية}\n\n"
                        f"{حالة_الرهان}"
                    )
                    send_to_telegram(رسالة_النتيجة)
                    waiting_for_result = False
            else:
                print("📭 متصل بالخادم، ولكن لا توجد مباريات حية حالياً في هذه البطولة.")
        else:
            print(f"⚠️ الموقع أعاد استجابة غير صحيحة، كود: {response.status_code}")
            
    except Exception as e:
        # طباعة الخطأ الفعلي لنعرف المشكلة بدقة
        print(f"🔄 جاري التحديث، والسبب الحالي: {str(e)[:50]}")
        
    time.sleep(20)
