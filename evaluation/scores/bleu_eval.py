"""
BLEU score evaluation module
"""

from sacrebleu.metrics import BLEU

class BleuEvaluator:
    def __init__(self, tokenize=None):
        """
        Initialize BLEU evaluator
        
        Args:
            tokenize: Tokenization method or language code for SacreBLEU
        """
        self.bleu_model = BLEU(tokenize=tokenize)
    
    def evaluate_corpus(self, mts, refs):
        """
        Evaluate corpus-level BLEU score
        
        Args:
            mts: List of machine translations
            refs: List of reference translations or list of lists of references
            
        Returns:
            Dictionary containing BLEU score and full results
        """
        bleu_results = self.bleu_model.corpus_score(mts, refs)
        return {
            'bleu_score': bleu_results.score,
            'bleu_results': bleu_results
        }
    
    def evaluate_sentence(self, mt, refs):
        """
        Evaluate sentence-level BLEU score
        
        Args:
            mt: Machine translation
            refs: List of reference translations
            
        Returns:
            BLEU score
        """
        return self.bleu_model.sentence_score(mt, refs).score 
    
if __name__ == "__main__":
    bleu_evaluator = BleuEvaluator()
    # mt = "The player is encountering with the Blue Terran's SUV"
    # mt = "The South Korea player is encountering with the Blue Terran's SCV"
    mt = "asdasdasdas 123123 asdasda"
    refs = ["The South Korea player is encountering with the Blue Terran's SCV"]
    print(bleu_evaluator.evaluate_sentence(mt, refs))