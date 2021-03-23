cd ./tests/dist/gan
python main.py \
    --verbose \
    --batch_size 4 \
    --data_path /tmp/cifar10 \
    --max_epochs 2 \
    --epoch_length 2
    --log_train 1 \
    --log_eval 1
