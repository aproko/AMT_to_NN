README:

Goal: To read in AMT data sheets (containing HITs with 10 questions, the first of which is a gold check question) and transform them to neural net input.

Each HIT question has the following fields: Input.sentenceID1, Input.sentence1, Input.hedge1, Input.hedgeType1, Input.defHedgeType1, Input.hedgingDef1, Input.hedgingEx1, Input.nonHedgeDef1, Input.nonHedgeEx1

The first question in each HIT is a check question so it also has the field Input.answer.

The output looks like this: Label(0 or 1) \t Text. The Text is a wind of [-2,+2] around our potential hedge word. 

To run, just do:

bash run.sh /path/to/AMT/file

The output will be saved in this directory as output.txt. It can then be used in hedge_nn/train instead of train_dev.txt (or as the test file).