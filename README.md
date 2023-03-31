# ChatGPT doc manager

- Answering question based on given document
- Use Embedding to select relavent doc
  - idea came from openai cookbook [Question answering using embeddings](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb)
- build using nicegui https://nicegui.io

## it may not be that useful, but

- not useful because chatgpt plugin is there
  - plus new bing with edge browser
- but, good way to learn by building something
  - I plan to learn:
    - web scraping
    - docker deployment
    - project planning and prototyping

## plan
- build doc collector
  - web doc collector
- build chat UI
  - with embedding info about what docs are selected
- doc manager
  - preprocessing
    - embedding inference
    - shortening
  - selecting
    - select specific collection for certain answer
  - info update
    - detect new changes
    - update the collection incrementally
