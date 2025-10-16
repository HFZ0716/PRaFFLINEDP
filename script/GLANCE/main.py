# -*- coding:utf-8 -*-
import warnings
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from src.models.tools import *
from src.models.explain import *
from src.models.glance import *
from src.models.natural import *
from src.utils.config import PROJECT_RELEASE_LIST
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(main.py))))

warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

# The model name and its corresponding python class implementation
MODEL_DICT = {'MIT-TMI-LR': TMI_LR, 'MIT-TMI-SVM': TMI_SVM, 'MIT-TMI-MNB': TMI_MNB, 'MIT-TMI-DT': TMI_DT,
              'MIT-TMI-RF': TMI_RF, 'MIT-LineDP': LineDP,
              'SAT-PMD': PMD, 'SAT-CheckStyle': CheckStyle,
              'NLP-NGram': NGram, 'NLP-NGram-C': NGram_C,
              'Glance-EA': Glance_EA, 'Glance-MD': Glance_MD, 'Glance-LR': Glance_LR,
              'GLANCE-MD': Glance_MD_full_threshold,
              }


# ========================= Run RQ1 experiments =================================
def get_project_releases_dict():
    """
    :return: project releases dict: dict[project] = [r1, r2, ..., rn]
    """
    project_releases_dict = {}
    for release in PROJECT_RELEASE_LIST:
        project = release.split('-')[0]
        if project not in project_releases_dict:
            project_releases_dict[project] = [release]
        else:
            project_releases_dict[project].append(release)

    return project_releases_dict

def run_cross_release_predict(prediction_model, save_time=False):
    # time
    release_name, build_time_list, pred_time_list = [], [], []
    for project, releases in get_project_releases_dict().items():
        for i in range(len(releases) - 1):
            # 1. Loading data. train data index = i, test data index = i + 1
            print(f'========== {prediction_model.model_name} CR PREDICTION for {releases[i + 1]} ================'[:60])
            # ####### Build time #######
            t_start = time.time()
            # 实例化prediction_model类，并传入当前版本和下一个版本的名称以及一个布尔值 is_realistic
            model = prediction_model(releases[i], releases[i + 1], is_realistic=True)
            t_end = time.time()
            build_time_list.append(t_end - t_start)
            # ####### Pred time #######
            t_start = time.time()
            # 对文件级别进行预测
            model.file_level_prediction()
            # 分析文件级别的预测结果
            model.analyze_file_level_result()
            # 对行级别进行预测
            model.line_level_prediction()
            # 分析行级别的预测结果
            model.analyze_line_level_result()
            t_end = time.time()
            pred_time_list.append(t_end - t_start)
            release_name.append(releases[i + 1])

            data = {'release_name': release_name, 'build_time': build_time_list, 'pred_time': pred_time_list}
            data = pd.DataFrame(data, columns=['release_name', 'build_time', 'pred_time'])
            data.to_csv(model.execution_time_file, index=False) if save_time else None


def run_default():
    # Glance_LR/Glance_MD/Glance_EA/Glance_MD_full_threshold重写了文件级缺陷预测方法
    run_cross_release_predict(Glance_LR)
    run_cross_release_predict(Glance_MD)
    run_cross_release_predict(Glance_EA)
    run_cross_release_predict(Glance_MD_full_threshold)
    # LineDP重写了行级别缺陷预测方法
    run_cross_release_predict(LineDP)

    pass


def parse_args():
    # If there is no additional parameters in the command line, run the default models.
    if len(sys.argv) == 1:
        run_default()
    # Run the specific models.
    else:
        model_name = sys.argv[1]
        if model_name in MODEL_DICT.keys():
            run_cross_release_predict(MODEL_DICT[model_name])


if __name__ == '__main__':
    parse_args()
