import os
import socket
import subprocess
import requests
import sys

class start:

  def __init__(self, host, force=False, proxies={"http": '',"https": ''}):
    try:
      ip = socket.gethostbyname(host)
      v = self.get_package_version('stdclasses')
      
      try:
        last_ver = requests.get('http://'+ip+':8080/workbench/biblioteca/last_ver.php',proxies=proxies).text
      except:
        last_ver = None
      v = '1.1.115'
      if v is None or v != last_ver or force:
        if v is None:
          print('STDCLASSES Nao encontrado. Instalando')
        elif v != last_ver:
          print('Nova versao da STDCLASSES encontrada. Atualizando!')
          print('Versao atual: '+v)
          print('Versao nova: '+last_ver)
        else:
          print('Forcando instalacao da STDCLASSES')
        
        try:
          cdsw_user = os.environ['HADOOP_USER_NAME'].upper()
          self.install('http://'+ip+':8080/workbench/biblioteca/install.php', host=host)
        except:
          try:
            cdsw_user = os.environ['NB_USER'].upper()
            self.install('http://'+host+':8080/workbench/biblioteca/install.php', host=host)
          except:
            print('Nao foi possivel instalar/atualizar a biblioteca!')
        
    except Exception as e:
      print(e)
      print('Nao foi possivel instalar/atualizar a biblioteca!')
      print('Se instalacao/atualizacao necessaria, abrir nova sessao')
      
      
      
  
  def get_package_version(self, package = 'stdclasses'):
    v = None
    try:
      p = subprocess.Popen("pip show stdclasses|grep Version",
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT)
          
      results = p.stdout.readlines()
      for r in results:
        if 'Version: ' in r.strip():
          v = r.strip().replace('Version: ', '')
          return v
    except:
      pass
  
    try:
      import pkg_resources
      v = pkg_resources.get_distribution(package).version
    except:
      try:
        from importlib.metadata import version
        v = version(package)
      except:
        pass
    
    return v
  

  def install(self, package, pip2 = True, host=''):
    
    
    results = []
    if not os.path.exists('.stdclasses'):
      os.mkdir('.stdclasses')
    if sys.version_info[0] < 3:
      try:
        a=open('.stdclasses/pip.py', 'wb').write(requests.post('http://'+host+':8080/workbench/biblioteca/pip.txt', proxies = {"http": '',"https": ''}).content)
        p = subprocess.Popen("python2 .stdclasses/pip.py",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.readlines()
        
        a=open('.stdclasses/stdclasses.tar.gz', 'wb').write(requests.post('http://'+host+':8080/workbench/biblioteca/install.php', proxies = {"http": '',"https": ''}).content)
        results = subprocess.Popen("pip2 install .stdclasses/stdclasses.tar.gz",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.readlines()
        
      except:
        pass
        
      
    else:
      try:
        a=open('.stdclasses/stdclasses.tar.gz', 'wb').write(requests.post('http://'+host+':8080/workbench/biblioteca/install.php', proxies = {"http": '',"https": ''}).content)
        results = subprocess.Popen("pip3 install .stdclasses/stdclasses.tar.gz",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.readlines()
        
      except:
        pass
      
    sucesso = False
    mstr = ''
    for result in results:
      if('Successfully installed stdclasses-' in str(result)):
        sucesso = True
        mstr = result
        break
    try:
      version = mstr.replace('\n','').split('-')[1]
    except:
      version = '-'
    if sucesso:
      print('Atualizacao da biblioteca realizada com sucesso!')
      print('Versao instalada (CLI) : {}'.format(version))
      print('Versao instalada (PKG) : {}'.format(self.get_package_version()))
    else:
      print('Houve um problema ao tentar reinstalar a biblioteca')
      
    
  
  
  
  
  

import os
import sys
import socket
from datetime import datetime
import time
import subprocess



from threading import Thread
class ThreadUpdateInststd(Thread):
  def __init__ (self, host):
    Thread.__init__(self, host)
    
  def run(self, host):
    
    if sys.version_info[0] < 3:
      try:
        p = subprocess.Popen("wget https://bootstrap.pypa.io/get-pip.py",
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT)
        results = p.stdout.readlines()
    
        p = subprocess.Popen("python2 get-pip.py",
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT)
        results = p.stdout.readlines()
        
        try:
          files = os.listdir('/home/cdsw/')
        
          for file in files:
            if('get-pip' in file):
              os.remove(file)
        except:
          None
          
      except:
        None
      try:  
        p = subprocess.Popen("pip2 install --upgrade inststd",
          shell=True,
          stdout=subprocess.PIPE,
          stderr=subprocess.STDOUT)
        results = p.stdout.readlines()
      except:
        None
      
    else:
      p = subprocess.Popen("pip3 install --upgrade inststd",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
      results = p.stdout.readlines()
#a = ThreadUpdateInststd().start()

  
  
'''
#import socket
#import requests
#from pip._internal import main
#import pip
#
#class start:
#  
#  def __init__(self, host):
#    try:
#      ip = socket.gethostbyname(host)
#      self.install('http://'+ip+':8080/workbench/biblioteca/install.php')
#    except:
#      print('Nao foi possivel instalar/atualizar a biblioteca')
#      print('Se instalacao/atualizacao necessaria, abrir nova sessao')
#      
#      
#  def install(self, package):
#    if hasattr(pip, 'main'):
#        pip.main(['install', '--upgrade', package])
#    else:
#        main(['install', '--upgrade', package])
'''