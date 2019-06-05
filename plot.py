import pandas as pd
import numpy as np
import glob
import json
import matplotlib.pyplot as plt

SEARCH_PATTERN = '*{vid}-{res}_crf_{crf}_maxdur_{maxdur}_{enc}_{cbrcapped}*'

def get_size_vmaf(vid,res,crf,maxdur,enc,cbrcapped):
    searchfor = SEARCH_PATTERN.format(**locals())
    print(searchfor)
    statdir = glob.glob(searchfor)
    if len(statdir) > 0:
        statdir = statdir[0]
        vmaf = np.mean(pd.read_csv(statdir + '/psnr_ssim_vmaf.csv')['vmaf'])
        with open(statdir + '/vid_opts.json') as f:
            vid_opts = json.load(f)
            # add sanity checks
            if cbrcapped == 'cbr' in vid_opts:
                if not 'cst_bitrate':
                    print("ERROR")
                    return None
                if not 'meanrate' in vid_opts:
                    print("ERROR")
                    return None
        with open(statdir + '/video_statistics.json') as f:
            vid_stats = json.load(f)
        
        return float(vid_stats['size_total'])/(1000000*8), vmaf

var_vmaf_4 =  get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[1]
var_vmaf_10 =  get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[1]

Bunny_vmaf = {
    4 : {
        'VAR' : get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[1], \
        'NA' : get_size_vmaf('BigBuckBunny',2160,16,'3c0','fix','cbr')[1], \
        'EM' : get_size_vmaf('BigBuckBunny',2160,16,'4c0','fix','cbr')[1]
    },
    10 : {
        'VAR' : get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[1], \
        'NA' : get_size_vmaf('BigBuckBunny',2160,16,'4c5','fix','cbr')[1], \
        'EM' : get_size_vmaf('BigBuckBunny',2160,16,'10c0','fix','cbr')[1]
    }
}

Bunny_vmaf_diff = {
    4 : {
        'VAR' : var_vmaf_4 - get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[1], \
        'NA' : var_vmaf_4 - get_size_vmaf('BigBuckBunny',2160,16,'3c0','fix','cbr')[1], \
        'EM' : var_vmaf_4 - get_size_vmaf('BigBuckBunny',2160,16,'4c0','fix','cbr')[1]
    },
    10 : {
        'VAR' : var_vmaf_10 - get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[1], \
        'NA' : var_vmaf_10 - get_size_vmaf('BigBuckBunny',2160,16,'4c5','fix','cbr')[1], \
        'EM' : var_vmaf_10 - get_size_vmaf('BigBuckBunny',2160,16,'10c0','fix','cbr')[1]
    }
}


Bunny_sizes = {
    4 : {
        'VAR' : get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[0], \
        'NA' : get_size_vmaf('BigBuckBunny',2160,16,'3c0','fix','cbr')[0] , \
        'EM' : get_size_vmaf('BigBuckBunny',2160,16,'4c0','fix','cbr')[0]
    },
    10 : {
        'VAR' : get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[0], \
        'NA' : get_size_vmaf('BigBuckBunny',2160,16,'4c5','fix','cbr')[0], \
        'EM' : get_size_vmaf('BigBuckBunny',2160,16,'10c0','fix','cbr')[0]
    }
}

var_filesize_4 =  get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[0]
var_filesize_10 =  get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[0]

Bunny_sizes_diff = {
    4 : {
        'VAR' : (get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[0] - var_filesize_4) \
             / get_size_vmaf('BigBuckBunny',2160,16,'4c0','var','cbr')[0], \
        'NA' : (get_size_vmaf('BigBuckBunny',2160,16,'3c0','fix','cbr')[0] - var_filesize_4) \
            / get_size_vmaf('BigBuckBunny',2160,16,'3c0','fix','cbr')[0], \
        'EM' : (get_size_vmaf('BigBuckBunny',2160,16,'4c0','fix','cbr')[0] - var_filesize_4) \
            / get_size_vmaf('BigBuckBunny',2160,16,'4c0','fix','cbr')[0]
    },
    10 : {
        'VAR' : (get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[0] - var_filesize_10) \
            / get_size_vmaf('BigBuckBunny',2160,16,'10c0','var','cbr')[0], \
        'NA' : (get_size_vmaf('BigBuckBunny',2160,16,'4c5','fix','cbr')[0] - var_filesize_10) \
            / get_size_vmaf('BigBuckBunny',2160,16,'4c5','fix','cbr')[0], \
        'EM' : (get_size_vmaf('BigBuckBunny',2160,16,'10c0','fix','cbr')[0] - var_filesize_10) \
            /   get_size_vmaf('BigBuckBunny',2160,16,'10c0','fix','cbr')[0]
    }
}

font = {'family' : 'normal',
    'weight' : 'normal',
    'size'   : 20}
plt.rc('font', **font)

ax = plt.gca()
df_results = pd.DataFrame.from_dict(Bunny_vmaf, orient='index')
boxplot_results = df_results.plot.bar(ax=ax,rot=0)
ax.set_xlabel('Video')
ax.set_ylabel('VMAF')
ax.legend(loc='center')
plt.tight_layout() 
plt.savefig('vmaf.pdf')
plt.close()

ax = plt.gca()
df_results = pd.DataFrame.from_dict(Bunny_vmaf_diff, orient='index')
boxplot_results = df_results.plot.bar(ax=ax,rot=0)
ax.set_xlabel('Video')
ax.set_ylabel(r'$vmaf_{var} - vmaf_{x}$')
ax.legend(loc='center')
plt.tight_layout() 
plt.savefig('vmaf_diff.pdf')
plt.close()

ax = plt.gca()
df_results = pd.DataFrame.from_dict(Bunny_sizes, orient='index')
boxplot_results = df_results.plot.bar(ax=ax,rot=0)
ax.set_xlabel('Video')
ax.set_ylabel('Filesize (MBit/s)')
ax.legend(loc='center')
plt.tight_layout() 
plt.savefig('sizes.pdf')
plt.close()

ax = plt.gca()
df_results = pd.DataFrame.from_dict(Bunny_sizes_diff, orient='index')
boxplot_results = df_results.plot.bar(ax=ax,rot=0)
ax.set_xlabel('Video')
ax.set_ylabel(r'$\frac{vmaf_{var} - vmaf_{x}}{vmaf_{x}}$')
ax.legend(loc='center')
plt.tight_layout() 
plt.savefig('sizes_diff.pdf')
plt.close()