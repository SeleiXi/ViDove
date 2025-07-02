import pandas as pd
import sys
import os

def add_path(custom_path):
    if custom_path not in sys.path: sys.path.insert(0, custom_path)

# Add the project root to Python path
this_dir = os.path.dirname(__file__)
lib_path = os.path.join(this_dir, '..', '..')
add_path(lib_path)

from evaluation.scores.bleu_eval import BleuEvaluator

class CalAvgScoresInCsv:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        
    def cal_avg_scores(self):
        df = pd.read_csv(self.csv_path)

        # 过滤掉MT为NaN、空字符串或"。"的行，保留有实际翻译内容的行
        # filtered_df = df[
        #     (df['MT'].notna()) &  # 过滤NaN值
        #     (df['MT'] != '') &    # 过滤空字符串
        #     (df['MT'] != '。')    # 过滤只有句号的行
        # ]
        filtered_df = df[(df['MT'] != '。')]
        
        # 过滤【MT】栏位不为 "。" 的行（跳过【Translation的结果】不为空的情况）
        # filtered_df = df[df['MT'] != '。']

        
        # 只打印10行的所有内容
        print(filtered_df[['MT','ref']].head(10))  
        
        
        print(f'过滤后的行数: {len(filtered_df)}')
        # 计算 COMET / LLM Score 栏位的平均值
        average_comet = filtered_df['sCOMET'].mean()
        # average_comet = df['dCOMET'].mean()
        average_llm_score = filtered_df['COMET'].mean()

        print(f'sCOMET 栏位的平均值为: {average_comet}')
    


        mt_list = filtered_df[['MT']]
        mt_list = filtered_df['MT'].tolist()
        print(mt_list[:10])
        mt_list = [
        "我认为BLEU是一个很好的东西。",
        "其次,我建议使用润滑槽方法,这意味着每天多次在单杠上悬挂,时间约为你最大悬挂时间的50%,这主要是进行低于最大强度的训练,你需要频繁练习,同时尽量保持身体的清新感,每天都要进行润滑槽训练."
    ]
        ref_list = filtered_df['ref'].tolist()   
        print(ref_list[:10])
        # ref_list = filtered_df['MT'].tolist()
        # ref_list = filtered_df['COMET'].tolist()
        # print(mt_list)
        # print(ref_list[:10])
        ref_list = [
        "你好，我认为BLEU是一个非常糟糕的评价指标。",
        "第二，我推荐磨合训练法，单杠训练一天多次，锻炼时间保持在你最长记录的50%，也就是做次强度训练。勤加练习，同时保持精力充沛。每天如是磨合训练。"
    ]
        bleu_result = BleuEvaluator().evaluate_sentence(mt_list, [ref_list])
        print(f"BLEU: {bleu_result['bleu_score']}")
        

if __name__ == "__main__":
    cal_avg_scores_in_csv = CalAvgScoresInCsv('./evaluation/test_data/qwen_result.csv')
    cal_avg_scores_in_csv.cal_avg_scores()
