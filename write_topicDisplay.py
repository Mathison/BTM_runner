#!/usr/bin/env python
#coding=utf-8
# Function: translate the results from BTM
# Input:
#    mat/pw_z.k20

import sys
import os
# return:    {wid:w, ...}
def read_vocab(pt):
    voca = {}
    for index,l in enumerate(open(pt)):
        try:
            w = str(l.replace('\n',''))
            voca[int(index)] = w
        except Exception as e:
            print(e) 
    return voca

def read_pz(pt):
    return [float(p) for p in open(pt).readline().split()]
    
# voca = {wid:w,...}
def dispTopics(pt, voca, pz):
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True)
        #tmps = ' '.join(['%s' % voca[w] for w,v in wvs[:10]])
        tmps = ' '.join(['%s:%f' % (voca[w],v) for w,v in wvs[:30]])
        topics.append((pz[k], tmps))
        k += 1
        
    print('p(z)\t\tTop words')
    for pz, s in topics:
        print('%f\t%s' % (pz, s))

def writeTopics(dir, pt, voca, pz,K,W,model_dir):
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True)
        tmps = ' '.join(['%s:%f' % (voca[w],v) for w,v in wvs[:30]])
        topics.append((pz[k], tmps))
        k += 1
    
    write_file = open(dir + model_dir + '_topic.txt','w')
    write_file.write('K:%d, n(W):%d' % (K, W))
    write_file.write('\n')
    write_file.write('p(z)\t\tTop words')
    write_file.write('\n')
    for pz, s in topics:
        write_file.write('%f %s' % (pz, s))
        write_file.write('\n')
    write_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python %s <file_path> <model_dir> <K> <voca_pt>' % sys.argv[0])
        print('\tmodel_dir    the output dir of BTM')
        print('\tK    the number of topics')
        print('\tvoca_pt    the vocabulary file')
        exit(1)

    dir = sys.argv[1]  ####the directory to put all BTM, vocab.txt and index.txt   
    model_dir = sys.argv[2]  ###just the name of the BTM folder
    K = int(sys.argv[3])
    voca_pt = sys.argv[4]  ###just the name of the vocab file

    voca = read_vocab(dir + voca_pt)    
    W = len(voca)

    pz_pt = dir + model_dir + '/' + 'k%d.pz' % K

    pz = read_pz(pz_pt)
    
    zw_pt = dir + model_dir + '/' + 'k%d.pw_z' %  K
    #dispTopics(zw_pt, voca, pz)
    writeTopics(dir,zw_pt, voca, pz,K,W,model_dir)