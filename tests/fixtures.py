import pytest


@pytest.fixture
def create_poll_data():
    return {
      "questions": [
        {
          "possible_answers": [
            {
              "text": "вариант 1",
              "question": 1
            }
          ],
          "text": "Первый вопрос",
          "question_type": 1,
          "poll": 1
        }
      ],
      "name": "Опрос первый",
      "end_date": "2021-08-17T05:01:24.862Z",
      "description": "Опиание"
    }
