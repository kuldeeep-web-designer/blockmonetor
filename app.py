from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = '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'
client = Groq(api_key=GROQ_API_KEY)

with open("knowledge.txt", 'r', encoding='utf-8') as file:
    knowledge = file.read() 


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'response': "No message provided."}), 400

    if user_message.lower() in ['hi', 'hello', 'hey']:
        return jsonify({'response': 'Hello! I am BlockMentor AI 🤖 I can help you understand blockchain and dApp concepts!'})

    # Quick test shortcut to avoid calling external API during testing
    if user_message == '__test__':
        mock_reply = (
            "Definition: AI is the field of creating systems that can perform tasks requiring human intelligence.\n"
            "Examples:\n- Chatbots\n- Image recognition\n- Recommendation systems\n"
            "What next:\n- Types\n- Applications\n- Advantages"
        )
        return jsonify({'response': mock_reply})

    try:
        completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
    "role": "user",
    "content": f"""
You are a helpful AI tutor chatbot.

Your job is to give SHORT and INTERACTIVE answers.

RULES:
- Remember you will not answer anything which is not in the knowledge base{knowledge}.
- Do NOT give long paragraphs
- Give only basic explanation first
- Keep answer within 4-6 lines
- Always include 2-3 simple examples
- After answering, suggest next options to explore

FORMAT:
1. Definition (short)
2. Examples (bullet points)
3. Ask user what they want next (like types, applications, advantages, etc.) (bullet points)

Knowledge:
{knowledge}

Question: {user_message}

If answer not found, say: Sorry, I don't know the answer for this question.
"""
}],

 )
    
        bot_reply = completion.choices[0].message.content.strip()

    except Exception as e:
        # Return a friendly error without exposing internals
        return jsonify({'response': 'Error: could not get a response from the AI service right now.'}), 502

    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)