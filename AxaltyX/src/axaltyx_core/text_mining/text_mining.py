import pandas as pd
import numpy as np
import re
from collections import Counter

def sentiment_analysis(data: pd.DataFrame, text_var: str, method: str = "lexicon", language: str = "chinese") -> dict:
    try:
        # 检查变量是否存在
        if text_var not in data.columns:
            raise ValueError(f"变量 {text_var} 不存在于数据中")
        
        # 简单的情感词典（中文）
        if language == "chinese":
            positive_words = ['好', '棒', '优秀', '满意', '喜欢', '赞', '高兴', '快乐', '幸福', '美好']
            negative_words = ['差', '糟糕', '失望', '讨厌', '坏', '烂', '生气', '悲伤', '痛苦', '难过']
        else:
            # 英文情感词典
            positive_words = ['good', 'great', 'excellent', 'satisfied', 'like', 'love', 'happy', 'joy', 'wonderful', 'amazing']
            negative_words = ['bad', 'terrible', 'disappointed', 'hate', 'awful', 'sad', 'angry', 'painful', 'miserable', 'upset']
        
        # 计算情感得分
        sentiment_scores = []
        word_frequencies = Counter()
        positive_words_found = Counter()
        negative_words_found = Counter()
        
        for text in data[text_var].astype(str):
            # 分词（简单的空格分词）
            words = re.findall(r'\b\w+\b', text.lower())
            
            # 统计词频
            word_frequencies.update(words)
            
            # 计算情感得分
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            # 统计积极和消极词汇
            for word in words:
                if word in positive_words:
                    positive_words_found[word] += 1
                elif word in negative_words:
                    negative_words_found[word] += 1
            
            # 计算情感得分
            if len(words) > 0:
                score = (positive_count - negative_count) / len(words)
            else:
                score = 0
            
            sentiment_scores.append(score)
        
        # 计算情感分布
        sentiment_distribution = {
            'positive': sum(1 for score in sentiment_scores if score > 0.1),
            'neutral': sum(1 for score in sentiment_scores if -0.1 <= score <= 0.1),
            'negative': sum(1 for score in sentiment_scores if score < -0.1)
        }
        
        # 获取前10个积极和消极词汇
        top_positive = dict(positive_words_found.most_common(10))
        top_negative = dict(negative_words_found.most_common(10))
        
        return {
            "success": True,
            "results": {
                "sentiment_scores": sentiment_scores,
                "distribution": sentiment_distribution,
                "word_frequencies": dict(word_frequencies.most_common(20)),
                "top_positive": top_positive,
                "top_negative": top_negative
            },
            "warnings": [],
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }

def text_preprocessing(data: pd.DataFrame, text_var: str, operations: list[str] = None) -> dict:
    try:
        # 检查变量是否存在
        if text_var not in data.columns:
            raise ValueError(f"变量 {text_var} 不存在于数据中")
        
        # 默认操作
        if operations is None:
            operations = ["lowercase", "tokenize", "remove_stopwords"]
        
        # 停止词列表
        stopwords = set([
            '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你',
            '会', '着', '没有', '看', '好', '自己', '这', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by'
        ])
        
        processed_text = []
        vocabulary = set()
        
        for text in data[text_var].astype(str):
            # 转为小写
            if "lowercase" in operations:
                text = text.lower()
            
            # 移除标点符号
            text = re.sub(r'[\p{P}\p{S}]', ' ', text)
            
            # 分词
            if "tokenize" in operations:
                words = re.findall(r'\b\w+\b', text)
            else:
                words = [text]
            
            # 移除停止词
            if "remove_stopwords" in operations:
                words = [word for word in words if word not in stopwords]
            
            # 词干提取（简单实现）
            if "stemming" in operations:
                # 简单的中文词干提取（仅做示例）
                if any(ord(c) > 127 for c in words[0]):
                    pass  # 中文不做词干提取
                else:
                    # 英文简单词干提取
                    stemmed_words = []
                    for word in words:
                        if word.endswith('ing'):
                            stemmed_words.append(word[:-3])
                        elif word.endswith('ed'):
                            stemmed_words.append(word[:-2])
                        elif word.endswith('s'):
                            stemmed_words.append(word[:-1])
                        else:
                            stemmed_words.append(word)
                    words = stemmed_words
            
            # 词形还原（简单实现）
            if "lemmatize" in operations:
                # 简单的词形还原（仅做示例）
                lemmatized_words = []
                for word in words:
                    # 这里只是简单示例，实际应使用NLTK等库
                    if word == 'better':
                        lemmatized_words.append('good')
                    elif word == 'best':
                        lemmatized_words.append('good')
                    else:
                        lemmatized_words.append(word)
                words = lemmatized_words
            
            processed_text.append(' '.join(words))
            vocabulary.update(words)
        
        # 构建文档-词矩阵
        vocabulary_list = list(vocabulary)
        doc_term_matrix = []
        
        for text in processed_text:
            words = text.split()
            row = [words.count(word) for word in vocabulary_list]
            doc_term_matrix.append(row)
        
        doc_term_matrix = pd.DataFrame(doc_term_matrix, columns=vocabulary_list)
        
        return {
            "success": True,
            "results": {
                "processed_text": processed_text,
                "vocabulary": list(vocabulary),
                "document_term_matrix": doc_term_matrix
            },
            "warnings": [],
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "results": {},
            "warnings": [],
            "error": str(e)
        }
