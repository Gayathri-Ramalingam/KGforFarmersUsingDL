import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer
from transformers.pipelines import TokenClassificationPipeline
from run_classification_report import classification_report
from conll2003_load import Conll2003


def load_model():
    model_name = "Jean-Baptiste/roberta-large-ner-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return TokenClassificationPipeline(model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

def preprocess_dataset(dataset):
    sentences = []
    true_labels = []
    for _, entry in dataset:
        sentences.append(entry['tokens'])
        true_labels.append(entry['ner_tags'])
    return sentences, true_labels

def predict_labels(pipeline, sentences):
    pred_labels = []
    for sentence in sentences:
        results = pipeline(" ".join(sentence))
        predicted_tags = ["O"] * len(sentence)  # Default to 'O'
        
        for entity in results:
            word = entity['word'].replace('##', '')  # Handle subword tokens
            index = next((i for i, token in enumerate(sentence) if token == word), None)
            if index is not None:
                predicted_tags[index] = entity['entity']
        
        pred_labels.append(predicted_tags)
    return pred_labels

def main():
    dataset = Conll2003()._generate_examples("data/conll2003/test.txt")
    
    pipeline = load_model()
    sentences, true_labels = preprocess_dataset(dataset)
    predicted_labels = predict_labels(pipeline, sentences)
    
    
    print(classification_report(true_labels, predicted_labels))
    

if __name__ == "__main__":
    main()
