cd ./tests/dist/image_classification
python main.py \
    --verbose \
    --train_max_epochs 2 \
    --train_epoch_length 2 \
    --eval_max_epochs 2 \
    --eval_epoch_length 2 \
    --log_train 1 \
    --log_eval 1 \
    --train_batch_size 4 \
    --eval_batch_size 4 \
