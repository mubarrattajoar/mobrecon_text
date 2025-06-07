exp_name='test'

CUDA_VISIBLE_DEVICES=0 python -m mobrecon.main \
    --exp_name $exp_name \
    --config_file mobrecon/configs/mobrecon_ds_mod.yml
