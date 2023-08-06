import os
import re
import wget
from typing import List, Tuple, Optional
import torch
import torch.nn as nn
from transformers import BertModel, BertConfig
from transformers import BertTokenizerFast
import youtokentome as yttm


class SentimentClassifierBERT(nn.Module):
    def __init__(self, bert_config: str):
        super(SentimentClassifierBERT, self).__init__()
        config = BertConfig.from_pretrained(bert_config)
        self.bert = BertModel(config)
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.6),
            nn.ReLU(),
            nn.Linear(768, 3),
        )
    def forward(self, input_ids: torch.tensor, attention_mask: torch.tensor):
        out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        out = torch.mean(out[0], dim=1)
        out = self.classifier(out)
        return out

class TinySentimentClassifier(nn.Module):
    def __init__(self, vocab_size: int, embedding_dim: int, lstm_hidden: int):
        super(TinySentimentClassifier, self).__init__()
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0)
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=lstm_hidden,
            num_layers=2,
            bidirectional=True,
            dropout=.5
        )
        self.output = nn.Sequential(
            nn.Linear(lstm_hidden*2, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 3)
        )
    
    def forward(self, input_ids: torch.tensor):
        out = self.embedding(input_ids)
        out, _ = self.lstm(out)
        out = torch.mean(out, dim=1)
        out = self.output(out)
        return out

class SentimentClassifier:
    """Sentiment Classifier for short Russian texts.
    
    Classes:
    
    * 0 - neutral;
    * 1 - positive;
    * 2 - negative
    """
    def __init__(self, model_type: str = 'bert', model_path: str = 'models'):
        """Classifier initialization
        
        Args:
            model_type: str - type of model: `bert` or `tiny`.
            model_path: str - path for models' weights
        """
        if model_type in ('tiny', 'bert', 'bert_med', 'bert_reviews', 'bert_sentiment', 'bert_tweet'):
            if model_type == 'tiny':
                self.tokenizer, self.model = self.load_tiny(model_path)
            else:
                self.tokenizer, self.model = self.load_bert(model_path, model_type)
        else:
            raise ValueError('Undefined model type. Select: `bert` or `tiny`.')
        
        self.model_type = model_type
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.eval()
        self.model.to(self.device)
    
    def load_bert(self, model_path: str, model_type: str) -> Tuple:
        """ Load Bert model and tokenizer
        """
        models = {
            'bert': 'bert_sentiment.pt',
            'bert_med': 'bertMed.pt',
            'bert_reviews': 'bertRuReviews.pt',
            'bert_sentiment': 'bertRuSemtiment.pt',
            'bert_tweet': 'bertRuTweet.pt',
        }
        os.makedirs(model_path, exist_ok=True)
        if not os.path.isfile(os.path.join(model_path, models[model_type])):
            wget.download(
                f'https://github.com/blanchefort/RuSentiment/releases/download/v1.0bert/{models[model_type]}',
                os.path.join(model_path, models[model_type]))
        tokenizer = BertTokenizerFast.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
        model = SentimentClassifierBERT('DeepPavlov/rubert-base-cased-conversational')
        model.load_state_dict(torch.load(os.path.join(model_path, models[model_type])))
        return tokenizer, model
    
    def load_tiny(self, model_path: str) -> Tuple:
        """Load tiny model and tokenizer
        """
        tok_fname = '10k.yttm'
        m_fname = 'tiny_sentiment.pt'
        os.makedirs(model_path, exist_ok=True)
        if not os.path.isfile(os.path.join(model_path, tok_fname)):
            wget.download(
                'https://github.com/blanchefort/RuSentiment/releases/download/v1.0tiny/10k.yttm',
                os.path.join(model_path, tok_fname))
        if not os.path.isfile(os.path.join(model_path, m_fname)):
            wget.download(
                'https://github.com/blanchefort/RuSentiment/releases/download/v1.0tiny/tiny_sentiment.pt',
                os.path.join(model_path, m_fname))
        
        tokenizer = yttm.BPE(os.path.join(model_path, tok_fname))
        model = TinySentimentClassifier(
            vocab_size=10000,
            embedding_dim=96,
            lstm_hidden=64)
        model.load_state_dict(torch.load(os.path.join(model_path, m_fname)))
        return tokenizer, model
    
    def preprocess(self, text: str) -> str:
        """Minimal text preprocessing
        """
        text = re.sub("^\s+|\n|\r|\s+$", ' ', text)
        return text.strip().lower()
    
    def predict(self, texts: List[str], max_len: int = 70) -> Tuple:
        """Main method: predict sentiment classes for batch of texts

        Args:

            texts: List[str] - list of texts. Format:
                texts = [text_1, text_2, ..., text_n]
            max_len: int - maximal length of sequence.
        Returns:
            tuple - Result is a tuple of two lists:
                * sentiment class for each text;
                * logits for each text.
        """
        if len(texts) == 0:
            return False, False
        
        texts = list(map(self.preprocess, texts))
        
        if self.model_type == 'tiny':
            return self._predict_tiny(texts, max_len=max_len)
        return self._predict_bert(texts, max_len=max_len)
        
    
    def _predict_bert(self, texts: List[str], max_len: int) -> Tuple:
        tokenized_data = self.tokenizer(texts,
                                        padding='max_length',
                                        truncation=True,
                                        max_length=max_len,
                                        return_token_type_ids=False,
                                        return_tensors='pt')
        with torch.no_grad():
            logits = self.model(tokenized_data['input_ids'].to(self.device),
                                tokenized_data['attention_mask'].to(self.device))
        predicts = torch.argmax(logits, dim=1)
        return predicts.cpu().tolist(), logits.cpu().tolist()
    
    def _predict_tiny(self, texts: List[str], max_len: int) -> Tuple:
        sequence: List = []
        for comment in self.tokenizer.encode(texts, output_type=yttm.OutputType.ID):
            if len(comment) < max_len:
                offset = max_len - len(comment)
                comment += [0] * offset
            comment = comment[:max_len]
            sequence.append(comment)
        sequence = torch.tensor(sequence, dtype=torch.long)
        
        with torch.no_grad():
            logits = self.model(sequence.to(self.device))
        predicts = torch.argmax(logits, dim=1)
        return predicts.cpu().tolist(), logits.cpu().tolist()
