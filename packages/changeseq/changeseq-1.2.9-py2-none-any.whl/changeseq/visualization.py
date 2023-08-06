from __future__ import print_function
    
import svgwrite
import os
import logging
import argparse
import pandas as pd

### 2017-October-11: Adapt plots to new output; inputs are managed using "argparse".

logger = logging.getLogger('root')
logger.propagate = False

boxWidth = 10
box_size = 15
v_spacing = 3

# colors = {'G': '#F5F500', 'A': '#FF5454', 'T': '#00D118', 'C': '#26A8FF', 'N': '#B3B3B3', '-': '#B3B3B3'}
colors = {'G': '#F5F500', 'A': '#FF5454', 'T': '#00D118', 'C': '#26A8FF', 'N': '#B3B3B3', 'R': '#B3B3B3', '-': '#B3B3B3'}
for c in ['Y','S','W','K','M','B','D','H','V','.']:
    colors[c] = "#B3B3B3"
    
def parse_homer(identified,homer_output,genome):
    select_col="Annotation"
    command = "annotatePeaks.pl %s %s > %s"%(identified,genome,homer_output)
    os.system(command)
    df = pd.read_csv(identified,sep="\t")
    df.index = df['Genomic Coordinate'].to_list()
    df2 = pd.read_csv(homer_output,sep="\t",index_col=0)
    df['Annotation'] = df2[select_col]
    out = identified.replace(".txt",".annot.tsv")
    df.to_csv(out,sep="\t",index=False)
    return out
def parseSitesFile(infile):
    offtargets = []
    total_seq = 0
    with open(infile, 'r') as f:
        f.readline()
        for line in f:
            line = line.rstrip('\n')
            line_items = line.split('\t')
            # offtarget_reads = line_items[4]
            # no_bulge_offtarget_sequence = line_items[10]
            # bulge_offtarget_sequence = line_items[15]
            # target_seq = line_items[28]
            # realigned_target_seq = line_items[29]
            offtarget_reads = line_items[4]
            no_bulge_offtarget_sequence = line_items[7]
            bulge_offtarget_sequence = line_items[9]
            target_seq = line_items[14]
            realigned_target_seq = line_items[15]
            coord = line_items[3]
            num_mismatch = line_items[8]
            try:
                annot = line_items[16]
            except:
                annot = ""

            if no_bulge_offtarget_sequence != '' or bulge_offtarget_sequence != '':
                if no_bulge_offtarget_sequence:
                    total_seq += 1
                if bulge_offtarget_sequence:
                    total_seq += 1
                offtargets.append({'seq': no_bulge_offtarget_sequence.strip(),
                                   'bulged_seq': bulge_offtarget_sequence.strip(),
                                   'reads': int(offtarget_reads.strip()),
                                   'coord': str(coord),
                                   'annot': str(annot),
                                   'num_mismatch': str(num_mismatch),
                                   'target_seq': target_seq.strip(),
                                   'realigned_target_seq': realigned_target_seq.strip()
                                   })
    offtargets = sorted(offtargets, key=lambda x: x['reads'], reverse=True)
    return offtargets, target_seq, total_seq

# 3/6/2020 Yichao
def check_mismatch(a,b):
    from Bio.Data import IUPACData
    dna_dict = IUPACData.ambiguous_dna_values
    set_a = dna_dict[a.upper()]
    set_b = dna_dict[b.upper()]
    overlap = list(set(list(set_a)).intersection(list(set_b)))
    if len(overlap) == 0:
        return True
    else:
        return False
from Bio import SeqUtils
def find_PAM(seq,PAM):
	try:
		PAM_index = seq.index(PAM)
	except:
		# PAM on the left
		left_search = SeqUtils.nt_search(seq[:len(PAM)], PAM)
		if len(left_search)>1:
			PAM_index = left_search[1]
		else:
			right_search = SeqUtils.nt_search(seq[-len(PAM):], PAM)
			if len(right_search)>1:
				PAM_index = len(seq)-len(PAM)
			else:
				print ("PAM: %s not found in %s. Set PAM index to 20"%(PAM,seq))
				PAM_index=20
	return PAM_index

def visualizeOfftargets(infile, outfile, title, PAM, genome=None):

    output_folder = os.path.dirname(outfile)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    if genome!=None:
        infile = parse_homer(infile,outfile+".raw.homer.tsv",genome)
    # Get offtargets array from file
    offtargets, target_seq, total_seq = parseSitesFile(infile)

    # Initiate canvas
    dwg = svgwrite.Drawing(outfile + '.svg', profile='full', size=(u'100%', 100 + total_seq*(box_size + 1)))

    if title is not None:
        # Define top and left margins
        x_offset = 20
        y_offset = 50
        dwg.add(dwg.text(title, insert=(x_offset, 30), style="font-size:20px; font-family:Courier"))
    else:
        # Define top and left margins
        x_offset = 20
        y_offset = 20

    # Draw ticks
    # if target_seq.find('N') >= 0:
        # p = target_seq.index('N')
        # if p > len(target_seq) / 2:  # PAM on the right end
            # tick_locations = [1, len(target_seq)] + range(p, len(target_seq))  # limits and PAM
            # tick_locations += [x + p - 20 + 1 for x in range(p)[::10][1:]]  # intermediate values
            # tick_locations = list(set(tick_locations))
            # tick_locations.sort()
            # tick_legend = [p, 10, 1] + ['P', 'A', 'M']
        # else:
            # tick_locations = range(2, 6) + [14, len(target_seq)]  # complementing PAM and limits
            # tick_legend = ['P', 'A', 'M', '1', '10'] + [str(len(target_seq) - 4)]

        # for x, y in zip(tick_locations, tick_legend):
            # dwg.add(dwg.text(y, insert=(x_offset + (x - 1) * box_size + 2, y_offset - 2), style="font-size:10px; font-family:Courier"))
    # else:
        # tick_locations = [1, len(target_seq)]  # limits
        # tick_locations += range(len(target_seq) + 1)[::10][1:]
        # tick_locations.sort()
        # for x in tick_locations:
            # dwg.add(dwg.text(str(x), insert=(x_offset + (x - 1) * box_size + 2, y_offset - 2), style="font-size:10px; font-family:Courier"))
    ## Assume PAM is on the right end Yichao rewrite visualization code, generic PAM
    ## PAM can be on the left or right, Yichao 0713
    tick_locations = []
    tick_legend = []
    # PAM_index = target_seq.index(PAM)
    PAM_index = find_PAM(target_seq,PAM)
    count = 0
    for i in range(PAM_index,0,-1):
        count = count+1
        if count % 10 == 0:
            tick_legend.append(count)
            # print (count,i)
            tick_locations.append(i)
    if len(PAM)>=3:
        tick_legend+=['P', 'A', 'M']+['-']*(len(PAM)-3)
    else:
        tick_legend+=["PAM"]+['-']*(len(PAM)-3)
    tick_locations+=range(PAM_index+1,len(target_seq)+1)
    if PAM_index == 0:
        tick_legend = []
        tick_locations = []
        tick_legend+=['P', 'A', 'M']+['-']*(len(PAM)-3)
        tick_locations+=range(1,len(PAM)+1)
        count = 0
        for i in range(len(PAM)+1,len(target_seq)+1):
            count = count+1
            if count % 10 == 0 or count == 1:
                tick_legend.append(count)
                # print (count,i)
                tick_locations.append(i)
    # print (zip(tick_locations, tick_legend))
    for x,y in zip(tick_locations, tick_legend):
        dwg.add(dwg.text(y, insert=(x_offset + (x - 1) * box_size + 2, y_offset - 2), style="font-size:10px; font-family:Courier"))

    # Draw reference sequence row
    for i, c in enumerate(target_seq):
        y = y_offset
        x = x_offset + i * box_size
        dwg.add(dwg.rect((x, y), (box_size, box_size), fill=colors[c]))
        dwg.add(dwg.text(c, insert=(x + 3, y + box_size - 3), fill='black', style="font-size:15px; font-family:Courier"))
    dwg.add(dwg.text('Reads', insert=(x_offset + box_size * len(target_seq) + 16, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))
    dwg.add(dwg.text('Mismatches', insert=(box_size * (len(target_seq) + 1) + 90, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))
    dwg.add(dwg.text('Coordinates', insert=(box_size * (len(target_seq) + 1) + 200, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))
    if genome!=None:
        dwg.add(dwg.text('Annotation', insert=(box_size * (len(target_seq) + 1) + 450, y_offset + box_size - 3), style="font-size:15px; font-family:Courier"))

    # Draw aligned sequence rows
    y_offset += 1  # leave some extra space after the reference row
    line_number = 0  # keep track of plotted sequences
    for j, seq in enumerate(offtargets):
        realigned_target_seq = offtargets[j]['realigned_target_seq']
        no_bulge_offtarget_sequence = offtargets[j]['seq']
        bulge_offtarget_sequence = offtargets[j]['bulged_seq']

        if no_bulge_offtarget_sequence != '':
            k = 0
            line_number += 1
            y = y_offset + line_number * box_size
            for i, (c, r) in enumerate(zip(no_bulge_offtarget_sequence, target_seq)):
                x = x_offset + k * box_size
                if r == '-':
                    if 0 < k < len(target_seq):
                        x = x_offset + (k - 0.25) * box_size
                        dwg.add(dwg.rect((x, box_size * 1.4 + y), (box_size*0.6, box_size*0.6), fill=colors[c]))
                        dwg.add(dwg.text(c, insert=(x+1, 2 * box_size + y - 2), fill='black', style="font-size:10px; font-family:Courier"))
                elif c == r:
                    dwg.add(dwg.text(u"\u2022", insert=(x + 4.5, 2 * box_size + y - 4), fill='black', style="font-size:10px; font-family:Courier"))
                    k += 1
                elif r == 'N':
                    dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
                    k += 1
                else:
                    dwg.add(dwg.rect((x, box_size + y), (box_size, box_size), fill=colors[c]))
                    dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
                    k += 1
        if bulge_offtarget_sequence != '':
            k = 0
            line_number += 1
            y = y_offset + line_number * box_size
            for i, (c, r) in enumerate(zip(bulge_offtarget_sequence, realigned_target_seq)):
                x = x_offset + k * box_size
                if r == '-':
                    if 0 < k < len(realigned_target_seq):
                        x = x_offset + (k - 0.25) * box_size
                        dwg.add(dwg.rect((x, box_size * 1.4 + y), (box_size*0.6, box_size*0.6), fill=colors[c]))
                        dwg.add(dwg.text(c, insert=(x+1, 2 * box_size + y - 2), fill='black', style="font-size:10px; font-family:Courier"))
                elif c == r:
                    dwg.add(dwg.text(u"\u2022", insert=(x + 4.5, 2 * box_size + y - 4), fill='black', style="font-size:10px; font-family:Courier"))
                    k += 1
                elif r == 'N':
                    dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
                    k += 1
                else:
                    dwg.add(dwg.rect((x, box_size + y), (box_size, box_size), fill=colors[c]))
                    dwg.add(dwg.text(c, insert=(x + 3, 2 * box_size + y - 3), fill='black', style="font-size:15px; font-family:Courier"))
                    k += 1

        if no_bulge_offtarget_sequence == '' or bulge_offtarget_sequence == '':
            reads_text = dwg.text(str(seq['reads']), insert=(box_size * (len(target_seq) + 1) + 20, y_offset + box_size * (line_number + 2) - 2),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(reads_text)
            mismatch_text = dwg.text(seq['num_mismatch'], insert=(box_size * (len(target_seq) + 1) + 130, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(mismatch_text)
            mismatch_text = dwg.text(seq['coord'], insert=(box_size * (len(target_seq) + 1) + 200, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(mismatch_text)
            if genome!= None:
                annot_text = dwg.text(seq['annot'], insert=(box_size * (len(target_seq) + 1) + 450, y_offset + box_size * (line_number + 1) + 5),
                                      fill='black', style="font-size:15px; font-family:Courier")
                dwg.add(annot_text)
        else:
            reads_text = dwg.text(str(seq['reads']), insert=(box_size * (len(target_seq) + 1) + 20, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(reads_text)
            mismatch_text = dwg.text(seq['num_mismatch'], insert=(box_size * (len(target_seq) + 1) + 130, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(mismatch_text)
            mismatch_text = dwg.text(seq['coord'], insert=(box_size * (len(target_seq) + 1) + 200, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:15px; font-family:Courier")
            dwg.add(mismatch_text)
            if genome!= None:
                annot_text = dwg.text(seq['annot'], insert=(box_size * (len(target_seq) + 1) + 450, y_offset + box_size * (line_number + 1) + 5),
                                      fill='black', style="font-size:15px; font-family:Courier")
                dwg.add(annot_text)
            reads_text02 = dwg.text(u"\u007D", insert=(box_size * (len(target_seq) + 1) + 7, y_offset + box_size * (line_number + 1) + 5),
                                  fill='black', style="font-size:23px; font-family:Courier")
            dwg.add(reads_text02)
    dwg.save()

def main():
    parser = argparse.ArgumentParser(description='Plot visualization plots for re-aligned reads.')
    parser.add_argument("-f","--identified_file", help="FullPath/output file from reAlignment_circleseq.py", required=True)
    parser.add_argument("-o","--outfile", help="FullPath/VIZ", required=True)
    parser.add_argument("-t","--title", help="Plot title", required=True)
    parser.add_argument("-g","--genome", help="if specified, homer annotation will be performed", default=None)
    parser.add_argument("--PAM", help="PAM sequence", default="NGG")    
    args = parser.parse_args()

    print(args)

    visualizeOfftargets(args.identified_file, args.outfile, args.title, args.PAM,args.genome)

if __name__ == "__main__":

    main()
