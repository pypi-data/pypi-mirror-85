from .data import COLORS #line:1
from .yolact import Yolact #line:2
from .utils .augmentations import FastBaseTransform #line:3
from .utils import timer #line:4
from .utils .functions import SavePath #line:5
from .layers .output_utils import postprocess ,undo_image_transformation #line:6
from .data import cfg ,set_cfg #line:8
import numpy as np #line:10
import torch #line:11
import argparse #line:13
import random #line:14
from collections import defaultdict #line:15
from PIL import Image #line:16
import matplotlib .pyplot as plt #line:17
import cv2 #line:18
w_aim ,h_aim =256 ,512 #line:22
def show (OO0O0OOOO0OOO0OOO ,size =8 ):#line:26
    plt .figure (figsize =(size ,size ))#line:27
    if np .max (OO0O0OOOO0OOO0OOO )<=1 :#line:28
        plt .imshow (OO0O0OOOO0OOO0OOO ,vmin =0 ,vmax =1 )#line:29
    else :#line:30
        plt .imshow (OO0O0OOOO0OOO0OOO ,vmin =0 ,vmax =255 )#line:31
    plt .gray ()#line:32
    plt .show ()#line:33
    plt .close ()#line:34
    print ()#line:35
def str2bool (O0OOOOO000O0OOOO0 ):#line:37
    if O0OOOOO000O0OOOO0 .lower ()in ('yes','true','t','y','1'):#line:38
        return True #line:39
    elif O0OOOOO000O0OOOO0 .lower ()in ('no','false','f','n','0'):#line:40
        return False #line:41
    else :#line:42
        raise argparse .ArgumentTypeError ('Boolean value expected.')#line:43
def parse_args (argv =None ,inpass =None ,outpass =None ,model_path =None ):#line:45
    OO0OO0OOOO0O0O000 =argparse .ArgumentParser (description ='YOLACT COCO Evaluation')#line:47
    OO0OO0OOOO0O0O000 .add_argument ('--trained_model',default =model_path ,type =str ,help ='Trained state_dict file path to open. If "interrupt", this will open the interrupt file.')#line:50
    OO0OO0OOOO0O0O000 .add_argument ('--top_k',default =10 ,type =int ,help ='Further restrict the number of predictions to parse')#line:52
    OO0OO0OOOO0O0O000 .add_argument ('--cuda',default =True ,type =str2bool ,help ='Use cuda to evaulate model')#line:54
    OO0OO0OOOO0O0O000 .add_argument ('--fast_nms',default =True ,type =str2bool ,help ='Whether to use a faster, but not entirely correct version of NMS.')#line:56
    OO0OO0OOOO0O0O000 .add_argument ('--display_masks',default =True ,type =str2bool ,help ='Whether or not to display masks over bounding boxes')#line:58
    OO0OO0OOOO0O0O000 .add_argument ('--display_bboxes',default =True ,type =str2bool ,help ='Whether or not to display bboxes around masks')#line:60
    OO0OO0OOOO0O0O000 .add_argument ('--display_text',default =True ,type =str2bool ,help ='Whether or not to display text (class [score])')#line:62
    OO0OO0OOOO0O0O000 .add_argument ('--display_scores',default =True ,type =str2bool ,help ='Whether or not to display scores in addition to classes')#line:64
    OO0OO0OOOO0O0O000 .add_argument ('--display',dest ='display',action ='store_true',help ='Display qualitative results instead of quantitative ones.')#line:66
    OO0OO0OOOO0O0O000 .add_argument ('--shuffle',dest ='shuffle',action ='store_true',help ='Shuffles the images when displaying them. Doesn\'t have much of an effect when display is off though.')#line:68
    OO0OO0OOOO0O0O000 .add_argument ('--ap_data_file',default ='results/ap_data.pkl',type =str ,help ='In quantitative mode, the file to save detections before calculating mAP.')#line:70
    OO0OO0OOOO0O0O000 .add_argument ('--resume',dest ='resume',action ='store_true',help ='If display not set, this resumes mAP calculations from the ap_data_file.')#line:72
    OO0OO0OOOO0O0O000 .add_argument ('--max_images',default =-1 ,type =int ,help ='The maximum number of images from the dataset to consider. Use -1 for all.')#line:74
    OO0OO0OOOO0O0O000 .add_argument ('--output_coco_json',dest ='output_coco_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this just dumps detections into the coco json file.')#line:76
    OO0OO0OOOO0O0O000 .add_argument ('--bbox_det_file',default ='results/bbox_detections.json',type =str ,help ='The output file for coco bbox results if --coco_results is set.')#line:78
    OO0OO0OOOO0O0O000 .add_argument ('--mask_det_file',default ='results/mask_detections.json',type =str ,help ='The output file for coco mask results if --coco_results is set.')#line:80
    OO0OO0OOOO0O0O000 .add_argument ('--config',default =None ,help ='The config object to use.')#line:82
    OO0OO0OOOO0O0O000 .add_argument ('--output_web_json',dest ='output_web_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this dumps detections for usage with the detections viewer web thingy.')#line:84
    OO0OO0OOOO0O0O000 .add_argument ('--web_det_path',default ='web/dets/',type =str ,help ='If output_web_json is set, this is the path to dump detections into.')#line:86
    OO0OO0OOOO0O0O000 .add_argument ('--no_bar',dest ='no_bar',action ='store_true',help ='Do not output the status bar. This is useful for when piping to a file.')#line:88
    OO0OO0OOOO0O0O000 .add_argument ('--display_lincomb',default =False ,type =str2bool ,help ='If the config uses lincomb masks, output a visualization of how those masks are created.')#line:90
    OO0OO0OOOO0O0O000 .add_argument ('--benchmark',default =False ,dest ='benchmark',action ='store_true',help ='Equivalent to running display mode but without displaying an image.')#line:92
    OO0OO0OOOO0O0O000 .add_argument ('--no_sort',default =False ,dest ='no_sort',action ='store_true',help ='Do not sort images by hashed image ID.')#line:94
    OO0OO0OOOO0O0O000 .add_argument ('--seed',default =None ,type =int ,help ='The seed to pass into random.seed. Note: this is only really for the shuffle and does not (I think) affect cuda stuff.')#line:96
    OO0OO0OOOO0O0O000 .add_argument ('--mask_proto_debug',default =False ,dest ='mask_proto_debug',action ='store_true',help ='Outputs stuff for scripts/compute_mask.py.')#line:98
    OO0OO0OOOO0O0O000 .add_argument ('--no_crop',default =False ,dest ='crop',action ='store_false',help ='Do not crop output masks with the predicted bounding box.')#line:100
    OO0OO0OOOO0O0O000 .add_argument ('--image',default ='{}:{}'.format (inpass ,outpass ),type =str ,help ='A path to an image to use for display.')#line:102
    OO0OO0OOOO0O0O000 .add_argument ('--images',default =None ,type =str ,help ='An input folder of images and output folder to save detected images. Should be in the format input->output.')#line:104
    OO0OO0OOOO0O0O000 .add_argument ('--video',default =None ,type =str ,help ='A path to a video to evaluate on. Passing in a number will use that index webcam.')#line:106
    OO0OO0OOOO0O0O000 .add_argument ('--video_multiframe',default =1 ,type =int ,help ='The number of frames to evaluate in parallel to make videos play at higher fps.')#line:108
    OO0OO0OOOO0O0O000 .add_argument ('--score_threshold',default =0.15 ,type =float ,help ='Detections with a score under this threshold will not be considered. This currently only works in display mode.')#line:110
    OO0OO0OOOO0O0O000 .add_argument ('--dataset',default =None ,type =str ,help ='If specified, override the dataset specified in the config with this one (example: coco2017_dataset).')#line:112
    OO0OO0OOOO0O0O000 .add_argument ('--detect',default =False ,dest ='detect',action ='store_true',help ='Don\'t evauluate the mask branch at all and only do object detection. This only works for --display and --benchmark.')#line:114
    OO0OO0OOOO0O0O000 .set_defaults (no_bar =False ,display =False ,resume =False ,output_coco_json =False ,output_web_json =False ,shuffle =False ,benchmark =False ,no_sort =False ,no_hash =False ,mask_proto_debug =False ,crop =True ,detect =False )#line:117
    global args #line:119
    args =OO0OO0OOOO0O0O000 .parse_args (argv )#line:120
    if args .output_web_json :#line:122
        args .output_coco_json =True #line:123
    if args .seed is not None :#line:125
        random .seed (args .seed )#line:126
iou_thresholds =[O0O00OOO0O0OO00O0 /100 for O0O00OOO0O0OO00O0 in range (50 ,100 ,5 )]#line:128
coco_cats ={}#line:129
coco_cats_inv ={}#line:130
color_cache =defaultdict (lambda :{})#line:131
def prep_display (OO0OOOOO00000OO0O ,O0O000O00O0O00OOO ,O0OO000000O00000O ,O00OOO0O0OOO0O0OO ,O0O0O000OO0000O0O ,undo_transform =True ,class_color =False ,mask_alpha =0.45 ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:133
    ""#line:136
    if undo_transform :#line:137
        O00O000OO0OOOO000 =undo_image_transformation (O0OO000000O00000O ,O0O0O000OO0000O0O ,O00OOO0O0OOO0O0OO )#line:138
        OOOO00O000OO0O0OO =torch .Tensor (O00O000OO0OOOO000 )#line:140
    else :#line:141
        OOOO00O000OO0O0OO =O0OO000000O00000O /255.0 #line:142
        O00OOO0O0OOO0O0OO ,O0O0O000OO0000O0O ,_O000OO0OO0OO0OOO0 =O0OO000000O00000O .shape #line:143
    with timer .env ('Postprocess'):#line:145
        OOOO000000OO0OOOO =postprocess (O0O000O00O0O00OOO ,O0O0O000OO0000O0O ,O00OOO0O0OOO0O0OO ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:148
    with timer .env ('Copy'):#line:152
        if cfg .eval_mask_branch :#line:153
            OOOO0O0OO0OOO00O0 =OOOO000000OO0OOOO [3 ][:args .top_k ]#line:155
        OOOO00000O0OO0OOO ,O00O0000O00O000OO ,O00OO0O0O0OO00OOO =[O0O0OO000000OO0O0 [:args .top_k ].cpu ().numpy ()for O0O0OO000000OO0O0 in OOOO000000OO0OOOO [:3 ]]#line:156
    OO0O0OOOOOOO00OO0 =np .array (OOOO00000O0OO0OOO ,str )#line:159
    OO0O0OOOOOOO00OO0 [OO0O0OOOOOOO00OO0 =='0']='person'#line:160
    OO0O0OOOOOOO00OO0 [OO0O0OOOOOOO00OO0 =='24']='backpack'#line:161
    OO0O0OOOOOOO00OO0 [OO0O0OOOOOOO00OO0 =='26']='handbag'#line:162
    OO0O0OOOOOOO00OO0 [OO0O0OOOOOOO00OO0 =='27']='tie'#line:163
    if verbose >0 :#line:164
        print ('detected: {}'.format (OO0O0OOOOOOO00OO0 ))#line:165
    O00O0000OOO00OO0O =min (args .top_k ,OOOO00000O0OO0OOO .shape [0 ])#line:169
    for O0OO0OOO0OO0O0OOO in range (O00O0000OOO00OO0O ):#line:170
        if O00O0000O00O000OO [O0OO0OOO0OO0O0OOO ]<args .score_threshold :#line:171
            O00O0000OOO00OO0O =O0OO0OOO0OO0O0OOO #line:172
            break #line:173
    if O00O0000OOO00OO0O ==0 :#line:180
        O000000OO0OOOOO0O =np .ones ((h_aim ,w_aim ),'uint8')*255 #line:181
        return O000000OO0OOOOO0O #line:182
    def O0OOOOO00O000O000 (O0O0O00OOO00OOOO0 ,on_gpu =None ):#line:186
        global color_cache #line:187
        OO00OO000OO0O0OOO =(OOOO00000O0OO0OOO [O0O0O00OOO00OOOO0 ]*5 if class_color else O0O0O00OOO00OOOO0 *5 )%len (COLORS )#line:188
        if on_gpu is not None and OO00OO000OO0O0OOO in color_cache [on_gpu ]:#line:190
            return color_cache [on_gpu ][OO00OO000OO0O0OOO ]#line:191
        else :#line:192
            OOO000OO000O0O00O =COLORS [OO00OO000OO0O0OOO ]#line:193
            if not undo_transform :#line:194
                OOO000OO000O0O00O =(OOO000OO000O0O00O [2 ],OOO000OO000O0O00O [1 ],OOO000OO000O0O00O [0 ])#line:196
            if on_gpu is not None :#line:197
                OOO000OO000O0O00O =torch .Tensor (OOO000OO000O0O00O ).to (on_gpu ).float ()/255. #line:198
                color_cache [on_gpu ][OO00OO000OO0O0OOO ]=OOO000OO000O0O00O #line:199
            return OOO000OO000O0O00O #line:203
    if args .display_masks and cfg .eval_mask_branch :#line:206
        OOOO0O0OO0OOO00O0 =OOOO0O0OO0OOO00O0 [:O00O0000OOO00OO0O ,:,:,None ]#line:208
        OOOO0O0OO0OOO00O0 =np .array (OOOO0O0OO0OOO00O0 )#line:211
        OOOO0O0OO0OOO00O0 =OOOO0O0OO0OOO00O0 .reshape (OOOO0O0OO0OOO00O0 .shape [:-1 ])#line:213
        O00OO0OO00OOO0000 =[]#line:218
        O00O0OOO000000OO0 =len (OO0OOOOO00000OO0O )*len (OO0OOOOO00000OO0O [0 ])#line:220
        OO000O0OO0OO0000O ,O000OO0OOO00O0000 =0 ,0 #line:222
        OO00O0OO0O0000OOO =None #line:223
        for OO0OO0OOO0OOOO000 in range (len (OOOO00000O0OO0OOO )):#line:224
            if OOOO00000O0OO0OOO [OO0OO0OOO0OOOO000 ]==0 and np .sum (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ,:,:])>O00O0OOO000000OO0 *0.15 *0.5 :#line:225
                OO000O0OO0OO0000O =np .sum (np .array (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ]))#line:226
                if OO000O0OO0OO0000O >O000OO0OOO00O0000 :#line:227
                    O000OO0OOO00O0000 =OO000O0OO0OO0000O #line:228
                    OO00O0OO0O0000OOO =OO0OO0OOO0OOOO000 #line:229
        if OO00O0OO0O0000OOO is not None :#line:230
            O00OO0OO00OOO0000 .append (OO00O0OO0O0000OOO )#line:231
        OO000O0OO0OO0000O ,O000OO0OOO00O0000 =0 ,0 #line:233
        OO00O0OO0O0000OOO =None #line:234
        for OO0OO0OOO0OOOO000 in range (len (OOOO00000O0OO0OOO )):#line:235
            if OOOO00000O0OO0OOO [OO0OO0OOO0OOOO000 ]==24 and np .sum (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ,:,:])>O00O0OOO000000OO0 *0.009 *0.5 :#line:236
                OO000O0OO0OO0000O =np .sum (np .array (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ]))#line:237
                if OO000O0OO0OO0000O >O000OO0OOO00O0000 :#line:238
                    O000OO0OOO00O0000 =OO000O0OO0OO0000O #line:239
                    OO00O0OO0O0000OOO =OO0OO0OOO0OOOO000 #line:240
        if OO00O0OO0O0000OOO is not None :#line:241
            O00OO0OO00OOO0000 .append (OO00O0OO0O0000OOO )#line:242
        OO000O0OO0OO0000O ,O000OO0OOO00O0000 =0 ,0 #line:244
        OO00O0OO0O0000OOO =None #line:245
        for OO0OO0OOO0OOOO000 in range (len (OOOO00000O0OO0OOO )):#line:246
            if OOOO00000O0OO0OOO [OO0OO0OOO0OOOO000 ]==26 and np .sum (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ,:,:])>O00O0OOO000000OO0 *0.009 *0.5 :#line:247
                OO000O0OO0OO0000O =np .sum (np .array (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ]))#line:248
                if OO000O0OO0OO0000O >O000OO0OOO00O0000 :#line:249
                    O000OO0OOO00O0000 =OO000O0OO0OO0000O #line:250
                    OO00O0OO0O0000OOO =OO0OO0OOO0OOOO000 #line:251
        if OO00O0OO0O0000OOO is not None :#line:252
            O00OO0OO00OOO0000 .append (OO00O0OO0O0000OOO )#line:253
        OO000O0OO0OO0000O ,O000OO0OOO00O0000 =0 ,0 #line:255
        OO00O0OO0O0000OOO =None #line:256
        for OO0OO0OOO0OOOO000 in range (len (OOOO00000O0OO0OOO )):#line:257
            if OOOO00000O0OO0OOO [OO0OO0OOO0OOOO000 ]==27 and np .sum (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ,:,:])>O00O0OOO000000OO0 *0.0025 *0.5 :#line:258
                OO000O0OO0OO0000O =np .sum (np .array (OOOO0O0OO0OOO00O0 [OO0OO0OOO0OOOO000 ]))#line:259
                if OO000O0OO0OO0000O >O000OO0OOO00O0000 :#line:260
                    O000OO0OOO00O0000 =OO000O0OO0OO0000O #line:261
                    OO00O0OO0O0000OOO =OO0OO0OOO0OOOO000 #line:262
        if OO00O0OO0O0000OOO is not None :#line:263
            O00OO0OO00OOO0000 .append (OO00O0OO0O0000OOO )#line:264
        if verbose >0 :#line:268
            print ('valid index: {}'.format (O00OO0OO00OOO0000 ))#line:269
        if len (O00OO0OO00OOO0000 )==0 :#line:272
            O000000OO0OOOOO0O =np .ones ((h_aim ,w_aim ,3 ),'uint8')*255 #line:273
            return O000000OO0OOOOO0O #line:274
        OOOO0O0OO0OOO00O0 =OOOO0O0OO0OOO00O0 [O00OO0OO00OOO0000 ]#line:280
        OOO0OO0OOO000OO0O =np .max (OOOO0O0OO0OOO00O0 ,axis =0 )#line:284
        OOO00O0OO0O0O0O0O =np .ones ((5 ,5 ),np .uint8 )#line:308
        O0OO0O00O000O00OO =cv2 .morphologyEx (OOO0OO0OOO000OO0O ,cv2 .MORPH_CLOSE ,OOO00O0OO0O0O0O0O )#line:309
        O0OO0O00O000O00OO =np .array (O0OO0O00O000O00OO ,'uint8')#line:311
        try :#line:314
            _O000OO0OO0OO0OOO0 ,O00O000OO0O0O0000 ,_O000OO0OO0OO0OOO0 =cv2 .findContours (O0OO0O00O000O00OO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:315
        except :#line:316
            O00O000OO0O0O0000 ,_O000OO0OO0OO0OOO0 =cv2 .findContours (O0OO0O00O000O00OO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:317
        O0OOOO00OOOOO0OOO =max (O00O000OO0O0O0000 ,key =lambda O0O0OO0O00O00O0O0 :cv2 .contourArea (O0O0OO0O00O00O0O0 ))#line:320
        OOOO00O00OO0O0000 =np .zeros_like (O0OO0O00O000O00OO )#line:323
        O0OO000O00O00O000 =cv2 .drawContours (OOOO00O00OO0O0000 ,[O0OOOO00OOOOO0OOO ],-1 ,color =255 ,thickness =-1 )#line:324
        OO0000000O000O000 =np .min (np .where (O0OO000O00O00O000 >0 )[0 ])#line:328
        O0OO0O00OOOOO00O0 =np .max (np .where (O0OO000O00O00O000 >0 )[0 ])#line:329
        OO0OOO00OO00OO000 =np .min (np .where (O0OO000O00O00O000 >0 )[1 ])#line:330
        O00OO0O0000O0OOOO =np .max (np .where (O0OO000O00O00O000 >0 )[1 ])#line:331
        OO0OOOOO00000OO0O [:,:,0 ][O0OO000O00O00O000 ==0 ]=255 #line:335
        OO0OOOOO00000OO0O [:,:,1 ][O0OO000O00O00O000 ==0 ]=255 #line:336
        OO0OOOOO00000OO0O [:,:,2 ][O0OO000O00O00O000 ==0 ]=255 #line:337
        O0OO000000O00000O =cv2 .cvtColor (OO0OOOOO00000OO0O ,cv2 .COLOR_BGR2RGB )#line:341
        O0OO000000O00000O =Image .fromarray (O0OO000000O00000O )#line:342
        O0OO000000O00000O =O0OO000000O00000O .crop ((OO0OOO00OO00OO000 ,OO0000000O000O000 ,O00OO0O0000O0OOOO ,O0OO0O00OOOOO00O0 ))#line:349
        O0O0O000OO0000O0O ,O00OOO0O0OOO0O0OO =O0OO000000O00000O .size #line:350
        OOO0OO0O0OOO000OO =int (h_aim *0.95 )#line:353
        O0OO000000O00000O =O0OO000000O00000O .resize ((int (O0O0O000OO0000O0O *OOO0OO0O0OOO000OO /O00OOO0O0OOO0O0OO ),OOO0OO0O0OOO000OO ),Image .BICUBIC )#line:354
        O0O0O000OO0000O0O ,O00OOO0O0OOO0O0OO =O0OO000000O00000O .size #line:355
        OO0O00OO00OOOO0O0 =Image .new ('RGB',(w_aim ,h_aim ),(255 ,255 ,255 ))#line:359
        OO0O00OO00OOOO0O0 .paste (O0OO000000O00000O ,(w_aim //2 -O0O0O000OO0000O0O //2 ,int (h_aim *0.03 )))#line:360
        return OO0O00OO00OOOO0O0 #line:366
    return O00O000OO0OOOO000 #line:418
def evalimage (OOO00000O0000OO00 ,OOOO00O00000OOO0O :Yolact ,OOOO00O0O0O0OOO0O :str ,save_path :str =None ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:422
    OO0O0000OOO0O0000 =torch .from_numpy (OOO00000O0000OO00 ).float ()#line:424
    O0OO00OOOO000000O =FastBaseTransform ()(OO0O0000OOO0O0000 .unsqueeze (0 ))#line:425
    O0000OOOOO0OOOO0O =OOOO00O00000OOO0O (O0OO00OOOO000000O )#line:426
    OOOO0O000000OO000 =prep_display (OOO00000O0000OO00 ,O0000OOOOO0OOOO0O ,OO0O0000OOO0O0000 ,None ,None ,undo_transform =False ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:429
    return OOOO0O000000OO000 #line:435
def evaluate (O0OOO00OO000OO0O0 :Yolact ,OOOOO0O00000OOOO0 ,OOOOO0000000O0OOO ,train_mode =False ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:440
    O0OOO00OO000OO0O0 .detect .use_fast_nms =args .fast_nms #line:441
    cfg .mask_proto_debug =args .mask_proto_debug #line:442
    O00O000OOO0OOOOOO ,O000O00OO0OO0000O =args .image .split (':')#line:444
    OOOO0O0O0OOO0O00O =evalimage (OOOOO0000000O0OOO ,O0OOO00OO000OO0O0 ,O00O000OOO0OOOOOO ,O000O00OO0OO0000O ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:445
    return OOOO0O0O0OOO0O00O #line:446
class tool_mask :#line:482
    def __init__ (O00OO000O0OO0O00O ,O0OO000O0O000O0OO ):#line:483
        parse_args (model_path =O0OO000O0O000O0OO )#line:486
        if args .config is None :#line:488
            O0OO000O0O000O0OO =SavePath .from_str (args .trained_model )#line:489
            args .config =O0OO000O0O000O0OO .model_name +'_config'#line:491
            set_cfg (args .config )#line:493
        with torch .no_grad ():#line:495
            print ('Loading mask model...',end ='')#line:499
            O00OO000O0OO0O00O .net =Yolact ()#line:500
            O00OO000O0OO0O00O .net .load_weights (args .trained_model )#line:501
            O00OO000O0OO0O00O .net .eval ()#line:503
            print ('Done.')#line:504
            if args .cuda :#line:506
                O00OO000O0OO0O00O .net =O00OO000O0OO0O00O .net #line:508
    def __del__ (O0OOOOOO000000000 ):#line:512
        pass #line:513
    def do_mask (O0OOOOOO0O00000OO ,OOOO000O0OOOOOO00 ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:516
        parse_args ()#line:518
        OOOO000O0OOOOOO00 =cv2 .cvtColor (OOOO000O0OOOOOO00 ,cv2 .COLOR_RGB2BGR )#line:521
        with torch .no_grad ():#line:523
            O000O00000OOO0OOO =None #line:525
            OOO0O000O0OOO0000 =evaluate (O0OOOOOO0O00000OO .net ,O000O00000OOO0OOO ,OOOO000O0OOOOOO00 ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:527
        if verbose >0 :#line:531
            print ('mask end.')#line:532
        return np .array (OOO0O000O0OOO0000 ,'uint8')#line:533
if __name__ =='__main__':#line:537
    pass #line:539
