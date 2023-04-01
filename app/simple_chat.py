import asyncio
import os
import openai
from nicegui import ui
import dataclasses

openai.api_key = os.getenv("OPENAI_API_KEY")



@dataclasses.dataclass
class Message:
  role: str
  content: str

  @property
  def text(self) -> str:
    return self.content
  
  def to_dict(self):
    return dict(role=self.role, content=self.content)
  
@dataclasses.dataclass
class System(Message):
  pass

@dataclasses.dataclass
class Question(Message):
  pass

@dataclasses.dataclass
class Answer(Message):
  pass


class Conversation:
  history: list[Message]
  def __init__(self):
    self.history = [
      System('system', 'You are ChatGPT, a helpful assistant. You use Markdown format whenever possible')
    ]

  async def ask_chatgpt(self, question: str):
    question = Question('user', question)
    self.history.append(question)

    messages = [m.to_dict() for m in self.history]
    response = await openai.ChatCompletion.acreate(
      model="gpt-3.5-turbo",
      messages=messages,
      stream=True
    )

    answer_arr = []
    async for delta in response:
      if 'role' in delta.choices[0].delta: continue
      if delta.choices[0].finish_reason == 'stop': continue

      delta_text = delta.choices[0].delta.content
      answer_arr.append(delta_text)
      yield answer_arr

    answer_text = ''.join(answer_arr)
    answer = Answer('assistant', answer_text)
    self.history.append(answer)


class state:
  conversation = Conversation()
  wait_for_answer = False


async def submit_question():
  if state.wait_for_answer: return
  question = ui_input.value.strip()
  if not question: return 
  ui_input.value = ''

  with ui_chat:
    ui.markdown(question).classes('p-3 pb-1 border shadow rounded-md self-end').style('max-width: 90%')
    with ui.column().classes('p-3 pb-1 shadow border rounded-md') as spinner:
      ui.spinner('dots')

  state.wait_for_answer = True

  ui_answer = None
  stream = state.conversation.ask_chatgpt(question)
  async for answer_arr in stream:
    if not ui_answer:
      ui_chat.remove(spinner)
      with ui_chat:
        ui_answer = ui.markdown('').classes('p-3 pb-1 border shadow rounded-md').style('max-width: 90%')
    ui_answer.content = ''.join(answer_arr)
    
  state.wait_for_answer = False

with ui.column().classes('bg-blue-80 self-center w-full').style('width: 800px'):
  ui.markdown("hello world").classes('p-3 pb-1 border shadow rounded-md').style('max-width: 90%')
  ui_chat = ui.column().classes('w-full')
  ui_input = ui.input(placeholder='Type question here. Press "Enter" to submit')\
    .classes('px-3 border shadow rounded-md self-end').style('width: 80%')\
      .on('keypress.enter', submit_question)



ui.run(port=10086)

