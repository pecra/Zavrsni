_base_ = [
    '../_base_/models/segformer_mit-b0.py',
    '../_base_/datasets/synapse.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_80k.py'
]
crop_size = (512, 512)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor,
    backbone=dict())

optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=dict(
        type='AdamW', lr=0.00006, betas=(0.9, 0.999), weight_decay=0.01),
    paramwise_cfg=dict(
        custom_keys={
            'pos_block': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.),
            'head': dict(lr_mult=10.)
        }))

param_scheduler = [
    dict(
        type='LinearLR', start_factor=1e-6, by_epoch=False, begin=0, end=720),  
    dict(
        type='PolyLR',
        eta_min=0.0,
        power=1.0,
        begin=720,  
        end=80000, 
        by_epoch=False,
    )
]
test_evaluator = dict(type='IoUMetric', iou_metrics=['mIoU'], output_dir='work_dirs/format_results')

train_dataloader = dict(batch_size=4, num_workers=1)
val_dataloader = dict(batch_size=1, num_workers=1)
test_dataloader = val_dataloader
