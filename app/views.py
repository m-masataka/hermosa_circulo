# -*- coding: utf-8 -*- vim: set et ts=4 sw=4 :
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
import commands
import random
from app.utils.Cylinder import makeobj
from app.utils.lattice import lattice
from django.core.files import File
#from app.utils.bb import Lattice

class MainView(TemplateView):
    '''
    タイトルページ
    '''
    template_name = "index.html"
    def index(request):
        pass

class Boobs_BlenderView(TemplateView):
    '''
    Blenderのページ
    '''
    template_name = "boobs_blender.html"
    def boobs_blender(request):
        pass

class latticeView(TemplateView):
    '''
    latticeのページ
    '''
    template_name = "lattice.html"
    def IGA(request):
        pass

def update_lattice_object(request):
    '''
    latticeのモデルを更新
    '''
    to_x = float(request.POST.get("x",0.0))*10
    to_y = float(request.POST.get("y",0.0))*10
    to_z = float(request.POST.get("z",0.0))*10
    ret = lattice.Lattice_obj(to_x, to_y, to_z)
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../static/OBJfile/lattice.obj')
    file = open(file_path,'w')
    file.write(ret)
    return HttpResponseRedirect(reverse('lattice'))

def update_3D_object(request):
    '''
    3Dモデルの更新をするページ
    '''
    wheel_radius    = int(request.POST.get("wheel_radius",0))
    begining_point  = int(request.POST.get("begining_point",0))
    begin           = 100 - int(request.POST.get("begin",0))
    point_num       = int(request.POST.get("point_num",0))
    breast_wide     = 1.0 - float(request.POST.get("breast_wide",0.0))
    ret = makeobj.make(wheel_radius,begining_point,begin,point_num,breast_wide)
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../static/OBJfile/model2.obj')
    file = open(file_path,'w')
    file.write(ret)
    file.close()
    return HttpResponseRedirect(reverse('index'))
    #return HttpResponse(ret)

def executeBlender(request):
    '''
    Blenderによる3Dモデルの更新をするページ
    '''
    wheel_radius    = request.POST.get("wheel_radius",0)
    begin           = request.POST.get("begin",0)
    point_num       = request.POST.get("point_num",0)
    breast_wide     = request.POST.get("breast_wide",0.0)

    currentdir = str(os.getcwd())
    strcommand = "blender --background --python "+currentdir+"/app/utils/bb/Lattice.py "+wheel_radius+" "+begin+" "+point_num+" "+breast_wide
    check = commands.getoutput(strcommand)

    return HttpResponseRedirect(reverse('boobs_blender'))

def executeIGA(request):
    '''
    IGAによる個体の最適化をするページ
    '''
    file_num = 3
    para_num = 5
    parameter=[[0 for i in range(para_num)] for j in range(file_num)]
    for i in range(len(parameter)):
        for j in range(len(parameter[0])):
            if j == 1:
                parameter[i][j] = 10
            elif j == 3:
                parameter[i][j] = 30
            elif j == 4:
                parameter[i][j] = random.uniform(0.15,0.6)
            else:
                parameter[i][j] = random.randint(30,70)

    for i in range(len(parameter)):
        ret = makeobj.make(parameter[i][0],parameter[i][1],parameter[i][2],parameter[i][3],parameter[i][4])
        file = open(os.path.join(os.getcwd(),'app/static/OBJfile/iga/iga'+str(i)+'.obj'),'w')
        file.write(ret)
        file.close()
    return HttpResponseRedirect(reverse('IGA'))
