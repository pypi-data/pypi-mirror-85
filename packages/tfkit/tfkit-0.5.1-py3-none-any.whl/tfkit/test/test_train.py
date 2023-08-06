import unittest
import os
import pytest


class TestTrain(unittest.TestCase):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../../"))
    DATASET_DIR = os.path.join(ROOT_DIR, 'demo_data')
    CLAS_DATASET = os.path.join(DATASET_DIR, 'classification.csv')
    TAG_DATASET = os.path.join(DATASET_DIR, 'tag_row.csv')
    GEN_DATASET = os.path.join(DATASET_DIR, 'generate.csv')
    MASK_DATASET = os.path.join(DATASET_DIR, 'mask.csv')
    MCQ_DATASET = os.path.join(DATASET_DIR, 'mcq.csv')

    def testHelp(self):
        result = os.system('tfkit-train -h')
        assert (result == 0)

    def testMultiTask(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mttask/  --train ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --lr 5e-5 --test ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --model clas onebyone --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mttask/  --train ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --lr 5e-5 --test ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --model clas onebyone --likelihood pos --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mttask/  --train ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --lr 5e-5 --test ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --model clas onebyone --likelihood neg --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mttask/  --train ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --lr 5e-5 --test ' + self.CLAS_DATASET + ' ' + self.GEN_DATASET + ' --model clas onebyone --likelihood both --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)

    def testGenOneByOne(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/onebyone/   --train ' + self.GEN_DATASET + ' --test ' + self.GEN_DATASET + ' --model onebyone --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)

    def testGenOnce(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/once/   --train ' + self.GEN_DATASET + ' --test ' + self.GEN_DATASET + ' --model once --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)

    def testGenMask(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mask/ --train ' + self.MASK_DATASET + ' --test ' + self.MASK_DATASET + ' --model mask --config voidful/albert_chinese_tiny --maxlen 512')
        self.assertTrue(result == 0)

    def testMCQ(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/mcq/ --train ' + self.MCQ_DATASET + ' --test ' + self.MCQ_DATASET + ' --model mcq --config voidful/albert_chinese_tiny --maxlen 512 --handle_exceed start_slice')
        self.assertTrue(result == 0)

    def testGenWithSentLoss(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/ --train ' + self.GEN_DATASET + ' --test ' + self.GEN_DATASET + ' --model onebyone --config voidful/albert_chinese_tiny  --maxlen 50')
        self.assertTrue(result == 0)

    def testClassify(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/clas --train ' + self.CLAS_DATASET + ' --test ' + self.CLAS_DATASET + ' --model clas --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)

    def testTag(self):
        result = os.system(
            'tfkit-train --batch 2 --epoch 2 --savedir ./cache/tag --train ' + self.TAG_DATASET + ' --test ' + self.TAG_DATASET + ' --model tag --config voidful/albert_chinese_tiny --maxlen 50 --handle_exceed slide')
        self.assertTrue(result == 0)

    def testAddToken(self):
        result = os.system(
            'tfkit-train --batch 2 --add_tokens 5 --savedir ./cache/ --epoch 2  --train ' + self.GEN_DATASET + ' --test ' + self.GEN_DATASET + ' --model onebyone --config voidful/albert_chinese_tiny --maxlen 50')
        self.assertTrue(result == 0)
