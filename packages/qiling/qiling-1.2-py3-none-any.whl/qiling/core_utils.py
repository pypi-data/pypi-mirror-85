#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org) 

import os, logging, configparser

from keystone import *
from capstone import *
from binascii import unhexlify

from .utils import ql_build_module_import_name, ql_get_module_function
from .utils import ql_is_valid_arch, ql_is_valid_ostype
from .utils import loadertype_convert_str, ostype_convert_str, arch_convert_str
from .utils import ql_setup_filter, debugger_convert
from .const import QL_OS, QL_OS_ALL, QL_ARCH, QL_ENDIAN, QL_OUTPUT, QL_DEBUGGER
from .const import D_INFO, D_DRPT
from .exception import QlErrorArch, QlErrorOsType, QlErrorOutput
from .loader.utils import ql_checkostype


class QlCoreUtils(object):
    def __init__(self):
        super().__init__()
        self.archtype = None
        self.ostype = None
        self.path = None
        self.archendian = None

    # normal print out
    def nprint(self, *args, **kw):
        if type(self.console) is bool:
            pass
        else:
            raise QlErrorOutput("[!] console must be True or False")     
        
        # FIXME: this is due to console must be able to update during runtime
        if self.log_file_fd is not None:
            if self.multithread == True and self.os.thread_management is not None and self.os.thread_management.cur_thread is not None:
                fd = self.os.thread_management.cur_thread.log_file_fd
            else:
                fd = self.log_file_fd

            # setup filter for logger
            # FIXME: only works for logging due to we might need runtime disable nprint, it should be a global filter not only syscall
            if self.filter != None and self.output == QL_OUTPUT.DEFAULT:
                fd.addFilter(ql_setup_filter(self.filter))
            
            console_handlers = []

            for each_handler in fd.handlers:
                if type(each_handler) == logging.StreamHandler:
                    console_handlers.append(each_handler)

            if self.console == False:
                for each_console_handler in console_handlers:
                    if '_FalseFilter' not in [each.__class__.__name__ for each in each_console_handler.filters]:
                        each_console_handler.addFilter(ql_setup_filter(False))

            elif self.console == True:
                for each_console_handler in console_handlers:
                    for each_filter in [each for each in each_console_handler.filters]:
                        if '_FalseFilter' in each_filter.__class__.__name__:
                            each_console_handler.removeFilter(each_filter)
            
            args = map(str, args)
            msg = kw.get("sep", " ").join(args)

            if kw.get("end", None) != None:
                msg += kw["end"]

            elif msg != os.linesep:
                msg += os.linesep

            fd.info(msg)


    # debug print out, always use with verbose level with dprint(D_INFO,"helloworld")
    def dprint(self, level, *args, **kw):
        try:
            self.verbose = int(self.verbose)
        except:
            raise QlErrorOutput("[!] Verbose muse be int")    
        
        if type(self.verbose) != int or self.verbose > 99 or (self.verbose > 1 and self.output not in (QL_OUTPUT.DEBUG, QL_OUTPUT.DUMP)):
            raise QlErrorOutput("[!] Verbose > 1 must use with QL_OUTPUT.DEBUG or else ql.verbose must be 0")

        if self.output == QL_OUTPUT.DUMP:
            self.verbose = 99

        if int(self.verbose) >= level and self.output in (QL_OUTPUT.DEBUG, QL_OUTPUT.DUMP):
            if int(self.verbose) >= D_DRPT:
                try:
                    current_pc = self.reg.arch_pc
                except:
                    current_pc = 0    

                args = (("0x%x:" % current_pc), *args)        
                
            self.nprint(*args, **kw)


    def add_fs_mapper(self, ql_path, real_dest):
        self.os.fs_mapper.add_fs_mapping(ql_path, real_dest)


    # push to stack bottom, and update stack register
    def stack_push(self, data):
        self.arch.stack_push(data)


    # pop from stack bottom, and update stack register
    def stack_pop(self):
        return self.arch.stack_pop()


    # read from stack, at a given offset from stack bottom
    # NOTE: unlike stack_pop(), this does not change stack register
    def stack_read(self, offset):
        return self.arch.stack_read(offset)


    # write to stack, at a given offset from stack bottom
    # NOTE: unlike stack_push(), this does not change stack register
    def stack_write(self, offset, data):
        self.arch.stack_write(offset, data)


    def debugger_setup(self):
        # default remote server
        remotedebugsrv = "gdb"
        debug_opts = [None, None]

        if self.debugger != True and type(self.debugger) == str:      
            debug_opts = self.debugger.split(":")
    
            if len(debug_opts) == 2 and debug_opts[0] != "qdb":
                pass
            else:  
                remotedebugsrv, *debug_opts = debug_opts
                
            
            if debugger_convert(remotedebugsrv) not in (QL_DEBUGGER):
                raise QlErrorOutput("[!] Error: Debugger not supported")
            
        debugsession = ql_get_module_function("qiling.debugger." + remotedebugsrv + "." + remotedebugsrv, "Ql" + str.capitalize(remotedebugsrv))

        return debugsession(self, *debug_opts)

    def arch_setup(self):
        if not ql_is_valid_arch(self.archtype):
            raise QlErrorArch("[!] Invalid Arch")
        
        if self.archtype == QL_ARCH.ARM_THUMB:
            archtype =  QL_ARCH.ARM
        else:
            archtype = self.archtype

        archmanager = arch_convert_str(archtype).upper()
        archmanager = ("QlArch" + archmanager)

        module_name = ql_build_module_import_name("arch", None, archtype)
        return ql_get_module_function(module_name, archmanager)(self)


    def os_setup(self, function_name = None):
        if not ql_is_valid_ostype(self.ostype):
            raise QlErrorOsType("[!] Invalid OSType")

        if not ql_is_valid_arch(self.archtype):
            raise QlErrorArch("[!] Invalid Arch %s" % self.archtype)

        if function_name == None:
            ostype_str = ostype_convert_str(self.ostype)
            ostype_str = ostype_str.capitalize()
            function_name = "QlOs" + ostype_str
            module_name = ql_build_module_import_name("os", self.ostype)
            return ql_get_module_function(module_name, function_name)(self)

        elif function_name == "map_syscall":
            ostype_str = ostype_convert_str(self.ostype)
            arch_str = arch_convert_str(self.archtype)

            syscall_table = "map_syscall"

            module_name = ql_build_module_import_name("os", ostype_str, syscall_table)
            return ql_get_module_function(module_name, function_name)
        
        else:
            module_name = ql_build_module_import_name("os", self.ostype, self.archtype)
            return ql_get_module_function(module_name, function_name)


    def loader_setup(self, function_name = None):
        if not self.shellcoder:
            archtype, ostype, archendian = ql_checkostype(self.path)
            if self.archtype is None:
                self.archtype = archtype
            if self.ostype is None:
                self.ostype = ostype
            if self.archendian is None:
                self.archendian = archendian

        if not ql_is_valid_ostype(self.ostype):
            raise QlErrorOsType("[!] Invalid OSType")

        if not ql_is_valid_arch(self.archtype):
            raise QlErrorArch("[!] Invalid Arch %s" % self.archtype)

        if function_name == None:
            loadertype_str = loadertype_convert_str(self.ostype)
            function_name = "QlLoader" + loadertype_str
            module_name = ql_build_module_import_name("loader", loadertype_str.lower())
            return ql_get_module_function(module_name, function_name)(self)


    def component_setup(self, component_type, function_name):
        if not ql_is_valid_ostype(self.ostype):
            raise QlErrorOsType("[!] Invalid OSType")

        if not ql_is_valid_arch(self.archtype):
            raise QlErrorArch("[!] Invalid Arch %s" % self.archtype)

        module_name = "qiling." + component_type + "." + function_name
        function_name = "Ql" + function_name.capitalize() + "Manager"
        return ql_get_module_function(module_name, function_name)(self)


    def profile_setup(self):
        if self.profile:
            self.dprint(D_INFO, "[+] Customized profile: %s" % self.profile)

        os_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles", ostype_convert_str(self.ostype) + ".ql")

        if self.profile:
            profiles = [os_profile, self.profile]
        else:
            profiles = [os_profile]

        config = configparser.ConfigParser()
        config.read(profiles)
        return config
    
    # Assembler/Disassembler API

    def create_disassembler(self):
        if self.archtype == QL_ARCH.ARM:  # QL_ARM
            reg_cpsr = self.reg.cpsr
            mode = CS_MODE_ARM
            if self.archendian == QL_ENDIAN.EB:
                reg_cpsr_v = 0b100000
                # reg_cpsr_v = 0b000000
            else:
                reg_cpsr_v = 0b100000

            if reg_cpsr & reg_cpsr_v != 0:
                mode = CS_MODE_THUMB

            if self.archendian == QL_ENDIAN.EB:
                md = Cs(CS_ARCH_ARM, mode)
                # md = Cs(CS_ARCH_ARM, mode + CS_MODE_BIG_ENDIAN)
            else:
                md = Cs(CS_ARCH_ARM, mode)

        elif self.archtype == QL_ARCH.ARM_THUMB:
            md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

        elif self.archtype == QL_ARCH.X86:  # QL_X86
            md = Cs(CS_ARCH_X86, CS_MODE_32)

        elif self.archtype == QL_ARCH.X8664:  # QL_X86_64
            md = Cs(CS_ARCH_X86, CS_MODE_64)

        elif self.archtype == QL_ARCH.ARM64:  # QL_ARM64
            md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

        elif self.archtype == QL_ARCH.A8086:  # QL_A8086
            md = Cs(CS_ARCH_X86, CS_MODE_16)

        elif self.archtype == QL_ARCH.MIPS:  # QL_MIPS32
            if self.archendian == QL_ENDIAN.EB:
                md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN)
            else:
                md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 + CS_MODE_LITTLE_ENDIAN)

        else:
            raise QlErrorArch("[!] Unknown arch defined in utils.py (debug output mode)")

        return md
    
    def create_assembler(self):
        if self.archtype == QL_ARCH.ARM:  # QL_ARM
            reg_cpsr = self.reg.cpsr
            mode = KS_MODE_ARM
            if self.archendian == QL_ENDIAN.EB:
                reg_cpsr_v = 0b100000
                # reg_cpsr_v = 0b000000
            else:
                reg_cpsr_v = 0b100000

            if reg_cpsr & reg_cpsr_v != 0:
                mode = KS_MODE_THUMB

            if self.archendian == QL_ENDIAN.EB:
                ks = Ks(KS_ARCH_ARM, mode)
                # md = Cs(CS_ARCH_ARM, mode + CS_MODE_BIG_ENDIAN)
            else:
                ks = Ks(KS_ARCH_ARM, mode)

        elif self.archtype == QL_ARCH.ARM_THUMB:
            ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)

        elif self.archtype == QL_ARCH.X86:  # QL_X86
            ks = Ks(KS_ARCH_X86, KS_MODE_32)

        elif self.archtype == QL_ARCH.X8664:  # QL_X86_64
            ks = Ks(KS_ARCH_X86, KS_MODE_64)

        elif self.archtype == QL_ARCH.ARM64:  # QL_ARM64
            ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)

        elif self.archtype == QL_ARCH.A8086:  # QL_A8086
            ks = Ks(KS_ARCH_X86, KS_MODE_16)

        elif self.archtype == QL_ARCH.MIPS:  # QL_MIPS32
            if self.archendian == QL_ENDIAN.EB:
                ks = Ks(KS_ARCH_MIPS, KS_MODE_MIPS32 + KS_MODE_BIG_ENDIAN)
            else:
                ks = Ks(KS_ARCH_MIPS, KS_MODE_MIPS32 + KS_MODE_LITTLE_ENDIAN)

        else:
            raise QlErrorArch("[!] Unknown arch defined in utils.py (debug output mode)")

        return ks

class QlFileDes:
    def __init__(self, init):
        self.__fds = init

    def __getitem__(self, idx):
        return self.__fds[idx]

    def __setitem__(self, idx, val):
        self.__fds[idx] = val

    def __iter__(self):
        return iter(self.__fds)

    def __repr__(self):
        return repr(self.__fds)
    
    def save(self):
        return self.__fds

    def restore(self, fds):
        self.__fds = fds
