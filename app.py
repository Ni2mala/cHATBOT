import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

conversation_history = []

system_context = """You are a professional customer support assistant 
for an online clothing brand. Help customers with:
- Product details (size, color, fabric, fit, care)
- Pricing, discounts, availability
- Orders, shipping, tracking
- Returns, exchanges, refunds
Be clear, friendly, and concise."""


def chat_ollama(message_list):
    response = requests.post('http://localhost:11434/api/chat',
                             json={
                                 "model": "llama3.2",
                                 "messages": message_list,
                                 "stream": True,
                             })
    return response.json()['message']['content']


def save_chat(history_to_save, filename="chat_history.json"):
    with open(filename, "w") as f:
        data = {"chat_history": history_to_save}
        json.dump(data, f, indent=2)
    return True


def chat_with_memory(user_input, conversation_history, system_context):
    message_list = [{"role": "system", "content": system_context}]
    message_list.extend(conversation_history)
    message_list.append({"role": "user", "content": user_input})

    response = chat_ollama(message_list)

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": response})

    while len(conversation_history) > 20:
        del conversation_history[0:2]

    return response


# ── Routes ──

@app.route('/')
def index():
    return render_template('index.html')


from flask import Flask, render_template, request, jsonify, Response
import json

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'response': ''})

    def generate():
        # Build message list
        message_list = [{"role": "system", "content": system_context}]
        message_list.extend(conversation_history)
        message_list.append({"role": "user", "content": user_input})

        full_response = ""

        # Stream from Ollama
        with requests.post('http://localhost:11434/api/chat',
                           json={"model": "llama3.2", "messages": message_list, "stream": True},
                           stream=True) as r:
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get('message', {}).get('content', '')
                    full_response += token
                    yield f"data: {json.dumps({'token': token})}\n\n"

        # Save to history after full response
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": full_response})

        while len(conversation_history) > 20:
            del conversation_history[0:2]

        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(generate(), mimetype='text/event-stream')


@app.route('/save', methods=['POST'])
def save():
    save_chat(conversation_history)
    return jsonify({'status': 'saved'})


@app.route('/clear', methods=['POST'])
def clear():
    conversation_history.clear()
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    app.run(debug=True)