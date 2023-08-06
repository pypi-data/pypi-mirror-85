import copy
import math
import os
import re

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.cycles as cyc
import networkx.algorithms.dag as dag
import numpy as np
import pandas as pd


#################################################################################################
# Author: Alex Z
# Last Modification: 25/10/2020
# Version: 116d

# dependencies: python 3.6+, networkx, matplotlib, numpy, pandas
#################################################################################################


# Read input workbook into pandas dataframes, input path to workbook, output data_dict with equipment details
# data_dict = {1:data_cs, 2:data_sc, 3:data_cv, 4:data_bn, 5:data_stock, 6:data_trp, 7:data_apf, 8:data_splt, 9:data_prif, 21: data_sc_dst, 22: data_sc_pct}
'''
1. the split percentage to priority feeders will be 100% to mode 1 and 0 to the others.
'''
def access_data(path):
    """
    Purpose:
        Read input workbook into pandas dataframes, input path to workbook, output data_dict with equipment details

    Args:
        path (str): path to the input workbook file

    Returns: 
        data_dict (dict): equipment details in dataframe
        data_dict = {1:data_cs, 2:data_sc, 3:data_cv, 4:data_bn, 5:data_stock, 6:data_trp, 7:data_apf, 8:data_splt, 9:data_prif, 21: data_sc_dst, 22: data_sc_pct}
    """
    
    try:
        path = os.path.normpath(path)
        input_file = pd.ExcelFile(path, engine='pyxlsb')
    except FileNotFoundError:
        print('File '+ path + 'cannot be found.')
        return

    '''Reading data from workbook to dataframe, starts'''
    # screen details
    data_sc = pd.read_excel(input_file, 'Screen_details',skiprows=range(0,8))
    # version 108G or after, for KD2, screens now have ore type split group index
    data_sc = data_sc.loc[(data_sc['Screen active'] == 1)&(pd.isnull(data_sc['Screen name']) == False),['Index','Screen name','Capacity (tonnes)','Maximum screen rate (Tonnes per hour)', 'Screen ore type split Group index']]
    data_sc.rename(columns={'Screen name':'name','Capacity (tonnes)':'capacity','Maximum screen rate (Tonnes per hour)':'rate', 'Screen ore type split Group index':'sc_group_id'},inplace=True)
    data_sc = data_sc.set_index('Index')

    # crusher details
    data_cs = pd.read_excel(input_file, 'Crusher_details',skiprows=range(0,8))
    data_cs = data_cs.loc[(data_cs['Crusher active'] == 1)&(pd.isnull(data_cs['Crusher name']) == False),['Index','Crusher name','Capacity (tonnes)','Maximum crushing rate (Tonnes per hour)', 'Connected equipment index type', 'Equipment index']]
    data_cs.rename(columns={'Crusher name':'name','Capacity (tonnes)':'capacity','Maximum crushing rate (Tonnes per hour)':'rate', 'Connected equipment index type':'next_type_id', 'Equipment index':'next_id'},inplace=True)
    data_cs = data_cs.set_index('Index')

    # conveyor details
    data_cv = pd.read_excel(input_file, 'Conveyors',skiprows=range(0,8))
    data_cv = data_cv.loc[(data_cv['Conveyor active'] == 1)&(pd.isnull(data_cv['Conveyor name']) == False),['Index','Conveyor name','Length (Meters) ','Speed (Meters/Second)', 'Capacity (tonnes)', 'Connected equipment index type', 'Equipment index']]
    data_cv.rename(columns={'Conveyor name':'name','Capacity (tonnes)':'capacity','Length (Meters) ':'length','Speed (Meters/Second)':'speed', 'Connected equipment index type':'next_type_id', 'Equipment index':'next_id'},inplace=True)
    data_cv['rate'] = data_cv['capacity']/(data_cv['length']/data_cv['speed']/3600)
    data_cv = data_cv.set_index('Index')

    # bin details
    data_bn = pd.read_excel(input_file, 'Bin_details',skiprows=range(0,8))
    data_bn = data_bn.loc[(data_bn['Bin active'] == 1)&(pd.isnull(data_bn['Bin name']) == False),['Index','Bin name', 'Capacity (tonnes)', 'Discharge rate (Tonnes per hour)', 'Connected equipment index type', 'Equipment index']]
    data_bn.rename(columns={'Bin name':'name','Capacity (tonnes)':'capacity', 'Discharge rate (Tonnes per hour)':'rate', 'Connected equipment index type':'next_type_id', 'Equipment index':'next_id'},inplace=True)
    data_bn = data_bn.set_index('Index')

    # tripper detials
    data_trp = pd.read_excel(input_file, 'Tripper_details',skiprows=range(0,8))
    data_trp = data_trp.loc[(data_trp['Number of connected equipment'] != 0)&(pd.isnull(data_trp['Tripper name']) == False)]
    data_trp = data_trp.iloc[:,[0,1,3,8,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]]
    data_trp.rename(columns={'Tripper name':'name', 'Number of connected equipment':'connected_num', 'Connected equipment index type':'next_type_id'},inplace=True)
    data_trp.columns = data_trp.columns.str.replace('Equipment index ','next_id_')
    data_trp = data_trp.set_index('Index')

    # percentage splitter details
    # version 108G or after, for KD2, pct splitter can connect to different types of equipment
    data_splt = pd.read_excel(input_file, 'Pct_Splitter',skiprows=range(0,8))
    data_splt = data_splt.loc[(data_splt['Connected equipment 1'] != 0)&(data_splt['Equipment index 1'] != 0)&(pd.isnull(data_splt['Splitter name']) == False)]
    data_splt.rename(columns={'Splitter name':'name'},inplace=True)
    data_splt.columns = data_splt.columns.str.replace('Connected equipment ','next_type_id_')
    data_splt.columns = data_splt.columns.str.replace('Equipment index ','next_id_')
    data_splt.columns = data_splt.columns.str.replace('Percentage split ','pct_')
    data_splt = data_splt.loc[:,['Index', 'name', 'pct_1', 'pct_2', 'pct_3', 'pct_4', 'pct_5', 
                            'next_type_id_1', 'next_type_id_2', 'next_type_id_3', 'next_type_id_4', 'next_type_id_5', 
                            'next_id_1', 'next_id_2', 'next_id_3', 'next_id_4', 'next_id_5']]
    data_splt = data_splt.set_index('Index')

    # apron feeder details
    data_apf = pd.read_excel(input_file, 'Apron_feeder',skiprows=range(0,8))
    data_apf = data_apf.loc[data_apf['Active true or false value'] == 1]
    data_apf.rename(columns={'Apron feeder name':'name', 'Bin index':'pre_bin_id', 'Next type equipment connected':'next_type_id', 'Next equipment index':'next_id', 'Discharge rate (Tonnes per hour)':'rate'},inplace=True)
    data_apf = data_apf.loc[:,['Index', 'name', 'rate', 'pre_bin_id', 'next_type_id', 'next_id']]
    data_apf = data_apf.set_index('Index')


    # priority feeder detials
    data_prif = pd.read_excel(input_file, 'Priority_feeder',skiprows=range(0,8))
    data_prif = data_prif.loc[data_prif['Active true or false value'] == 1]
    data_prif.rename(columns={'Priority feeder name':'name','Activate when bin level exceeds N%':'upper_pct', 'Deactivate when bin level is less than N %':'lower_pct', 'Discharge rate (Tonnes per hour)':'rate', 'Bin index':'pre_bin_id', }, inplace=True)
    data_prif.columns = data_prif.columns.str.replace('Next type equipment connected','next_type_id')
    data_prif.columns = data_prif.columns.str.replace('Next equipment index','next_id')
    data_prif = data_prif.loc[:,['Index', 'name', 'upper_pct', 'lower_pct','rate', 'Active true or false value', 'pre_bin_id', 'next_type_id', 'next_id',
            'next_type_id.1', 'next_id.1', 'next_type_id.2', 'next_id.2']]
    data_prif = data_prif.set_index('Index')

    # stockpile group details
    data_stock = pd.read_excel(input_file, 'Stockpile_Group',skiprows=range(0,8))
    data_stock = data_stock.loc[data_stock['Active true or false value'] == 1]
    data_stock.rename(columns={'Group name':'name'}, inplace=True)
    data_stock = data_stock.iloc[:,:2]
    data_stock = data_stock.set_index('Index')

    # screen destination details
    # version 108G or after, screen desintation are assigned to screen groups
    data_sc_dst = pd.read_excel(input_file, 'Screen_destination',skiprows=range(0,8))
    data_sc_dst.rename(columns={'Screen Ore type group index':'sc_group_id','Connected equipment index type':'next_type_id', 'Equipment index':'next_id', 'Output stream':'splt_id'}, inplace=True)
    data_sc_dst = data_sc_dst.loc[:,['sc_group_id', 'splt_id', 'next_type_id', 'next_id']]

    # screen split percentage details
    '''version 108G or after, screen splits are assigned to screen groups'''
    data_sc_pct = pd.read_excel(input_file, 'Ore_type_split',skiprows=range(0,8))
    data_sc_pct.rename(columns={'Screen Ore type group index':'sc_group_id','Ore type index':'ore_type_id', 'Percentage':'pct', 
                                'In loop\n1= true\n0=false':'in_loop','Output stream':'splt_id'}, inplace=True)
    data_sc_pct = data_sc_pct.loc[:,['sc_group_id', 'splt_id', 'ore_type_id', 'pct', 'in_loop']]

    '''version before 108G, screen splits are assigned to screen'''
    # data_sc_pct = pd.read_excel(input_file, 'Ore_type_split',skiprows=range(0,8))
    # data_sc_pct.rename(columns={'Screen index':'sc_id','Ore type index':'ore_type_id', 'Percentage':'pct', 'In loop\n1= true\n0=false':'in_loop','Output stream':'splt_id'}, inplace=True)
    # data_sc_pct = data_sc_pct.iloc[:,[0,2,3,5,6,7]]
    
    '''Reading data from workbook to dataframe, ends''' 

    # Access End
    input_file.close()
    data_dict = {1:data_cs, 2:data_sc, 3:data_cv, 4:data_bn, 5:data_stock, 6:data_trp, 7:data_apf, 8:data_splt, 9:data_prif, 21:data_sc_dst, 22:data_sc_pct}
    return data_dict                                                                                                                          

def generate_graph(data_dict, lvl_lim=0, ore_type_num=1):
    """
    Purpose:
        generate a directed graph

    Args:
        data_dict (dict): dictionary with all the equipment detail data
        lvl_lim (int): control how many steps a node can search downstream
        ore_type_num (positive int): the number of ore types we are searching in screen split percentages. 

    Returns: 
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details, return an empty graph if ore_type_num is a none positive non integer number.
    """
    ep_map = nx.DiGraph()

    if ore_type_num <= 0 or type(ore_type_num) != int:
        print('ore_type_num must be an integer greater than 0')
        return ep_map

    # Generate graph by searching from all nodes from all 9 types of equipment
    for ep_type in range(1,10):
        data = data_dict[ep_type]
        for ep_id in data.index:
            find_neighbour_node(ep_id,ep_type,ep_map, data_dict, lvl_lim=lvl_lim, ore_type_num=ore_type_num)

    return ep_map

def find_neighbour_node(ep_id, type_id, ep_map, data_dict, lvl_lim=0, lvl_current=0, pre_name='', ore_type_num=1):
    """
    recursively find neighbour equipment and update graph

    Args:
        ep_id (int): equipment index of a specific equipment type
        type_id (int): equipment type
        ep_map (networkx.DiGraph): the empty directed graph to be updated
        data_dict (dict): dictionary with all the equipment detail data
        lvl_lim (int): control how many steps a node can search downstream
        lvl_current (int): inner passing variables that should not be defined by user.
        pre_name (str): inner passing variables that should not be defined by user.

    Returns: None
    """
    # return None if cannot find node
    if type_id == 0: return

    data = data_dict[type_id]
    try:
        name = data.loc[ep_id,'name']
    except Exception:
        print('Can not find this equipment, type:',type_id, 'id:', ep_id, 'previous equipment:',pre_name)
        return
    lvl_current += 1

    # return None if current search level meets the level limit
    if lvl_lim != 0 and lvl_current > lvl_lim: return

    # retrun node name if node already exists
    if ep_map.has_node(name): return name

    # Assign node, find next or previous node based on equipment type
    if type_id == 1: #Crusher
        # Get attributes, create node 
        capacity = data.loc[ep_id,'capacity']
        rate = data.loc[ep_id,'rate']
        ep_map.add_node(name, capacity=capacity, rate=rate, ep_type=type_id)

        # find next node and connect
        next_ep_id = data.loc[ep_id,'next_id']
        next_type_id = data.loc[ep_id,'next_type_id']
        next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map,data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if next_ep_name is not None: ep_map.add_edge(name, next_ep_name, output_pct=1)
        return name

    if type_id == 2: #Screen
        # data of screen distination and screen split percentage
        data_sc_dst = data_dict[21]
        data_sc_pct = data_dict[22]

        capacity = data.loc[ep_id,'capacity']
        rate = data.loc[ep_id,'rate']
        sc_group_id = data.loc[ep_id,'sc_group_id']
        ep_map.add_node(name, capacity=capacity, rate=rate, ep_type=type_id, sc_group_id=sc_group_id)
        
        total_splt_pct = 0
        num_conn = data_sc_dst[data_sc_dst.sc_group_id==sc_group_id].index.size

        # search screen destinations
        for i in range(1,num_conn+1):
            cond = (data_sc_dst.sc_group_id==sc_group_id)&(data_sc_dst.splt_id==i)
            next_ep_id = data_sc_dst.loc[cond, 'next_id'].item()
            next_type_id = data_sc_dst.loc[cond, 'next_type_id'].item()
            next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
            
            # create edge with all attributes if next nodes exist
            if next_ep_name is not None: 
                # get screen split pct dictionary of all ore type, {ore type: split pct}
                ore_type_split_dict = {}
                for ore_type_id in range(1,ore_type_num+1):
                    cond = (data_sc_pct.sc_group_id==sc_group_id)&(data_sc_pct.splt_id==i)&(data_sc_pct.ore_type_id==ore_type_id)
                    splt_pct = data_sc_pct.loc[cond, 'pct']
                    in_loop = 0 if data_sc_pct.loc[cond, 'in_loop'].empty else data_sc_pct.loc[cond, 'in_loop'].item()
                    ore_type_split_dict[ore_type_id] = 0 if splt_pct.empty else splt_pct.item()
                    total_splt_pct += ore_type_split_dict[ore_type_id]
                ep_map.add_edge(name, next_ep_name, output_pct=ore_type_split_dict, in_loop=in_loop)

        if total_splt_pct - ore_type_num > 0.0001 and total_splt_pct - ore_type_num < -0.0001:
            print('check split percentage of screen: ', name)
        return name

    if type_id == 3: #Conveyor
        length = data.loc[ep_id,'length']
        speed = data.loc[ep_id,'speed']
        capacity = data.loc[ep_id,'capacity']
        rate = data.loc[ep_id,'rate']
        ep_map.add_node(name, capacity=capacity, speed=speed, length=length, rate=rate, ep_type=type_id)

        next_ep_id = data.loc[ep_id,'next_id']
        next_type_id = data.loc[ep_id,'next_type_id']
        next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map,data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if next_ep_name is not None: ep_map.add_edge(name, next_ep_name, output_pct=1)
        return name

    if type_id == 4: #Bin
        capacity = data.loc[ep_id,'capacity']
        rate = data.loc[ep_id,'rate']
        ep_map.add_node(name, capacity=capacity, rate=rate, ep_type=type_id)

        next_ep_id = data.loc[ep_id,'next_id']
        next_type_id = data.loc[ep_id,'next_type_id']
        next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if next_ep_name is not None: ep_map.add_edge(name, next_ep_name, output_pct=1)
        return name

    if type_id == 5: # stockpile group
        ep_map.add_node(name, ep_type=type_id, ore_type_num=ore_type_num)
        return name

    if type_id == 6: #Tripper
        ep_map.add_node(name, ep_type=type_id)
        num_conn = data.loc[ep_id,'connected_num']
        next_type_id = data.loc[ep_id,'next_type_id']
        # search all valid connections
        for i in range(1,num_conn+1):
            next_ep_id = data.loc[ep_id,'next_id_'+str(i)]
            next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
            if next_ep_name is not None: ep_map.add_edge(name, next_ep_name)
        # evenly distribute output_pct to all successors
        for subnode in ep_map[name]:
            ep_map[name][subnode]['output_pct'] = 1/ep_map.out_degree(name)
        return name

    if type_id == 7: #Apron feeder
        rate = data.loc[ep_id,'rate'] 
        ep_map.add_node(name, rate=rate, ep_type=type_id)
        # Create connection between apron feeder and the previous bin
        pre_bin_id = data.loc[ep_id,'pre_bin_id']
        pre_bin_name = find_neighbour_node(pre_bin_id, 4, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if pre_bin_name is not None: 
            ep_map.add_edge(pre_bin_name, name, output_pct=1)
            # if previous bin have more than 1 output, distribute the percentage based on the proportion of total output rate
            '''Not very good at handling the rates when it is list, it only pick the first rate in the list to calculate the output_pct'''
            if ep_map.out_degree(pre_bin_name) > 1:
                total_output_rate = sum(parse_exp(ep_map.nodes[x]['rate'], return_type=1) for x in ep_map[pre_bin_name])
                ep_map.nodes[pre_bin_name]['rate'] = total_output_rate
                for subnode in ep_map[pre_bin_name]:
                    ep_map[pre_bin_name][subnode]['output_pct']=parse_exp(ep_map.nodes[subnode]['rate'], return_type=1)/total_output_rate

        # Create connection between apron feeder and next equipment
        next_ep_id = data.loc[ep_id,'next_id']
        next_type_id = data.loc[ep_id,'next_type_id']
        next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if next_ep_name is not None: ep_map.add_edge(name, next_ep_name, output_pct=1)
        return name

    if type_id == 8: #Pct spliter
        ep_map.add_node(name, ep_type=type_id, ore_type_num=ore_type_num)

        # search all valid connections
        num_ep = []
        for i in range(1,6):
            next_type_id = data.loc[ep_id,'next_type_id_'+str(i)]
            next_ep_id = data.loc[ep_id,'next_id_'+str(i)]
            if next_ep_id == 0: continue
            num_ep.append(i)
        if len(num_ep) <= 0:
            print('The number of connected percentage splitter ',name,' is incorrect.')
            return name
        # extract next equipment information on the right index
        for i in num_ep:
            next_type_id = data.loc[ep_id,'next_type_id_'+str(i)]
            next_ep_id = data.loc[ep_id,'next_id_'+str(i)]
            next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
            splt_pct = parse_exp(data.loc[ep_id,'pct_'+str(i)])
            if next_ep_name is not None: ep_map.add_edge(name, next_ep_name, output_pct=splt_pct)
        return name

    if type_id == 9: #Priority feeder
        upper_pct = data.loc[ep_id,'upper_pct']
        lower_pct = data.loc[ep_id,'lower_pct']
        rate = data.loc[ep_id,'rate']
        ep_map.add_node(name, rate=rate, upper_pct=upper_pct, lower_pct=lower_pct, ep_type=type_id)

        # connect previous bin
        pre_bin_id = data.loc[ep_id,'pre_bin_id']
        pre_bin_name = find_neighbour_node(pre_bin_id, 4, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
        if pre_bin_name is not None: 
            ep_map.add_edge(pre_bin_name, name)
             # if previous bin have more than 1 output, evenly distribute the percentage
            if ep_map.out_degree(pre_bin_name) > 1:
                total_output_rate = sum(parse_exp(ep_map.nodes[x]['rate']) for x in ep_map[pre_bin_name])
                ep_map.nodes[pre_bin_name]['rate'] = total_output_rate
                for subnode in ep_map[pre_bin_name]:
                    ep_map[pre_bin_name][subnode]['output_pct']=parse_exp(ep_map.nodes[subnode]['rate'])/total_output_rate

        # connnect next equipment in all 3 modes
        for i in range(0,3):
            if i == 0: n = ''
            else: n = '.' + str(i)
            next_ep_id = data.loc[ep_id,'next_id'+n]
            next_type_id = data.loc[ep_id,'next_type_id'+n]
            next_ep_name = find_neighbour_node(next_ep_id,next_type_id, ep_map, data_dict,lvl_lim=lvl_lim, lvl_current=lvl_current, pre_name=name, ore_type_num=ore_type_num)
            if next_ep_name is not None: 
                mode = i + 1
                output_pct = 1 if mode == 1 else 0
                ep_map.add_edge(name, next_ep_name, mode=mode, output_pct=output_pct)
        # update output_pct of all the out edges
        # for subnode in ep_map[name]:
        #     ep_map[name][subnode]['output_pct']=1/ep_map.out_degree(name)
        return name

def parse_exp(rate, return_type=0):
    """roughly convert rate from expressions string to a number or a list of number
    Cautions: this function cannot deal with all the expressions.

    Args:
        exp (str): string expression
        return_type (int, optional, default=0): return a single number or the first number in the list if return_type=1, otherwise return the whole result

    Returns: 
        float type rate if there is, otherwise None
    """  
    if type(rate) != str: return rate
    rate_list = [float(rate) for rate in re.split(r'\*\(A_OreType==[1-9]\)\+?|\*\(.*E_EpAvailability\(.*\)\)|\s*\*\s*\(A_OreType.*?\)\s*\+?\s*|\*\(V_BinStatus.*[<=>]+.*?\)|\(|\)', rate) if rate !=""]
    if len(rate_list) == 0:
        return None
    elif len(rate_list) == 1 or return_type == 1:
        return rate_list[0]
    else:
        return rate_list

def find_constraint(ep_map, pct_split):  
    """find the constraint equipment in ep_map. Whether an equipment is a constraint depends on its expected throughput and rate. The one with the greatest throughput/rate will be the constraint.
        However, rate can not be proper loaded if it is written in expression

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        pct_split (dict): a dictionary with equipment names as keys and mass split percentage as value.

    Returns:
        constrained_list (list): a list of the constrained equipment node,
        rate_dict (dict): {node: rate}, 
        hr_dict (dict): {node: hr}, where hr = throughput/rate. hr = -1 if rate = 0
    """
    rate_dict = {}
    hr_dict = {}
    constrained_list = []

    for node in pct_split:
        if node in ep_map:
            if 'rate' in ep_map.nodes[node]:
                rate = parse_exp(ep_map.nodes[node]['rate'])
                if type(rate) == list:
                    rate = rate[0]
                throughput = pct_split[node]
                rate_dict[node] = rate
                if rate > 0:
                    hr_dict[node] = throughput / rate
                else:
                    # for equipment that doesn't have rates, assign -1
                    hr_dict[node] = -1

    hr_dict = {node: hr for node, hr in sorted(hr_dict.items(), key= lambda item: item[1], reverse=True)}
    constrained_value = hr_dict[max(hr_dict, key= lambda node: hr_dict[node])]
    constrained_list = [node for node in hr_dict if hr_dict[node] == constrained_value]
    
    return constrained_list, rate_dict, hr_dict

def find_loops(ep_map):
    """
    Purpose:
        find loops in the equipment map.

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
    Returns: 
        unique_ep_list (list): a list of all unique equipment in loops.
        loop_list (2D list): a list of list with equipment names in the loop if there are loops, otherwise return []. Each loop must be unique.
    """
    all_loops = list(nx.simple_cycles(ep_map))
    loop_list = []
    unique_ep_list = []
    for loop in all_loops:
        if len(loop_list) == 0: loop_list.append(loop)
        for i in range(len(loop_list)):
            next_loop = loop_list[i]
            if set(next_loop) == set(loop): break
            if i == len(loop_list) - 1: loop_list.append(next_loop)
        for ep in loop:
            if ep not in unique_ep_list:
                unique_ep_list.append(ep)
    
    return unique_ep_list, loop_list

def validate_split(pct_split, ep_map):
    """
    Purpose:
        make sure the total pct of all source nodes is equal to the total of all target nodes

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        pct_split (dict): a dictionary with equipment names as keys and mass split percentage as value.

    Returns: 
        None if the validation passes, otherwise raise error.
    """
    source_list,target_list,_ = get_special_nodes(ep_map)
    total_input = round(sum(pct_split[source] for source in source_list if source in pct_split),4)
    total_output = round(sum(pct_split[target] for target in target_list if target in pct_split),4)

    if total_input != total_output:
        print('The input and output are not balanced, \ninput:{}, output:{}'.format(total_input,total_output))
    else:
        print('split balanced, \ninput:{}, output:{}'.format(total_input,total_output))

    return

def calculate_split(ep_map, node_dict, end_node=[], ore_type_id=1):
    """
    Purpose:
        do static calculation of split percentages going through all downstream equipment nodes from the given source node.

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        node_dict (dict): equipment name and input pct pair dictionary that defines the input value to that node, for example {'Crusher_1':50, 'Crusher_2':50} 
                            represents 50 units inputs are placed to both Crusher_1 and Crusher_2.
        ore_type_id (int, optional, default=1): the ore type id used to get the right split percentage.
        
    Returns: 
        pct_split (dict): a dictionary with equipment names as keys and mass split percentage as value.
    """
    pct_split = {}

    if ore_type_id <= 0 or type(ore_type_id) != int:
        print('ore_type_num must be an integer greater than 0')
        return pct_split

    ep_in_loops, _ = find_loops(ep_map)
    for node in node_dict:
        pct_split = calculate_split_from_node(ep_map, node, input_pct=node_dict[node], pct_split=pct_split, ep_in_loops=ep_in_loops, ore_type_id=ore_type_id)
    
    return pct_split

def calculate_split_from_node(ep_map, node, end_node=[], input_pct=1, pct_split=None, ep_in_loops=None, ore_type_id=1, sc_visited=None, max_sc_visited=1):
    """
    Purpose:
        do static calculation of split percentages going through all downstream equipment nodes from the given source node,
        current function skip the calculation in looping edge when it arriaves at the same screen the second time, such as from screen to secondary crusher then back to screen.

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        node (str): the name of equipment node as the source to start the calculation.
        end_node (list, optional, default=[]): a list of nodes, where the recursive calculation will end if it reachs nodes in this list. Can be used when doing calculation by splitting a graph in to multiple parts.
        input_pct (float, optional, default=1): the percentage go through the source node, which can be used as pct if set it to 100, or any other values.
        pct_split (dict, optional, default=None): a dictionary with {node: split pct}
        ep_in_loops (list, optional, default=None): a name list of equipment that are in loops, each name is unique.
        ore_type_id (int, optional, default=1): the ore type id used to get the right split percentage
        sc_visited (dict, default=None): an inherent parameter used as a recoding list through all recursions, which should not be used by users

    Returns: 
        pct_split (dict): a dictionary with equipment names as keys and mass split percentage as value.
    """

    if ore_type_id <= 0 or type(ore_type_id) != int:
        print('ore_type_num must be an integer greater than 0')
        return pct_split

    if input_pct == 0:
        return pct_split

    # get split percentage (output_pct) based on ore type if the equipment is screen, otherwise just get output_pct.
    get_split_pct = lambda node,next_node: ep_map[node][next_node]['output_pct'][ore_type_id] if ep_map.nodes[node]['ep_type'] == 2 else ep_map[node][next_node]['output_pct']
    
    # initialize for the first call
    if pct_split == None: pct_split = {}
    if ep_in_loops == None: ep_in_loops, _ = find_loops(ep_map)
    if sc_visited == None: sc_visited = {}

    if node in pct_split:
        pct_split[node] = pct_split[node] + input_pct
    else:
        pct_split[node] = input_pct

    if node in end_node: return pct_split

    # start checking next equipment node based on current node type and conditions
    # visit the non looping edges if the screen is in loop, and its group has already been visited 'n' times
    
    if ep_map.nodes[node]['ep_type'] == 2:
        split_cond = max_sc_visited == 0 or \
                    (ep_map.nodes[node]['sc_group_id'] in sc_visited and \
                    sc_visited[ep_map.nodes[node]['sc_group_id']] >= max_sc_visited)
    else:
        split_cond = False
    
    if (ep_map.nodes[node]['ep_type'] == 2) and (node in ep_in_loops) and split_cond:
        # calculate the percentage to an exit that is not in a loop 
        non_loop_pct = sum(get_split_pct(node,next_node) for next_node in ep_map[node] if next_node not in ep_in_loops)
        
        for next_node in ep_map[node]:
            # skip if it is a looping edge
            if next_node in ep_in_loops: continue
            else:
                next_input_pct = get_split_pct(node,next_node)/non_loop_pct * input_pct
                # pass deep copy of sc_visited to the next recursion, otherwise different call will share the same visited list.
                calculate_split_from_node(ep_map, next_node, end_node=end_node, input_pct=next_input_pct, pct_split=pct_split, ep_in_loops=ep_in_loops, 
                                            ore_type_id=ore_type_id, sc_visited=copy.deepcopy(sc_visited), max_sc_visited=max_sc_visited
                                            )
    # visit all edges otherwise
    else:
        # assign new screen to sc_visited
        if ep_map.nodes[node]['ep_type'] == 2: 
            if node not in sc_visited:
                sc_visited[ep_map.nodes[node]['sc_group_id']] = 1 
            else: sc_visited[ep_map.nodes[node]['sc_group_id']] += 1

        for next_node in ep_map[node]:
            next_input_pct = get_split_pct(node,next_node) * input_pct
            if next_input_pct > 0:
                calculate_split_from_node(ep_map, next_node, end_node=end_node, input_pct=next_input_pct, pct_split=pct_split, ep_in_loops=ep_in_loops, 
                                        ore_type_id=ore_type_id, sc_visited=copy.deepcopy(sc_visited), max_sc_visited=max_sc_visited
                                        )
            else:
                continue
    
    return pct_split

def calculate_rates_from_node(ep_map, node, end_node=[], input_rate_dict=None, ep_in_loops=None, ore_type_id=1, sc_visited=None, max_sc_visited=1, input_rate=None, output_rate_dict=None):
    """
    This function is very similar to the calculate_split_from_node. It does static calculation on the input rate of each equipment, the input rate pass to the next equipment is
    based on min(current equipment rate, input rate of the current equipment) * split percentage to the next equipment

    Caution: the result depends on the equipment rate, however, the current code can not 100% support all the rates written in expression.

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        node (str): the name of equipment node as the source to start the calculation.
        end_node (list, optional, default=[]): a list of nodes, where the recursive calculation will end if it reachs nodes in this list. Can be used when doing calculation by splitting a graph in to multiple parts.
        input_rate_dict (dict, optional, default=None): a dictionary with {equipment: input rate}
        ep_in_loops (list, optional, default=None): a name list of equipment that are in loops, each name is unique.
        ore_type_id (int, optional, default=0): the ore type id used to get the right split percentage
        sc_visited (dict, default=None): an inherent parameter used as a recoding list through all recursions, which should not be used by users

    Returns: 
        input_rates (dict): a dictionary with equipment names as keys and its input rates as value.
    """

    if ore_type_id <= 0 or type(ore_type_id) != int:
        print('ore_type_num must be an integer greater than 0')
        return input_rate_dict

    # get split percentage (output_pct) based on ore type if the equipment is screen, otherwise just get output_pct.
    get_split_pct = lambda node,next_node: ep_map[node][next_node]['output_pct'][ore_type_id] if ep_map.nodes[node]['ep_type'] == 2 else ep_map[node][next_node]['output_pct']
    
    
    # if no rate, like tripper, give them super large rate
    if 'rate' not in ep_map.nodes[node]:
        ep_rate = 9999999
    # if it is expression, convert it to numeric
    elif type(ep_map.nodes[node]['rate']) == str:
        try:
            ep_rate = parse_exp(ep_map.nodes[node]['rate'])
        except Exception:
            print('error, cannot deal with ', node, ep_map.nodes[node]['rate'])
            return input_rate_dict

        # if rate is a list based on ore type
        if type(ep_rate) == list:
            if len(ep_rate) == 3:
                ep_rate = ep_rate[(ore_type_id-1)//3]
            elif len(ep_rate) == 9:
                ep_rate = ep_rate[ore_type_id-1]
            else:
                print('error, cannot deal with ', node, ep_map.nodes[node]['rate'], ep_rate)
    # if rate is 0 like the bin with apron feeder, get the total rate of the next nodes
    elif ep_map.nodes[node]['rate'] == 0:
        ep_rate = sum(ep_map.nodes[sub_node]['rate'] for sub_node in ep_map[node])
    else:
        ep_rate = ep_map.nodes[node]['rate']

    # initialize for the first call
    if input_rate_dict == None: input_rate_dict = {}
    if ep_in_loops == None: ep_in_loops, _ = find_loops(ep_map)
    if sc_visited == None: sc_visited = {}
    if input_rate == None: input_rate = ep_rate
    if output_rate_dict == None: output_rate_dict = {}

    # the input rate can be contributed by more than 1 equipment upstream
    if node in input_rate_dict:
        old_input_rate = input_rate_dict[node]
        new_input_rate = input_rate_dict[node] + input_rate
    else:
        old_input_rate = 0
        new_input_rate = input_rate
    input_rate_dict[node] = new_input_rate

    # the out rate to the next equipment should be the exceeding part, new_input_rate - old_input_rate, but it is also constrained by the output rate of equipment itself
    output_rate = min(new_input_rate, ep_rate) - old_input_rate

    # # skip the calculation if the output rate remains the same
    # if node in output_rate_dict and output_rate_dict[node] == output_rate: 
    #     return input_rate_dict
    # else:
    #     output_rate_dict[node] = output_rate

    if node in end_node: return input_rate_dict

    # start checking next equipment node based on current node type and conditions
    # visit the non looping edges if the screen is in loop, and its group has already been visited 'n' times
    
    if ep_map.nodes[node]['ep_type'] == 2:
        split_cond = max_sc_visited == 0 or \
                    (ep_map.nodes[node]['sc_group_id'] in sc_visited and \
                    sc_visited[ep_map.nodes[node]['sc_group_id']] >= max_sc_visited)
    else:
        split_cond = False
    
    if (ep_map.nodes[node]['ep_type'] == 2) and (node in ep_in_loops) and split_cond:
        # calculate the percentage to an exit that is not in a loop 
        non_loop_pct = sum(get_split_pct(node,next_node) for next_node in ep_map[node] if next_node not in ep_in_loops)
        
        for next_node in ep_map[node]:
            # skip if it is a looping edge
            if next_node in ep_in_loops: continue
            else:
                next_input_rate = get_split_pct(node,next_node)/non_loop_pct * output_rate
                # pass deep copy of sc_visited to the next recursion, otherwise different call will share the same visited list.
                calculate_rates_from_node(ep_map, next_node, end_node=end_node, input_rate=next_input_rate, input_rate_dict=input_rate_dict, ep_in_loops=ep_in_loops, 
                                        ore_type_id=ore_type_id, sc_visited=copy.deepcopy(sc_visited), max_sc_visited=max_sc_visited, output_rate_dict=output_rate_dict
                                        )
    # visit all edges otherwise
    else:
        # assign new screen to sc_visited
        if ep_map.nodes[node]['ep_type'] == 2: 
            if node not in sc_visited:
                sc_visited[ep_map.nodes[node]['sc_group_id']] = 1 
            else: sc_visited[ep_map.nodes[node]['sc_group_id']] += 1

        for next_node in ep_map[node]:
            next_input_rate = get_split_pct(node,next_node) * output_rate
            if next_input_rate > 0:
                # if next_node in ['Tripper_CV1231', 'CV1231', 'SC1301', 'CV1332', 'VF1301']: 
                # if next_node in ['CV1231']: 
                #     print("node {}, next_node {}, eprate {:.2f}, input {:.2f}, output {:.2f}, next_input_rate {:.2f}, stacked_input_rate {:.2f}".format(node, next_node, ep_rate, input_rate, output_rate, next_input_rate, input_rate_dict[node]))
                calculate_rates_from_node(ep_map, next_node, end_node=end_node, input_rate=next_input_rate, input_rate_dict=input_rate_dict, ep_in_loops=ep_in_loops, 
                                        ore_type_id=ore_type_id, sc_visited=copy.deepcopy(sc_visited), max_sc_visited=max_sc_visited, output_rate_dict=output_rate_dict
                                        )
            else:
                continue
    
    return input_rate_dict

def get_special_nodes(ep_map):
    """
    Purpose:
        find out all the source nodes (no input), target nodes (no output) and isolated nodes (no input and output)

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        
    Returns: 
        pct_split (dict): a dictionary with equipment names as keys and mass split percentage as value.
    """
    source_list=[]
    target_list=[]
    isolated_list=[]
    for node in ep_map.nodes:
        if ep_map.in_degree(node) == 0 and ep_map.out_degree(node) > 0:
            source_list.append(node)
        if ep_map.in_degree(node) > 0 and ep_map.out_degree(node) == 0:
            target_list.append(node)
        if ep_map.in_degree(node) == 0 and ep_map.out_degree(node) == 0:
            isolated_list.append(node)
    return source_list,target_list,isolated_list

def get_path_steps(ep_map, source, target):
    """
    Purpose:
        return the minimum number of steps from source node to target node, return infinity if path does not exist

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        source (str): name of the source node
        target (str): name of the target node
        
    Returns: 
        steps(int): return the minimum number of steps from source node to target node, return infinity if path does not exist
    """
    try:
        steps = nx.shortest_path_length(ep_map,source,target)
        return steps
    except nx.NetworkXNoPath as e:
        return math.inf

def get_pos(ep_map, h_dis=2, v_dis=2, start_node=None, end_node=None):
    """
    Purpose:
        Get pos dict with all nodes coordinates

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        v_dis (float), h_dis (float): vertical and horizontal distance between nodes.
        
    Returns: 
        pos (dict): a dictionary that contains nodes and their coordinates, equipment name as key and coordinates tuple as value, like 'Screen_1':(1,1)
    """
    pos = {}
    _x_max = {}
    source_list,_,_ = get_special_nodes(ep_map)

    if start_node == None:
        for source in source_list:
            positioning_nodes(ep_map, source, end_node=[], pos=pos, h_dis=h_dis, v_dis=v_dis, _max_x=_x_max)

        # place all isolated nodes separately
        x = 0
        for node in ep_map.nodes:
            if node not in pos:
                pos[node] = (x,v_dis)
                x += h_dis
    else:
        if start_node in ep_map:
            positioning_nodes(ep_map, start_node, end_node=[], pos=pos, h_dis=h_dis, v_dis=v_dis, _max_x=_x_max)
        else:
            print('start_node is not in ep_map')

    return pos

def positioning_nodes(ep_map, node, end_node=[], pos=None, x=0, y=0, v_dis=2, h_dis=2, _max_x=None):
    """
    Purpose:
        recursively give each node a proper coordinates (x,y) for visualization

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        node (str): the name of equipment node as the source to start the positioning.
        pos (dict): the dictionary that contains nodes and their coordinates, equipment name as key and coordinates tuple as value, like 'Screen_1':(1,1)
        x (float), y (float): the coordinates of the start node.
        v_dis (float), h_dis (float): vertical and horizontal distance between nodes.
        _max_x: inner passing variable that contains the maximum x of each y.
        
    Returns: 
        pos (dict): the dictionary that contains nodes and their coordinates, equipment name as key and coordinates tuple as value, like 'Screen_1':(1,1)
    """
    if pos == None: pos = {}
    if _max_x == None: _max_x = {}

    if node in pos: 
        return pos[node][0], x
    else:
        y = y
        if y in _max_x: x = _max_x[y]+h_dis

        pos[node] = (x,y)
        _max_x[y] = x

        if node in end_node: return 
        else:
            # recursively positioning the next node
            for next_node in ep_map.adj[node]:
                positioning_nodes(ep_map, next_node, pos=pos, x=x, y=y-v_dis, v_dis=v_dis, h_dis=h_dis, _max_x=_max_x)
            return pos, x

def draw_map(ep_map, pos, pct_split=None):
    """
    Purpose:
        Using matplotlib to visualize the equipment directed graph (ep_map) based on the position dictionary (pos)

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        pos (dict): a dictionary that contains nodes and their coordinates, equipment name as key and coordinates tuple as value, like 'Screen_1':(1,1)
        pct_split (dict, default=None): if use, the split percentage will also be labeled in visualization.
                                        pct_split is a dictionary with equipment names as keys and mass split percentage as value, 
                                        calculated by using calculate_split() or calculate_split_from_node()

    Returns: 
        fig (matplotlib.figure.Figure): figure object that is the visualization of the graph.
        graph_map (networkx.DiGraph): the a deep copy of ep_map filtered out nodes not in pos and pct_split
    """
    
    # create node labels with name and the split pct
    if pct_split != None:
        if len(pct_split) == 0:
            print('Please confirm pct_split, it\'s not matching the nodes in pos')
            pct_label = None
        else:
            pct_label = {n:n+'\n'+str(round(pct,2)) for n,pct in pct_split.items() if n in pos}
    else:
        pct_label = None

    graph_map = copy.deepcopy(ep_map)
    node_list = list(graph_map.nodes)
    for node in node_list:
        if pct_split != None:
            if (node not in pos) or (node not in pct_split):
                graph_map.remove_node(node)
        else:
            if node not in pos:
                graph_map.remove_node(node)
            
    # give different colors based on node types (source, target, isolated)
    source_list,target_list,isolated_list = get_special_nodes(ep_map)
    node_color_list = []
    for node in graph_map.nodes:
        if node in source_list:
            node_color_list.append('green')
        elif node in target_list:
            node_color_list.append('red')
        elif node in isolated_list:
            node_color_list.append('grey')
        else:
            node_color_list.append('pink')

    # give different shapes based on node equipment types
    # data_dict {1:data_cs, 2:data_sc, 3:data_cv, 4:data_bn, 5:data_stock, 6:data_trp, 7:data_apf, 8:data_splt, 9:data_prif, 21: data_sc_dst, 22: data_sc_pct}
    shape_dict = {1:'v', 2:'d', 3:'o', 4:'s', 5:'^', 6:'o', 7:'o', 8:'o', 9:'8'}
    fig = plt.figure(figsize=(30,30)) 
    
    for ep_type in shape_dict:
        selected_nodes = [node for node in graph_map.nodes if graph_map.nodes[node]['ep_type'] == ep_type]
        selected_nodes_index = [list(graph_map.nodes).index(node) for node in selected_nodes]
        selected_color = [node_color_list[index] for index in selected_nodes_index]
        nx.draw_networkx_nodes(graph_map, pos, node_size=800, 
                                node_color=selected_color, 
                                nodelist=selected_nodes, 
                                edgecolors=None, node_shape=shape_dict[ep_type]
                                )
    
    nx.draw_networkx_labels(graph_map, pos, labels=pct_label)
    nx.draw_networkx_edges(graph_map,pos, arrowstyle='- >', arrowsize=15, min_target_margin=15, alpha=0.5)
    # nx.draw_networkx_edge_labels(ep_map,pos,edge_labels=edge_label)
    plt.show()

    return fig, graph_map

def draw_map_new(ep_map, pos, figsize=(30,30), margin=0, labels={}):
    """
    Purpose:
        Using matplotlib to visualize the equipment directed graph (ep_map) based on the position dictionary (pos)
    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        pos (dict): a dictionary that contains nodes and their coordinates, equipment name as key and coordinates tuple as value, like 'Screen_1':(1,1)
        labels (dict, default={}): dictionary should be like {label name (str): label dictionary (dict)}, label dictionary should be like {node (str): label value}.
                                    if use, the label value will be labeled in visualization as label name: label value. 
                                    pct_split is a dictionary with equipment names as keys and mass split percentage as value, 
                                    calculated by using calculate_split() or calculate_split_from_node()

    Returns: 
        fig (matplotlib.figure.Figure): figure object that is the visualization of the graph.
        ax (matplotlib.axes.Axes): matplotlib Axes object
        graph_map (networkx.DiGraph): the a deep copy of ep_map filtered out nodes not in pos and pct_split
    """
    
    # create node labels with name and the label values
    final_label_dict = {node:node for node in pos}
    for label in labels:
        try:
            label_name = str(label)
        except ValueError:
            continue

        new_label_dict = labels[label]
        if new_label_dict != None:
            if len(new_label_dict) == 0:
                print(f'Please confirm label {label_name}, which has nothing in the details')
                continue
            else:
                for node in final_label_dict:
                    if node in new_label_dict:
                        try:
                            label_value = str(round(float(new_label_dict[node]),2))
                        except ValueError:
                            continue
                        else:
                            final_label_dict[node] += '\n' + label_name + ':' + label_value
                    else:
                        continue
        else:
            continue

    graph_map = copy.deepcopy(ep_map)
    node_list = list(graph_map.nodes)
    for node in node_list:
        if (node not in pos):
            graph_map.remove_node(node)

    # give different colors based on node types (source, target, isolated)
    source_list,target_list,isolated_list = get_special_nodes(ep_map)
    node_color_list = []
    for node in graph_map.nodes:
        if node in source_list:
            node_color_list.append('green')
        elif node in target_list:
            node_color_list.append('red')
        elif node in isolated_list:
            node_color_list.append('grey')
        else:
            node_color_list.append('pink')

    # give different shapes based on node equipment types
    # data_dict {1:data_cs, 2:data_sc, 3:data_cv, 4:data_bn, 5:data_stock, 6:data_trp, 7:data_apf, 8:data_splt, 9:data_prif, 21: data_sc_dst, 22: data_sc_pct}
    shape_dict = {1:'v', 2:'d', 3:'o', 4:'s', 5:'^', 6:'o', 7:'o', 8:'o', 9:'8'}
    fig, ax = plt.subplots(figsize=figsize) 
    
    for ep_type in shape_dict:
        selected_nodes = [node for node in graph_map.nodes if graph_map.nodes[node]['ep_type'] == ep_type]
        selected_nodes_index = [list(graph_map.nodes).index(node) for node in selected_nodes]
        selected_color = [node_color_list[index] for index in selected_nodes_index]
        nx.draw_networkx_nodes(graph_map, pos, node_size=800, 
                                ax=ax,
                                node_color=selected_color, 
                                nodelist=selected_nodes, 
                                edgecolors=None, node_shape=shape_dict[ep_type]
                                )
    
    nx.draw_networkx_labels(graph_map, pos, ax=ax, labels=final_label_dict)
    nx.draw_networkx_edges(graph_map, pos, ax=ax, arrowstyle='- >', arrowsize=15, min_target_margin=15, alpha=0.5)
    # nx.draw_networkx_edge_labels(ep_map,pos,edge_labels=edge_label)
    ax.margins(margin)

    plt.show()

    return fig, ax, graph_map

def simplified_graph(ep_map, pct_split=None, print_merged_process=False):
    """
    keep searching the whole graph and merging all the parallel modules (bins, screens, trippery) into a equipment group, until there are no more nodes to merge.

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.
        pct_split (dict, optional, default=None): if use, the split percentage will be also calculated into merged nodes. pct_split is a dictionary with equipment names as keys and mass split percentage as value, calculated by using calculate_split() or calculate_split_from_node()
        print_merged_process (boolean, default=False): the function will print the merge process if it is set True

    Returns:
        simple_ep_map (networkx.DiGraph): a directed graph like the input ep_map with merged equipment nodes
        merged_pct_split (dict): if pct_split is passed to this function, the new pct_split with merged nodes will also be returned.

    """ 

    simple_ep_map_before = nx.DiGraph()
    simple_ep_map_after = copy.deepcopy(ep_map)
    merged_pct_split = pct_split
    while nx.is_isomorphic(simple_ep_map_before,simple_ep_map_after) == False:
        merged_ep_map, merged_pct_split = merge_equip(simple_ep_map_after, pct_split=merged_pct_split, print_merged_process=print_merged_process)
        simple_ep_map_before,simple_ep_map_after = simple_ep_map_after, merged_ep_map
    return simple_ep_map_after, merged_pct_split
    
def merge_equip(ep_map, pct_split=None, print_merged_process=False):
    """
    for once, search the whole graph and merged all the parallel modules (bins, screens, trippery) into a equipment group if they all have a shared selected source, and their names are similar (only the last 2 digits are different, such as VF1301 and VF1303)

    Args:
        ep_map (networkx.DiGraph): the directed graph with all the equipemnt connections and details.

        pct_split (dict, default=None): if use, the split percentage will be also calculated into merged nodes.
                                        pct_split is a dictionary with equipment names as keys and mass split percentage as value, 
                                        calculated by using calculate_split() or calculate_split_from_node()
        print_merged_process (boolean, default=False): the function will print the merge process if it is set True

    Returns: 
        simple_ep_map (networkx.DiGraph): a directed graph like the input ep_map with merged equipment nodes
        merged_pct_split (dict): if pct_split is passed to this function, the new pct_split with merged nodes will also be returned.
    """
    
    simple_ep_map = copy.deepcopy(ep_map)
    merge_node_dict={}
    # only starts if the node has multiple out edges and equipment type is bin (drained by mulitple priority feeders), tripper (split into multiple similar equipment) or screens (after previous merge)
    for node in simple_ep_map.nodes:
        if (simple_ep_map.out_degree(node) >= 2) and (simple_ep_map.nodes[node]['ep_type'] in [2,4,6,8,9]):
            sub_node_list = []
            for sub_node in simple_ep_map[node]:
                # merge crushers, screens, bins and priority feeders that have single flow in
                if (simple_ep_map.nodes[sub_node]['ep_type'] in [1,2,4,8,9]):
                    sub_node_list.append(sub_node)
            if len(sub_node_list) >= 2:
                merge_node_dict[node] = sub_node_list

    # go through merge_node_dict and merge all the nodes
    for source in merge_node_dict:
        if print_merged_process: print('Groupping starts, source:', source)
        merge_list = merge_node_dict[source]
        ep_group_list = []
        while merge_list:
            # pick the first node and compare with the rest
            first_node = merge_list.pop(0)
            ep_group = [first_node]
            merge_list_copy = copy.deepcopy(merge_list)
            for other_node in merge_list_copy:
                # check 1.if same name except for the last 2 digits, 2.same equipment types, 3.not predecessor or successor to each other.
                cond = (first_node[:-2] == other_node[:-2]) and \
                        (simple_ep_map.nodes[first_node]['ep_type'] == simple_ep_map.nodes[other_node]['ep_type']) and \
                        (first_node not in simple_ep_map.predecessors(other_node)) and \
                        (first_node not in simple_ep_map.successors(other_node))
                # if so, put them in the same ep_group
                if cond:
                    ep_group.append(other_node)
                    merge_list.remove(other_node)
            ep_group_list.append(ep_group)
        if print_merged_process: print(source,'groupping ends, group list:', ep_group_list)
        
        # keep processing if there are actually nodes to be merged
        try:
            if simple_ep_map.has_node(source) and len(ep_group_list) < simple_ep_map.out_degree(source):
                if print_merged_process: print('Merging starts, source:',source,'grouping list:',ep_group_list)
                for ep_group in ep_group_list:
                    # merge equipment names and destinations if there is an equipment group
                    if len(ep_group) > 1:
                        # to create the name of the merged node, it picks the equip with the minimum last 2 digits as the first and the maximum as the last. 
                        max_num = max([int(ep[-2:]) for ep in ep_group])
                        min_num = min([int(ep[-2:]) for ep in ep_group])
                        
                        merged_node = ep_group[0][:-2] + f'{min_num:02d}' + '-' + f'{max_num:02d}'
                        # merged_node = ep_group[0][:-2] + '{:02d}'.format(min_num) + '-' + '{:02d}'.format(max_num)

                        merged_node_attribute = {}
                        if 'ep_type' in simple_ep_map.nodes[ep_group[0]]:
                            merged_node_attribute['ep_type'] = simple_ep_map.nodes[ep_group[0]]['ep_type']
                        if 'rate' in simple_ep_map.nodes[ep_group[0]]:
                            merged_node_attribute['rate'] = '(' + str(simple_ep_map.nodes[ep_group[0]]['rate']) + ') * ' + str(len(ep_group))
                        if 'capacity' in simple_ep_map.nodes[ep_group[0]]:
                            merged_node_attribute['capacity'] = len(ep_group) * simple_ep_map.nodes[ep_group[0]]['capacity']
                        if 'sc_group_id' in simple_ep_map.nodes[ep_group[0]]:
                            merged_node_attribute['sc_group_id'] = simple_ep_map.nodes[ep_group[0]]['sc_group_id']
                        merged_node_attribute['ep_group'] = True
                        merged_node_attribute['ep_list'] = ep_group
                        simple_ep_map.add_nodes_from([(merged_node, merged_node_attribute)])
                        if print_merged_process: print('Merging ends, create merged node',merged_node,'from',ep_group)
                        if pct_split != None:
                            if set(ep_group).issubset(set(pct_split)):
                                merged_pct = sum(pct_split[ep] for ep in ep_group)
                                if round(merged_pct,4) != round(pct_split[ep_group[0]]*len(ep_group),4):
                                    print(f'Please check the split percentage among {ep_group}, the percentage is not evenly distributed.{merged_pct:.2f} to {pct_split[ep_group[0]]*len(ep_group):.2f}')
                                    for ep in ep_group:
                                        print(type(pct_split[ep]), pct_split[ep])
                                pct_split[merged_node] = merged_pct
                                if print_merged_process: print('Total split pct in',merged_node,'is',merged_pct)

                        # connect the new merged node to the single source and all the destinations
                        # split pct will not be merged, given the situation can be too complicated. 
                        # For example, 3 screens connected to 3 bins separately needs to be treated differently to 3 screens all connected to 3 bins.
                        for ep in ep_group:
                            # 1.connect the source nodes (predecessors) to the merged node
                            simple_ep_map.add_edges_from([(source_node, merged_node) for source_node in simple_ep_map.predecessors(ep)])
                            # 2.connect the merged node to all target nodes (successors) of nodes that merged.
                            simple_ep_map.add_edges_from([(merged_node, target_node) for target_node in simple_ep_map.successors(ep)])
                            # 3.remove all the nodes that merged.
                            simple_ep_map.remove_node(ep)  

        except Exception:
            print('error merging from source')
            print(source)
            print(simple_ep_map.out_degree(source))
            print(simple_ep_map[source]) 
                   

    return simple_ep_map, pct_split
