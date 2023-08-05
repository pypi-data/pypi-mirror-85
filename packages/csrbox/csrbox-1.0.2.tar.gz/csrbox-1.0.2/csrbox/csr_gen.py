import logging
import re
import sys
import os
import csrbox
import csrbox.utils as utils
from csrbox.constants import *
import csrbox.csrgrp_check as csrgrp_check
import datetime
import textwrap

version = csrbox.__version__
logger = logging.getLogger(__name__)

def csr_gen (isa_file, grp_file, work_dir, logging=False):
    '''
        Top level function which validates the sanity of the grouping yaml 
        followed by calls to subfunctions which generated the corresponding 
        bluespec code. This function further assumes that the riscv-config
        isa yaml provided is the validated/normalized version.

        We also update the the size node for the csrs in the attributes YAML
        file based on the csrs that have been instantiated in the riscv-config
        YAML

        :param isa_file: path to the **validated** riscv-config ISA yaml file
        :param grp_file: path to the csr grouping YAML file.
        :param work_dir: path to the directory where the bluespec files should be generated

        :type isa_file: str
        :type grp_file: str
        :type work_dir: str
    '''
    
    isa_yaml = utils.load_yaml(isa_file)
    grp_yaml = utils.load_yaml(grp_file)
    
    csrgrp_check.csrgrp_check(isa_yaml, grp_yaml, logging)
    attr_yaml = csrgrp_check.calculate_size(isa_yaml)
    csr_define(isa_yaml , work_dir , 'csrbox.defines', logging)
    csr_decoder(isa_yaml, work_dir , 'csrbox_decoder.bsv', logging)
    csr_types(isa_yaml  , work_dir , 'csr_types.bsv', logging)
    groups_gen(isa_yaml, grp_yaml, attr_yaml, work_dir, logging)

def csr_types(isa_yaml, work_dir,  bsv, logging=False):
    '''
        Function to generate the types bluespec file which includes structures
        and functions that are used across the csrbox modules
        
        :param isa_yaml: the riscv-config isa YAML
        :param work_dir: path to the directory where the bluespec files should be generated
        :param bsv: name of the file to be created inside the work_dir

        :type isa_yaml: dict 
        :type work_dir: str
        :type bsv: str

    '''
    if logging: 
        logger.info('Creating File: ' + bsv)
    bsvfile = open(work_dir + bsv, 'w')
    pkg_name = bsv[:-4]
    
    xlen = str(isa_yaml['hart0']['supported_xlen'][0])

    bsvfile.write(license_header.format(version, str(datetime.datetime.now())))
    bsvfile.write('''
package {0} ;
    `include "csrbox.defines"

'''.format(pkg_name))
    bsvfile.write(csrreq_struct_temp.format(xlen))
    bsvfile.write(func_temp.format(xlen))
    bsvfile.write(end_package_temp)
    bsvfile.close()


def groups_gen(isa_yaml, grp_yaml, attr_yaml, work_dir, logging=False):
    '''
        Function which co-ordinates the generation of all the bluespec code for
        the individual groups/stations and the top level bluespec module.

        The function first creates a subset of the
        riscv-config isa yaml based on the csrs present in each group and calls
        various sub-functions to generate the corresponding bsv file of the
        individual groups/station.

        Once the station files are generated the csr_top is called which is used
        to generate the top module instantiating and connecting all the
        individual groups/stations.

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type work_dir: str
    '''
    rvxlen = 'rv' + str(max(isa_yaml['hart0']['supported_xlen']))
    xlen = str(max(isa_yaml['hart0']['supported_xlen']))

    station_isa = {}
    csr_isa = {}

    not_acc = []
    max_len = len(grp_yaml)

    for grp, elems in grp_yaml.items():
        if 'grp'+str(max_len) == grp:
            last = True
        else:
            last = False
        for node in isa_yaml['hart0']:
            if isinstance(isa_yaml['hart0'][node], dict):
                if 'description' in isa_yaml['hart0'][node]:
                    csr_name = node
                    name_str = str(csr_name)
                    if isa_yaml['hart0'][csr_name][rvxlen]['accessible'] == True:
                      if csr_name.upper() in elems:
                          station_isa[csr_name] = isa_yaml['hart0'][node]
                          csr_isa[csr_name] = isa_yaml['hart0'][node]
                    else:
                       not_acc.append(name_str)

        filename = 'csrbox_' + grp + '.bsv'
        bsvstr = ''
        bsvfile = open(work_dir+filename, 'w')
        if logging:
            logger.info('Writing file: ' + filename)
        pkg_name = filename[:-4]
        bsvstr += str(license_header.format(version, str(datetime.datetime.now())))
        bsvstr += (package_temp.format(pkg_name))
        bsvstr = station_interface(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr = station_module(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr = station_regs(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr = station_modbody(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr = station_req(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr = station_methods(station_isa, grp_yaml, attr_yaml, rvxlen,
                pkg_name, last, bsvstr, logging)
        bsvstr += (end_module_temp)
        bsvstr +=(end_package_temp)
        bsvfile.write(bsvstr)
        station_isa.clear()   
    bsvstr = csr_top(csr_isa, grp_yaml, attr_yaml, rvxlen,
             'csrbox', logging)
    filename = 'csrbox.bsv'
    bsvfile = open(work_dir + filename, 'w')
    bsvfile.write(bsvstr)

def csr_decoder(isa_yaml, work_dir, bsv, logging=False):

    ''' 
        Function to generate the bluespec decoder file indicating if the access
        to the CSR if valid or not
        :param isa_yaml: the riscv-config isa YAML
        :param work_dir: path to the directory where the bluespec files should be generated
        :param bsv: name of the file to be created inside the work_dir

        :type isa_yaml: dict 
        :type work_dir: str
        :type bsv: str
    '''

    rvxlen = 'rv' + str(isa_yaml['hart0']['supported_xlen'][0])

    definefile = open(work_dir + bsv, 'w')
    definefile.write(license_header.format(version, str(datetime.datetime.now())))
    definefile.write("////////////////CSR DECODER////////////////")
    pkg_name = bsv[:-4]
    definefile.write(package_temp.format(pkg_name))
    definefile.write(func_decoder)

    for node in isa_yaml['hart0']:
        if isinstance(isa_yaml['hart0'][node], dict):
            if 'address' in isa_yaml['hart0'][node] and ( isa_yaml['hart0'][node][rvxlen]['accessible'] == True) :
                csr_name = node
                definefile.write(       case_address_temp.format(csr_name.upper()))
    definefile.write('\n           endcase')
    definefile.write('\n     return valid;')
    definefile.write('\n     endfunction')

    definefile.write(end_package_temp)
    definefile.close()

def csr_define(isa_yaml, work_dir, bsv, logging=False):
    '''
        Function which generates the defines file which captues the macro
        encodings used across the csrbox bsv modules

        :param isa_yaml: the riscv-config isa YAML
        :param work_dir: path to the directory where the bluespec files should be generated
        :param bsv: name of the file to be created inside the work_dir

        :type isa_yaml: dict 
        :type work_dir: str
        :type bsv: str
    '''

    if logging:
        logger.info('Creating Defines file: ' + bsv)
    rvxlen = 'rv' + str(isa_yaml['hart0']['supported_xlen'][0])
    definefile = open(work_dir + bsv, 'w')
    definefile.write(license_header.format(version, str(datetime.datetime.now())))
    definefile.write("////////////////CSR LIST////////////////")

    for node in isa_yaml['hart0']:
        if isinstance(isa_yaml['hart0'][node], dict):
            if 'address' in isa_yaml['hart0'][node] and ( isa_yaml['hart0'][node][rvxlen]['accessible'] == True) :
                csr_name = node
                if logging:
                 logger.debug('Processing CSR: ' + str(csr_name.upper()))
                
                csr_address = format(isa_yaml['hart0'][csr_name]['address'],'x')

                if logging:
                 logger.debug('|-- address: ' + str(csr_address))
                 
                definefile.write(address_temp.format(csr_name.upper(),csr_address))

    definefile.close()


def create_concat_vector(mylist, xlen):
    '''
    Function to return a bsv-string for a csr which is the concetation of the
    all its subfields and gaps replaced with zeros'

    :param mylist: A list of 3 tuple entries. Each entry has the following
    information per subfield [msb of subfield, width of the subfield, name of
    the subfield]

    :return: string with concatenation of all the sub-fields.
  '''
    concat_length = 0
    newlist = sorted(mylist, key=lambda x: x[0])[::-1]
    cv = ' '
    last_lsb = xlen - 1
    while len(newlist) != 0:
        msb, width, name, type_reg = newlist[0]
        newlist.pop(0)
        if msb != last_lsb:
            cv += readonly_temp.format(last_lsb - msb) + ','
            concat_length += 1
        if 'ro_variable' in type_reg and (name != 'mstatus_sd'):
            cv += 'readOnlyReg(rg_' + str(name) + ' ),'
        else:
            cv += 'rg_' + str(name) + ' ,'
        concat_length += 1
        last_lsb = msb - width

    return concat_length, cv[:-1]


def get_reset_val(value, width, lsb, xlen):
    ''' 
    Function to extract 'width' number of bits starting at the 'lsb' position of
    the value. Note here that the python indexes the binary string from the let
    while the lsb defines the position from the right. Hence the need for this
    function

    :param value: the integer value from which bits need to be extracted.
    :param width: size of extraction
    :param lsb:   starting position of extraction

    :return: returns the reset value in decimal form
  '''
    b = '{:0' + xlen + 'b}'
    # convert number into binary first
    binary = b.format(value)

    # remember python indexes from left to right
    end = len(binary) - lsb - 1
    start = end - width + 1
    kBitSubStr = binary[start:end + 1]

    # convert extracted sub-string into decimal again
    return int(kBitSubStr, 2)


def derive_warl_func(csr_name, width, warl_str):
    '''
        Function to convert the warl strings in the riscv-config YAML to
        corresponding bluespec code.

        The function first splits the warl string into the condition and the
        legalizing strings. A regular expression is then applied to both strings
        separately to extract parameters and create bluespec code.


        :param csr_name: string indicating the name of the csr
        :param width: indicates the max size of the csr
        :param warl_str: containts the warl string from the riscv-config YAML string

        :type csr_name: str
        :type width: int
        :type warl_str: str
    '''

    warl_split = warl_str.split('->')
    regex_range = re.compile(csr_name + '\[(.*?)\]\s*(.*?)\s*\[(.*?)\]')
    regex_bitmask = re.compile(csr_name + '\[(.*?)\]\s*bitmask\s*\[(.*?)\]')
    regex_cond = re.compile('(.*?)\[(.*?)\]\s*(.*?)\s*\[(.*?)\]')
    bsv_str = ''
    condition_str = ''
    if len(warl_split) > 1:
        csr, indices, x, val = regex_cond.findall(warl_split[0])[0]
        if 'not' in x:
            eq = '=='
        else:
            eq = '!='
        condition_str += 'if ( rg_{0}[{1}] {2} {3} )\n'.format(csr, indices, eq, val)
        legal = warl_split[1]
    else:
        legal = warl_split[0]
        condition = ''


    range_vals = regex_range.findall(legal)
    bitmask_vals = regex_bitmask.findall(legal)
    full_warl = False
    if range_vals != []:
        bsv_str += 'if ( ('
        for x in range_vals:
            bsv_str += '('
            indices = x[0]
            if 'not' in x[1]:
                not_eq = True
            else:
                not_eq = False
            values = x[2].split(',')
            for v in values:
                if ':' in v:
                    base_bound = v.split(':')
                    if int(base_bound[0],16) == 0 and int(base_bound[1],16) == (2**int(width) -1):
                        full_warl = True
                    bsv_str += '( x[' + indices + '] >= ' +\
                    base_bound[0] + ' && x[' + indices + '] <= ' +base_bound[1] + ') ||'
                elif not_eq:
                    bsv_str += '( x[' + indices + '] != ' + v + ') ||'
                else:
                    bsv_str += '( x[' + indices + '] == ' + v + ') ||'
            bsv_str = bsv_str[:-2] + ') && '
        bsv_str = bsv_str[:-3] + ')'
        bsv_str = bsv_str.replace('0x', "'h") + ')\n'
        bsv_str += '                        r._write(x);'
    elif bitmask_vals != []:
        indices = bitmask_vals[0][0]
        mask_fixed = bitmask_vals[0][1].split(',')
        mask = mask_fixed[0][2:]
        fixedval = mask_fixed[1][3:]
        bsv_str = "r._write( (x & 'h" + mask + ") | (~'h" + mask + " & " + fixedval + ") );"
    if full_warl:
        bsv_str = 'r._write(x);'
    bsv_str = condition_str + bsv_str
    return bsv_str

def station_interface(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):

    '''
        Function to create the interface definition of individual
        groups/stations. 

        First Value methods are created for all csrs that are instantiated in
        the particular group. Next, custom action methods required for specific
        csrs of their subfields are created.

        Finally action methods to read shadow or dependent csrs is created.

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''
    xlen = int(rvxlen[2:])
    bsvstr += interface_temp.format(pkg_name)

    if logging:
        logger.info('Initiating interface generation for : ' + pkg_name)

    # define a value method for each csr.
    for csrname in isa_yaml:
        if attr_yaml[csrname]['value_method']['required']:
            if  logging:
                logger.debug('-- Creating value methods for ' + csrname)
            size = attr_yaml[csrname]['size']
            bsvstr +=(methodv_dec_temp.format(size, csrname))

    # define csr specific action methods.
    for csrname in isa_yaml:
        if attr_yaml[csrname]['action_method']['required']:
            if  logging:
                logger.debug('-- Creating action methods for ' + csrname)
            size = attr_yaml[csrname]['size']
            arguments = attr_yaml[csrname]['action_method']['def_arguments']
            arguments = arguments.replace('xlen',str(xlen))
            arguments = arguments.replace('size',str(size))
            arguments = textwrap.indent(arguments, '    ')
            bsvstr +=('\n    '+arguments)
    bsvstr +=('\n')

    # create action methods of dependent csrs
    incomming_reads = []
    for csrname in isa_yaml:
        if 'depends_on_csr' in attr_yaml[csrname]:
            if len(attr_yaml[csrname]['depends_on_csr']) != 0:
                if  logging:
                    logger.debug('-- Creating action/read methods for dependencies of ' + csrname)
                for dependent in attr_yaml[csrname]['depends_on_csr']:
                    create_sideband = True
                    dcsr = dependent
                    if '::' in dependent:
                        condition, csr = re.findall(r'^(.*?)::(.*?)$',dependent)[0]
                        if eval(condition) :
                            dcsr = csr
                        else:
                            create_sideband = False
                    if create_sideband and dcsr not in isa_yaml and \
                            dcsr not in incomming_reads \
                            and attr_yaml[dcsr]['size'] is not None:
                        size = attr_yaml[dcsr]['size']
                        bsvstr +=(methoda_read_temp.format('Bit#('+str(size)
                            + ') _' + dcsr, dcsr))
                        incomming_reads.append(dcsr)

    # create methods for shadow csrs not in the current station
    for csrname, content in isa_yaml.items():
        subfields = []
        for s in content[rvxlen]['fields']:
            if isinstance(s, list):
                continue
            else:
                subfields.append(s)
        if not subfields:
            size = attr_yaml[csrname]['size']
            if content[rvxlen]['shadow'] is not None:
                if  logging:
                    logger.debug('-- Creating action/read methods for shadow csr :' + csrname)
                shadow_csr = content[rvxlen]['shadow'].split('.')[0]
                if shadow_csr not in isa_yaml and \
                        shadow_csr not in incomming_reads and\
                        attr_yaml[shadow_csr]['size']is not None:
                    bsvstr +=(methoda_read_temp.format('Bit#('+str(size)
                            + ') _' + shadow_csr, shadow_csr))
                    incomming_reads.append(shadow_csr)

    if logging:
        logger.info('Interface created for : ' + pkg_name)
    # define generic methods for all stations
    bsvstr +=(method_station_generic)
    if not last:
        bsvstr +=(method_fwd_temp)
    bsvstr += (end_interface_temp)
    return bsvstr

def station_module(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):

    ''' 
        Function to create the bluespec module syntax and other synthesis 
        attributes of the module 

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''

    if logging:
        logger.info('Creating module for : ' + pkg_name)

    for csrname in isa_yaml:
        if 'mod_attributes' in attr_yaml[csrname]:
            for modattr in attr_yaml[csrname]['mod_attributes']:
                bsvstr += '  ' + modattr + '\n'
    bsvstr += (module_temp.format(pkg_name))
    if logging:
        logger.info('Module created for : ' + pkg_name)

    return  bsvstr

def station_modbody (isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):
    ''' 
        Function to create the bluespec module rules/body requirements per csr
        basis

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''

    if logging:
        logger.info('Creating custom rules/module elements for : ' + pkg_name)
    for csrname in isa_yaml:
        if 'module_body' in attr_yaml[csrname]:
            bsvstr += textwrap.indent(attr_yaml[csrname]['module_body'],'    ')
    if logging:
        logger.info('Custom rules/module elements created for : ' + pkg_name)
    return bsvstr

def station_methods(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):
    ''' 
        Function to create the bluespec method definitions for each
        group/station. First the value methods of each csr in the group is
        created. Followed by custom action method and then the shadow/dependent
        csrs.

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''
    xlen = int(rvxlen[2:])
    if logging:
        logger.info('Creating method definitions for : ' + pkg_name)
    
    # default value methods
    for csrname in isa_yaml:
        if logging:
            logger.debug('-- Defining value methods for : ' + csrname)
        if attr_yaml[csrname]['value_method']['required']:
            if 'dec_body' in attr_yaml[csrname]['value_method']:
                bsvstr += methodv_def_temp.format(csrname, '', attr_yaml[csrname]['value_method']['dec_body'])
            else:
                bsvstr += methodv_def_temp.format(csrname, 'rg_', csrname)
    
    # custom action methods
    for csrname in isa_yaml:
        if logging:
            logger.debug('-- Defining custom Action methods for : ' + csrname)
        if attr_yaml[csrname]['action_method']['required']:
            size = attr_yaml[csrname]['size']
            _str = attr_yaml[csrname]['action_method']['dec_body']
            _str = _str.replace('size', str(size))
            bsvstr += textwrap.indent( _str+ '\n', '    ')
    
    # create action methods of dependent csrs
    incomming_reads = []
    for csrname in isa_yaml:
        if 'depends_on_csr' in attr_yaml[csrname]:
            if len(attr_yaml[csrname]['depends_on_csr']) != 0:
                if logging:
                    logger.debug('-- Defining action methods for dependencies of : ' + csrname)
                for dependent in attr_yaml[csrname]['depends_on_csr']:
                    create_sideband = True
                    dcsr = dependent
                    if '::' in dependent:
                        condition, csr = re.findall(r'^(.*?)::(.*?)$',dependent)[0]
                        if eval(condition) :
                            dcsr = csr
                        else:
                            create_sideband = False
                    if create_sideband and dcsr not in isa_yaml and \
                            dcsr not in incomming_reads \
                            and attr_yaml[dcsr]['size'] is not None:
                        size = attr_yaml[dcsr]['size']
                        if 'reg_instantiation' in attr_yaml[csrname]:
                            if len(attr_yaml[csrname]['reg_instantiation']) !=0 :
                                bsvstr += temp_method_shadow.format(str(size), dcsr)
                        else:
                            bsvstr += temp_method_shadow.format(str(size), dcsr)
                        incomming_reads.append(dcsr)
    # create methods for shadow csrs not in the current station
    for csrname, content in isa_yaml.items():
        subfields = []
        for s in content[rvxlen]['fields']:
            if isinstance(s, list):
                continue
            else:
                subfields.append(s)
        if not subfields:
            size = attr_yaml[csrname]['size']
            if content[rvxlen]['shadow'] is not None:
                if logging:
                    logger.debug('-- Defining Action methods for shadows of : ' + csrname)
                shadow_csr = content[rvxlen]['shadow'].split('.')[0]
                if shadow_csr not in isa_yaml and\
                        attr_yaml[shadow_csr]['size']is not None and \
                        shadow_csr not in incomming_reads:
                    if 'reg_instantiation' in attr_yaml[csrname]:
                        if len(attr_yaml[csrname]['reg_instantiation']) !=0 :
                            bsvstr += temp_method_shadow.format(str(size), shadow_csr)
                    else:
                        bsvstr += temp_method_shadow.format(str(size), shadow_csr)
                    incomming_reads.append(shadow_csr)

    bsvstr += method_generic_def_temp
    if not last:
        bsvstr += method_fwd_def_temp
    return bsvstr

def station_req(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):
    ''' 
        The function to create the final methods which serves the request from
        the core for each csr.

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''

    if logging:
        logger.info('Generating Core request routine for : ' + pkg_name)
    bsvstr += method_csr_req_def_temp
    bsvstr += method_case_req
    xlen = int(rvxlen[2:])

    for csrname in isa_yaml:
        size = attr_yaml[csrname]['size']
        address = isa_yaml[csrname]['address']
        ro = False
        is_shadow = False
        shadow_csr = None
        regname = csrname

        if not isa_yaml[csrname][rvxlen]['fields'] :
            if isa_yaml[csrname][rvxlen]['shadow'] is not None:
                is_shadow = True
                shadow_csr = isa_yaml[csrname][rvxlen]['shadow']

        if (address & 0xC00) == 0xC00:
            ro = True

        if 'write_condition' in attr_yaml[csrname]:
            write_cond = attr_yaml[csrname]['write_condition']
        else:
            write_cond = ''

        if is_shadow: 
            regname = shadow_csr
        logger.debug('Case statement for ' +csrname + ' Address: ' +\
                str(address))

        if 'csr_op' in attr_yaml[csrname] and (\
                shadow_csr is None or shadow_csr in isa_yaml):
                if logging:
                    logger.debug('-- Creating custom logic for : ' + csrname)
                _t = attr_yaml[csrname]['csr_op'].replace('size',str(size))
                _t = _t.replace('xlen',str(xlen))
                _t = textwrap.indent(_t, '            ') + '\n'
                bsvstr += _t
        elif ro:
            bsvstr += case_def_ro.format(csrname.upper(), regname, xlen)
            if logging:
                logger.debug('-- Creating read-only logic for : ' + csrname)
        else:
            bsvstr += case_def.format(csrname.upper(), regname, xlen, write_cond)
            if logging:
                logger.debug('-- Creating default logic for : ' + csrname)
    
    if last:
        bsvstr += (endcase_temp)
    else:
        bsvstr += (endcase_fwd_temp)
    if logging:
        logger.info('Core request routine created for : ' + pkg_name)

    return bsvstr

def station_regs(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkg_name,
        last, bsvstr, logging = False):
    '''
        Function to create the register and wires required to create the csrs.
        The function also creates WARL bluespec syntax using the
        derive_warl_func function.

        First the shadow/dependent wires are declared followed by the
        instantiation of the csrs present in the current group

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkg_name: name of the bluespec package this code belongs to.
        :param last: indicating this is the last station in the chain
        :param bsvstr: string containing rest of the code generated for the particular group/station
        :param work_dir: path to the directory where the bluespec files should be generated
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkg_name: str
        :type last: bool
        :type bsvstr: str
        :type work_dir: str
    '''
    if logging:
        logger.info('Generating storage elements for : ' + pkg_name)
    bsvstr += (other_vars_temp)
    shadows = []
    xlen = int(rvxlen[2:])
    # create wires of dependent csrs
    incomming_reads = []
    for csrname in isa_yaml:
        if 'depends_on_csr' in attr_yaml[csrname]:
            if len(attr_yaml[csrname]['depends_on_csr']) != 0:
                for dependent in attr_yaml[csrname]['depends_on_csr']:
                    create_sideband = True
                    dcsr = dependent
                    if '::' in dependent:
                        condition, csr = re.findall(r'^(.*?)::(.*?)$',dependent)[0]
                        if eval(condition) :
                            dcsr = csr
                        else:
                            create_sideband = False
                    if create_sideband and dcsr not in isa_yaml and \
                            dcsr not in incomming_reads \
                            and attr_yaml[dcsr]['size'] is not None:
                        size = attr_yaml[dcsr]['size']
                        bsvstr += temp_wire.format(size, dcsr)
                        incomming_reads.append(dcsr)


    for csrname,content in isa_yaml.items():
        if logging:
            logger.debug('-- Creating storage for : ' + csrname)
        subfields = []
        for s in content[rvxlen]['fields']:
            if isinstance(s, list):
                continue
            else:
                subfields.append(s)
        description = content['description']
        reset_val = content['reset-val']
        size = attr_yaml[csrname]['size']
        concat = []

        if not subfields:
            if 'reg_instantiation' in attr_yaml[csrname]:
                if len(attr_yaml[csrname]['reg_instantiation']) !=0 :
                    bsvstr += attr_yaml[csrname]['reg_instantiation'] + '\n'
            elif content[rvxlen]['shadow'] is not None:
                shadow_csr = content[rvxlen]['shadow'].split('.')[0]
                if shadow_csr not in isa_yaml and shadow_csr not in incomming_reads and\
                        attr_yaml[shadow_csr]['size']is not None:
                    bsvstr += temp_wire.format(size, shadow_csr)
                    incomming_reads.append(shadow_csr)
            elif 'ro_constant' in content[rvxlen]['type']:
                bsvstr += temp_readOnlyRegister.format(description, str(size),
                        csrname, reset_val)
            elif ('warl' in content[rvxlen]['type']):
                bsv_str = derive_warl_func( csrname, str(size),
                        content[rvxlen]['type']['warl']['legal'][0])
                bsvstr += temp_warlReg.format(description, str(size), 
                            csrname, reset_val, bsv_str)
            else:
                bsvstr +=  temp_register.format(description, str(xlen), csrname,
                        reset_val)
        else:
            for subfield in subfields:
                if logging:
                    logger.debug('|---- Subfield: ' + subfield)
                if subfield is not 'wlrl':
                    subcontent = isa_yaml[csrname][rvxlen][subfield]
                    if 'type' in subcontent:
                        type_reg = subcontent['type']
                    else:
                        type_reg = ''
                    msb = subcontent['msb']
                    lsb = subcontent['lsb']
                    subdescription = subcontent['description']
                    width = msb - lsb + 1
                    subreset_val = get_reset_val(reset_val, width, lsb, str(xlen))
                    if subcontent['shadow'] is not None:
                        concat.append([ msb, width, subcontent['shadow'].replace('.','_'), ''])
                    else:
                        concat.append([ msb, width, csrname + '_' + subfield, 
                         type_reg])

                    if subfield == 'sd' and csrname == 'mstatus':
                        bsvstr += temp_readOnlyRegister.format(subdescription,
                                str(width), csrname+'_'+subfield, 
                                "pack((rg_mstatus_xs == 2\'b11) || (rg_mstatus_fs == 2\'b11))")
                    elif subcontent['shadow'] is not None:
                        shadow_csr = subcontent['shadow'].split('.')[0]
                        if shadow_csr not in isa_yaml and shadow_csr not in incomming_reads and\
                                attr_yaml[shadow_csr]['size']is not None:
                            bsvstr += temp_wire.format(size, shadow_csr)
                            incomming_reads.append(shadow_csr)

                    elif 'ro_constant' in type_reg:
                        bsvstr += temp_readOnlyRegister.format(subdescription,
                                str(width), csrname+'_'+subfield, subreset_val)
                    elif 'warl' in type_reg:
                        bsv_str = derive_warl_func( subfield,
                            str(width),subcontent['type']['warl']['legal'][0])
                        bsvstr += temp_warlReg.format(subdescription,
                                    str(width), csrname+'_'+subfield, subreset_val, bsv_str)
                    else:
                        bsvstr += temp_readOnlyRegister.format(subdescription,
                                str(width), csrname+'_'+subfield, 0)
            length, cv = create_concat_vector(concat, int(xlen))
            bsvstr += concat_temp.format(description, xlen, csrname,\
                      length, cv)
    if logging:
        logger.info('Storage elements created for : ' + pkg_name)
    return bsvstr

def find_group(bar, csrname, logging=False):
    '''
        Function to find the group which a particular csr belongs to in the
        grouping yaml

        :param bar: the grouping YAML
        :param csrname: the name of the csr
        :type bar: dict
        :type csrname: str

        :return: name of thr group where the csr belongs. None if it is absent altogether
    '''
    for grps in bar:
        if csrname.upper() in bar[grps]:
            return grps
    return None

def csr_top(isa_yaml, grp_yaml, attr_yaml, rvxlen, pkgname, logging = False):
    '''
        Function to create the top level bluespec module which instantiates the
        individual group/station and creates the connection between them.

        The function also creates the methods required for handling traps and
        returns.

        :param isa_yaml: the riscv-config isa YAML
        :param grp_yaml: the grouping YAML
        :param attr_yaml: the attributes YAML
        :param rvxlen: a string containing the format: "rv32" or "rv64" depending on the XLEN value of the DUT
        :param pkgname: name of the bluespec package this code belongs to.
        
        :type isa_yaml: dict 
        :type grp_yaml: dict 
        :type attr_yaml: dict 
        :type rvxlen: str
        :type pkgname: str
    '''

    grp_list = sorted(list(grp_yaml))
    xlen = int(rvxlen[2:])
    if logging:
        logger.info('Creating file Top file : ' + str(pkgname))
    bsvstr = ''

    # initial license and imports
    bsvstr += license_header.format(version, str(datetime.datetime.now()))
    bsvstr += package_temp.format(pkgname)
    
    misa_grp = find_group(grp_yaml, 'misa')
    mstatus_grp = find_group(grp_yaml, 'mstatus')
    mepc_grp = find_group(grp_yaml, 'mepc')
    mtval_grp = find_group(grp_yaml, 'mtval')
    mcause_grp = find_group(grp_yaml, 'mcause')
    mtvec_grp = find_group(grp_yaml, 'mtvec')
    sstatus_grp = find_group(grp_yaml, 'sstatus')
    sepc_grp = find_group(grp_yaml, 'sepc')
    stval_grp = find_group(grp_yaml, 'stval')
    scause_grp = find_group(grp_yaml, 'scause')
    stvec_grp = find_group(grp_yaml, 'stvec')
    ustatus_grp = find_group(grp_yaml, 'ustatus')
    uepc_grp = find_group(grp_yaml, 'uepc')
    utval_grp = find_group(grp_yaml, 'utval')
    ucause_grp = find_group(grp_yaml, 'ucause')
    utvec_grp = find_group(grp_yaml, 'utvec')
    medeleg_grp = find_group(grp_yaml, 'medeleg')
    mideleg_grp = find_group(grp_yaml, 'mideleg')
    sedeleg_grp = find_group(grp_yaml, 'sedeleg')
    sideleg_grp = find_group(grp_yaml, 'sideleg')

    usertraps = False
    if None not in (ustatus_grp, uepc_grp, utval_grp, ucause_grp, utval_grp):
        usertraps = True
    supervisor = False
    if None not in (sstatus_grp, sepc_grp, stval_grp, scause_grp, stval_grp):
        supervisor = True


    # imports of each station
    if logging:
        logger.debug('-- Creating imports')
    for groups in grp_yaml:
        bsvstr += 'import csrbox_' + groups + ' :: * ;\n'
    bsvstr += 'import csrbox_decoder :: * ;'
    
    
    if logging:
        logger.debug('-- Creating interface')
    bsvstr += interface_temp.format(pkgname)
    # define a value method for each csr.
    for csrname in isa_yaml:
        if logging:
            logger.debug('-- Creating Interface for ' + csrname)
        if attr_yaml[csrname]['value_method']['required']:
            size = attr_yaml[csrname]['size']
            bsvstr +=(methodv_dec_temp.format(size, csrname))

    # define csr specific action methods.
    for csrname in isa_yaml:
        if logging:
            logger.debug('-- Creating custom action methods for : ' + csrname)
        if attr_yaml[csrname]['action_method']['required'] and \
                attr_yaml[csrname]['action_method']['global']: 
            size = attr_yaml[csrname]['size']
            arguments = attr_yaml[csrname]['action_method']['def_arguments']
            arguments = arguments.replace('xlen',str(xlen))
            arguments = arguments.replace('size',str(size))
            arguments = textwrap.indent(arguments, '    ')
            bsvstr +=('\n    '+arguments)
    bsvstr += ('\n')
    bsvstr += (method_top_generic.format(xlen))
    bsvstr += (end_interface_temp)
    # -------------- interface definition done ------------------------------#
    
    #--- create module
    if logging:
        logger.debug('-- Creating module')
    bsvstr += module_temp.format(pkgname) + '\n'

    if logging:
        logger.debug('-- Instatiating groups')
    # -- instantiate groups
    for grps in grp_yaml:
        bsvstr += '    let ' + grps + ' <- mk_csrbox_' + grps + ';\n'
   
    bsvstr += '''
    let lv_misa_s = {0}.mv_csr_misa[18];
    let lv_misa_u = {0}.mv_csr_misa[20];
    let lv_misa_n = {0}.mv_csr_misa[13];
    let lv_misa_c = {0}.mv_csr_misa[2];
    /*doc:reg: holds the current privilege level*/
    Reg#(Privilege_mode) rg_prv <- mkReg(Machine);
'''.format(misa_grp)

    anyhit = ''
    anydata = ''
    for grp in grp_yaml:
        anyhit += grp + '.mv_core_resp.hit' + ' || '
        anydata += grp + '.mv_core_resp.data' + ' | '
    anyhit = anyhit[:-4]
    anydata = anydata[:-3]
    bsvstr += check_hit_temp.format(anyhit, anydata, xlen)

    # req=response connection across stations
    if logging:
        logger.debug('-- Creating connections between core-fwd interfaces')
    for i in range(len(grp_list)-1):
        bsvstr += temp_req_connection.format(grp_list[i], grp_list[i+1])
    
    # -- connect rg_prv to all stations
    for grp in grp_yaml:
        bsvstr += temp_prv_connection.format(grp)
    
    # create action methods of dependent csrs
    if logging:
        logger.debug('-- defining action methods')
    for grp in grp_yaml:
        incomming_reads = []
        for csrs in grp_yaml[grp]:
            csrname = csrs.lower()
            if 'depends_on_csr' in attr_yaml[csrname]:
                if len(attr_yaml[csrname]['depends_on_csr']) != 0:
                    for dependent in attr_yaml[csrname]['depends_on_csr']:
                        create_sideband = True
                        dcsr = dependent
                        if '::' in dependent:
                            condition, csr = re.findall(r'^(.*?)::(.*?)$',dependent)[0]
                            if eval(condition) :
                                dcsr = csr
                            else:
                                create_sideband = False
                        if create_sideband and dcsr.upper() not in grp_yaml[grp] and \
                                dcsr not in incomming_reads \
                                and attr_yaml[dcsr]['size'] is not None:
                            if logging:
                                logger.debug('-- Creating connections for dependencies\
 of csr: ' +csrname + ' : ' +  str(dcsr))
                            dcsr_grp = find_group(grp_yaml, dcsr)
                            bsvstr += temp_top_csr_connection.format(\
                                    grp, dcsr, dcsr_grp )
                            incomming_reads.append(dcsr)
            subfields = []
            for s in isa_yaml[csrname][rvxlen]['fields']:
                if isinstance(s, list):
                    continue
                else:
                    subfields.append(s)
            if not subfields:
                size = attr_yaml[csrname]['size']
                if isa_yaml[csrname][rvxlen]['shadow'] is not None:
                    shadow_csr = isa_yaml[csrname][rvxlen]['shadow'].split('.')[0]
                    if shadow_csr.upper() not in grp_yaml[grp] and \
                            shadow_csr not in incomming_reads and\
                            attr_yaml[shadow_csr]['size']is not None:
                        if logging:
                            logger.debug('-- Creating connections for shadows of csr: ' +csrname + ' : ' + shadow_csr)
                        shadow_grp = find_group(grp_yaml, shadow_csr)
                        bsvstr += temp_top_csr_connection.format(\
                                    grp, shadow_csr, shadow_grp )
                        incomming_reads.append(shadow_csr)
            
    # return and trap method definitions
    if logging:
        logger.debug('-- Defining trap and return methods')
    bsvstr += method_top_def_temp
    bsvstr += method_top_ret_temp.format(xlen)
    if usertraps :
        bsvstr += method_top_ret_user_temp.format(mstatus_grp, uepc_grp)
    if supervisor:
        bsvstr += method_top_ret_supervisor_temp.format(mstatus_grp, sepc_grp)
    bsvstr += method_top_ret_machine_temp.format(mstatus_grp, mepc_grp)

    bsvstr += method_top_trap_temp.format(xlen)
    if usertraps and supervisor and medeleg_grp is not None \
            and mideleg_grp is not None:
        bsvstr += method_top_trap_sedeleg.format(sedeleg_grp, sideleg_grp)
    if (usertraps or supervisor) and medeleg_grp is not None:
        bsvstr += method_top_trap_medeleg.format(medeleg_grp, mideleg_grp)
    if usertraps:
        bsvstr += method_top_trap_user_temp.format(utval_grp, uepc_grp, ucause_grp,
            mstatus_grp, utvec_grp)
    if supervisor:
        bsvstr += method_top_trap_supervisor_temp.format(stval_grp, sepc_grp, scause_grp,
            mstatus_grp, stvec_grp)
    bsvstr += method_top_trap_machine_temp.format(mtval_grp, mepc_grp, mcause_grp,
            mstatus_grp, mtvec_grp)
    
    # complete the value method for each csr.
    if logging:
        logger.debug('-- Defining value methods')
    for csrname in isa_yaml:
        if attr_yaml[csrname]['value_method']['required']:
            grp = find_group(grp_yaml, csrname.upper())
            bsvstr += methodv_def_temp.format(csrname, grp+'.mv_csr_', csrname)

    
    # define csr specific action methods.
    if logging:
        logger.debug('-- Defining custom action methods')
    for csrname in isa_yaml:
        logger.debug('Top CSR Interface: ' + csrname)
        if attr_yaml[csrname]['action_method']['required'] and \
                attr_yaml[csrname]['action_method']['global']: 
            defs =  attr_yaml[csrname]['action_method']['def_arguments']
            csr_grp = find_group(grp_yaml, csrname.upper())
            methods = re.findall(r'\s*method\s*Action\s*(.*?)[\s(]', defs)
            for x in methods:
                bsvstr += methoda_top_temp.format(x, csr_grp)
            

    # -- end the module
    bsvstr += end_module_temp
    # end package
    bsvstr += end_package_temp
    return bsvstr

