from __future__ import division

import sys, time, getopt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
import matplotlib
# matplotlib.use('Agg')
plt.switch_backend('Agg')
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from os import listdir
from os.path import isfile, join
import mpmath as mp

mp.dps = 15

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True
rcParams["figure.figsize"] = (12,10)

def plot_datasets(dataset, view, utilization):
    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust (top = 0.5, bottom = 0.2, left = 0.1, right = 0.95, hspace = 0.3, wspace=0.05)

    bxinput = []
    ori = []
    conv_carry = []
    conv_inflation = []
    carry = []
    inflation = []
    for inputs in dataset:
        #ori.append(inputs[0])
        conv_carry.append(inputs[0])
        conv_inflation.append(inputs[1])
        carry.append(inputs[2])
        inflation.append(inputs[3])
        #print(inputs)
    #bxinput.append(ori)
    bxinput.append(conv_carry)
    bxinput.append(conv_inflation)
    bxinput.append(carry)
    bxinput.append(inflation)
    #print (bxinput)

    ax.set_yscale("log")
    ax.set_ylabel('WCDFP (log-scale)',size=20)
    ax.tick_params(axis='both', which='major',labelsize=12)
    
    #labels = ['Original', 'Carry-In', 'Inflation']
    labels = ['Conv-CarryIn','Conv-Inflation', 'CB-CarryIn', 'CB-Inflation']
    #the blue box
    boxprops = dict(linewidth=2, color='blue')
    #the median line
    medianprops = dict(linewidth=2.5, color='orange')
    whiskerprops = dict(linewidth=2.5, color='black')
    capprops = dict(linewidth=2.5)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(25)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(25)

    try:
        ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops)
    except ValueError:
        print ("ValueError")

    box = mpatches.Patch(color='blue', label='1st to 3rd Quartiles', linewidth=3)
    av = mpatches.Patch(color='orange', label='Median', linewidth=3)
    whisk = mpatches.Patch(color='black', label='Whiskers', linewidth=3)
    ax.grid()
    plt.legend(handles=[av, box, whisk], fontsize=12, frameon=True, loc=5)
    #plt.clf()
    #plt.show()
    return fig

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:u:s:m:f:h:rv:", ["ident=", "utilization=", "num_sets=", "max_fault_rate=", "fault_rate_step_size=", "hard_task_factor=", "rounded", "view="])
    except getopt.GetoptError as err:
        print (str(err))
        sys.exit(2)

    # num_tasks,
    num_sets, max_fault_rate, step_size_fault_rate, hard_task_factor = 0, 0, 0, 0
    ident, view, title = None, None, None
    rounded = False

    utilization = 50
    #utilization = 70
    for opt, arg in opts:
        if opt in ('-i', '--ident'):
            ident = str(arg)
        # if opt in ('-n', '--num_tasks'):
        #     num_tasks = int(arg)
        if opt in ('-u', '--utilization'):
            utilization = int(arg)
        # if opt in ('-s', '--num_sets'):
        #     num_sets = int(arg)
        if opt in ('-m', '--max_fault_rate'):
            max_fault_rate = min(1.0, float(arg))
        if opt in ('-f', '--fault_rate_step_size'):
            step_size_fault_rate = min(1.0, float(arg))
        if opt in ('-h', '--hard_task_factor'):
            hard_task_factor = float(arg)
        if opt in ('-r', '--rounded'):
            rounded = True
        if opt in ('-v', '--view'):
            view = str(arg)

    datasets = []
    # for fault_rate in np.arange(step_size_fault_rate, max_fault_rate + step_size_fault_rate, step_size_fault_rate):
    dataset = []

    #for num_tasks, num_sets in zip([2, 3, 5], [20, 20, 20]):
    for num_tasks, num_sets in zip([2, 3, 5], [10, 10, 10, 10]):
        if ident is not None:
            #filename_ori = 'res_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) +str('r' if rounded else '')
            filename_carry = 'res_carry_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) +str('r' if rounded else '')
            filename_inflation = 'res_inflation_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) + str('r' if rounded else '')
            filename_conv_carry = 'res_conv_carry_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) + str('r' if rounded else '')
            filename_conv_inflation = 'res_conv_inflation_tasksets_' + ident + '_n_' + str(num_tasks) + 'u_' + str(utilization) + '_m' + str(num_sets) + 's_'+ str(max_fault_rate) + 'f_' + str(step_size_fault_rate) + 'h_'+ str(hard_task_factor) + str('r' if rounded else '')
            try:
                #results_ori = np.load('../results/' + filename_ori + '.npy', allow_pickle=True)
                results_conv_inflation = np.load('../results/' + filename_conv_inflation + '.npy', allow_pickle=True)
                results_conv_carry = np.load('../results/' + filename_conv_carry + '.npy', allow_pickle=True)
                results_carry = np.load('../results/' + filename_carry + '.npy', allow_pickle=True)
                results_inflation = np.load('../results/' + filename_inflation + '.npy', allow_pickle=True)
                if view == 'prob_log':
                    for res_carry, res_inflation, res_conv_carry, res_conv_inflation in zip(results_carry, results_inflation, results_conv_carry, results_conv_inflation):
                        dataset.append([res_conv_carry, res_conv_inflation, res_carry['ErrProb'], res_inflation['ErrProb']])
                    plot = plot_datasets(dataset, view, utilization)
                    save_pdf = PdfPages('./'+ ident + '_' + str(num_tasks) + '_' + str(num_sets)+ '_' + str(view) + '_' +str(utilization)+ '_'+str(hard_task_factor)+'_'+str(max_fault_rate)+'.pdf')
                    # save_pdf = PdfPages(ident  + '_' + str(view) + '.pdf')
                    save_pdf.savefig(plot, bbox_inches='tight', pad_inches=0.0)
                    save_pdf.close()

                if view == 'counter':
                    counterInflation = 0
                    counterCarry = 0
                    same = 0
                    for res_carry, res_inflation, res_conv_carry, res_conv_inflation in zip(results_carry, results_inflation, results_conv_carry, results_conv_inflation):
                        if res_conv_carry > res_conv_inflation:
                            counterInflation +=1
                            print('Res: carry'+str(res_conv_carry)+' inflation'+str(res_conv_inflation))
                        elif res_conv_inflation > res_conv_carry:
                            counterCarry +=1
                        else:
                            same +=1                    
                    print ('BestU: '+str(utilization)+' TasksPerSet:'+str(num_tasks) +' Fault Rate: '+str(max_fault_rate)+' X: '+ str(hard_task_factor) + ' Inflation-Win: '+ str(counterInflation) + ' Carry-Win: ' + str(counterCarry) + ' BothSame: '+str(same))

            except Exception as e:
                print (e)
                continue
        else:
            print ('Must specify identifier')
            return
        
if __name__=="__main__":
    main()
