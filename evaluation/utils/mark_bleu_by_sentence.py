import csv
import pandas as pd
import os
import sys

from sacrebleu.metrics import BLEU

def add_path(custom_path):
    if custom_path not in sys.path: sys.path.insert(0, custom_path)
    
this_dir = os.path.dirname(__file__)
lib_path = os.path.join(this_dir, '..', '..')
add_path(lib_path)
from evaluation.scores.bleu_eval import BleuEvaluator


class MarkBleuBySentence:
    def __init__(self, csv_path, tokenize='zh'):
        self.csv_path = csv_path
        self.bleu_evaluator = BleuEvaluator()
        self.bleu_model = BLEU(tokenize=tokenize) 
    
    def mark_bleu_by_sentence(self):
        """
        读取CSV文件，计算每行的BLEU分数，并将结果添加到新列中
        """
        # 读取CSV文件
        df = pd.read_csv(self.csv_path)
        
        # 显示CSV文件的列名以便调试
        print("CSV文件的列名:")
        print(df.columns.tolist())
        print()
        
        # 检查必要的列是否存在
        # 根据之前的讨论，可能需要调整列名
        mt_column = None
        ref_column = None
        
        # 寻找机器翻译列
        for col in df.columns:
            if 'MT' in col or '翻译' in col or 'translation' in col.lower():
                mt_column = col
                break
        
        # 寻找参考答案列
        for col in df.columns:
            if 'ref' in col.lower() or '参考' in col or 'reference' in col.lower():
                ref_column = col
                break
        
        if mt_column is None:
            print("错误: 未找到机器翻译列(MT列)")
            print("可用的列:", df.columns.tolist())
            return
            
        if ref_column is None:
            print("错误: 未找到参考答案列(Reference列)")
            print("可用的列:", df.columns.tolist())
            return
        
        print(f"使用机器翻译列: {mt_column}")
        print(f"使用参考答案列: {ref_column}")
        print()
        
        # 计算每行的BLEU分数
        bleu_scores = []
        valid_count = 0
        
        for index, row in df.iterrows():
            mt_text = row[mt_column]
            ref_text = row[ref_column]
            
            # 检查数据是否有效
            if pd.isna(mt_text) or pd.isna(ref_text) or mt_text == '' or ref_text == '' or mt_text == '。':
                bleu_scores.append(None)  # 无效数据用None填充
                continue
            
            try:
                # 计算BLEU分数
                bleu_score = self.bleu_evaluator.evaluate_sentence(mt_text, [ref_text])
                bleu_score = self.bleu_model.sentence_score(mt_text, [ref_text]).score
                bleu_scores.append(bleu_score)
                valid_count += 1
                
                if valid_count <= 10:  # 只打印前10个结果作为示例
                    print(f"行 {index + 1}:")
                    print(f"  MT: {str(mt_text)[:50]}...")
                    print(f"  Ref: {str(ref_text)[:50]}...")
                    print(f"  BLEU: {bleu_score}")
                    print()
                    
            except Exception as e:
                print(f"计算第 {index + 1} 行BLEU分数时出错: {e}")
                bleu_scores.append(None)
        
        # 将BLEU分数添加到DataFrame
        df['BLEU_Score'] = bleu_scores
        
        # 保存修改后的CSV文件
        output_path = self.csv_path.replace('.csv', '_with_bleu.csv')
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"处理完成!")
        print(f"总行数: {len(df)}")
        print(f"有效BLEU计算: {valid_count}")
        print(f"结果已保存到: {output_path}")
        
        # 计算平均BLEU分数
        valid_bleu_scores = [score for score in bleu_scores if score is not None]
        if valid_bleu_scores:
            avg_bleu = sum(valid_bleu_scores) / len(valid_bleu_scores)
            print(f"平均BLEU分数: {avg_bleu:.4f}")
        
        return output_path
    
    def add_to_existing_csv(self):
        """
        直接在原CSV文件后添加BLEU列
        """
        # 读取现有的CSV文件
        df = pd.read_csv(self.csv_path)
        
        # 如果已经有BLEU_Score列，先删除
        if 'BLEU_Score' in df.columns:
            df = df.drop('BLEU_Score', axis=1)
        
        # 计算BLEU分数
        self.mark_bleu_by_sentence()
            
            
if __name__ == "__main__":
    # 使用示例
    mark_bleu_by_sentence = MarkBleuBySentence('./evaluation/test_data/qwen_result.csv')
    
    # 方法1: 创建新文件
    output_file = mark_bleu_by_sentence.mark_bleu_by_sentence()
    
    # 如果你想要直接修改原文件，可以取消注释下面的代码
    # mark_bleu_by_sentence.add_to_existing_csv()