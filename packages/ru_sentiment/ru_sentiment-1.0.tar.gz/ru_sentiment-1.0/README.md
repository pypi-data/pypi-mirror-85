# RuSentiment
_Short Russian texts sentiment classification_

Нейросети, классифицирующие короткие тексты на русском языке (например, комментарии или отзывы) по тональности.

Берт-модели обучены на основе [RuBert Conversational](https://huggingface.co/DeepPavlov/rubert-base-cased-conversational). Малая модель — LSTM с полносвязным слоем. Получена в ходе knowledge distillation.

## Модели

Для классификации по тональности нужно выбрать модель, которую планируется использовать:

* `bert` — Общая Берт-модель, обученная на всех корпусах.
* `tiny` — Малая модель, полученная в ходе дистилляции на всех корпусах текстов.
* `bert_med` — Берт-модель, обученная на корпусе **Отзывы о медучреждениях**.
* `bert_reviews` — Берт-модель, обученная на корпусе **RuReviews**.
* `bert_sentiment` — Берт-модель, обученная на корпусе **RuSentiment**.
* `bert_tweet` — Берт-модель, обученная на корпусе **RuTweetCorp**. (Только положительный и негативный классы).

## Категории
* Нейтральный: 0
* Позитивный: 1
* Отрицательный: 2

## Метрики моделей

Тестирование моделей проводилось на 2 CPU. Размер выборки: 35.180 примеров. Размер батча: 2.000 примеров.

| Модель | weighted F1 | Accuracy | Обработка, тексты/сек. |
|:-:|:-:|:-:|:-:|
|Большая модель|0.9039|0.9038|4.71|
|Малая модель|0.8753|0.8756|613.96|
|:-:|:-:|:-:|:-:|
|`bert_med`|0.9195|0.9465|--|
|`bert_reviews`|0.7750|0.8522|--|
|`bert_sentiment`|0.8056|0.8705|--|
|`bert_tweet`|0.9998|0.9999|--|

## Использование моделей

Установка:

```
pip install ru_sentiment
```

Либо:

```
git clone https://github.com/blanchefort/RuSentiment.git
pip install -r RuSentiment/ru_sentiment/requirements.txt
```

Использование:

```python
from ru_sentiment import SentimentClassifier

target_names = ['neutral', 'positive', 'negative']
texts = ['Еще немного карельских осенних красот.',
         'Никогда не задумывался о том, откуда на самом деле появляются апатия, постоянные переносы важных дел на потом и в принципе нежелание заниматься повседневными делами?',
         'Наливайки, ломбарды и микрозаймы на каждом шагу - первый признак депрессивного города с нищим населением.',
         'Горжусь🔥🔥🔥👏👏👏Хоть где-то мы лидируем😎😎😎👍👍👍Дай бог занять первое место в этом рейтинге💪💪💪😍😍😍',
         ]

# 1. bert
sent_cls = SentimentClassifier(model_type='bert', model_path='models')

results, _ = sent_cls.predict(texts=texts, max_len=70)

for t, l in zip(texts, results):
    print(target_names[l], ':', t)
    print('-'*15)

# 2. tiny
sent_cls = SentimentClassifier(model_type='tiny', model_path='models')

results, _ = sent_cls.predict(texts=texts, max_len=200)

for t, l in zip(texts, results):
    print(target_names[l], ':', t)
    print('-'*15)
```

## Корпусы, на которых модели обучались

Для обучения был собран большой агрегированный корпус из нескольких датасетов. Общий размер агрегированной выборки составил 351.797 текстов. Размер тестовой выборки — 10%.

**[RuTweetCorp](https://study.mokoron.com/)**

> Рубцова Ю. Автоматическое построение и анализ корпуса коротких текстов (постов микроблогов) для задачи разработки и тренировки тонового классификатора //Инженерия знаний и технологии семантического веба. – 2012. – Т. 1. – С. 109-116.

**[RuReviews](https://github.com/sismetanin/rureviews)**

> RuReviews: An Automatically Annotated Sentiment Analysis Dataset for Product Reviews in Russian.

**[RuSentiment](http://text-machine.cs.uml.edu/projects/rusentiment/)**

> A. Rogers A. Romanov A. Rumshisky S. Volkova M. Gronas A. Gribov RuSentiment: An Enriched Sentiment Analysis Dataset for Social Media in Russian. Proceedings of COLING 2018.

**[Отзывы о медучреждениях](https://github.com/blanchefort/datasets/tree/master/medical_comments)**

> Датасет содержит пользовательские отзывы о медицинских учреждениях. Датасет собран в мае 2019 года с сайта prodoctorov.ru
