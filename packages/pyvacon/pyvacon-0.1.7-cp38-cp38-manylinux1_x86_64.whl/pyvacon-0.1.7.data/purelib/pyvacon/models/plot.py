# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm


import pyvacon.analytics as analytics
import pyvacon.tools.enums as enums
import pyvacon.tools.converter as converter
import logging


def distribution(expiries, model, n_component, transformation = None,nBins=50, n_sims=1000, n_times_per_year=180, refdate = analytics.ptime()):
    '''
    plot a distribution of a simulated model component
    expiries: array of expiries which must be for a given model: an array of ptimes/datetimes or of integers (interpreted either as days to expiry)
                                                for a given model_lab: array of intgers describin the time points of values already simulaed in lab
    model: may be a BaseModel (then the values are simulated) or a ModelLab (then it i sassumed that simulation has already take place and values are used from lab)
    n_component: number of component for which the values are plotted
    n_sims: number of simulations (only needed if aseModel is given)
    n_times_per_year: number of time steps used within simulation (only needed if aseModel is given)
    refdate: reference date used in model siulation (only needed if aseModel is given)
    '''
    lab = None
    if isinstance(model, analytics.BaseModel):
        ptimes = converter.createPTimeList(refDate, expiries)    
        for i in range(len(expiries)):
            expiries[i] = i
        lab = analytics.ModelLab(model, refDate)
        lab.simulate(ptimes, n_sims, n_times)
    else:
        if isinstance(model, analytics.ModelLab):
            for k in expiries:
                if model.nSimTimePoints() <= k:
                    raise('Timeslice not simulated in model lab.')
            lab = model

    if lab == None:
        raise("Either an object of type BaseModel or a ModelLab must be given.")

    for i in range(0,len(expiries)):
        sims = analytics.vectorDouble()
        lab.getTimeSlice(sims, expiries[i], n_component)
        if transformation is not None:
            for j in range(len(sims)):
                sims[j] = transformation(sims[j])
        plt.subplot(len(expiries), 1, i+1)
        n, bins, patches = plt.hist(sims, nBins, normed=1, facecolor='blue', alpha=0.75)
        if isinstance(expiries[i], analytics.ptime):
            plt.title(expiries[i].to_string())
        else:
            plt.title(str(expiries[i]))


def distribution2d(expiries, model, n_component, transformation = (None,None),nBins=50, n_sims=1000, n_times_per_year=180, refdate = analytics.ptime()):
    '''
    plot a 2d-distribution of a two simulated model components
    expiries: array of expiries which must be for a given model: an array of ptimes/datetimes or of integers (interpreted either as days to expiry)
                                                for a given model_lab: array of intgers describin the time points of values already simulaed in lab
    model: may be a BaseModel (then the values are simulated) or a ModelLab (then it i sassumed that simulation has already take place and values are used from lab)
    n_component: tuple of number of components for which the values are plotted
    transformations: tuple of functions of transformations applied to the two components
    n_sims: number of simulations (only needed if aseModel is given)
    n_times_per_year: number of time steps used within simulation (only needed if aseModel is given)
    refdate: reference date used in model siulation (only needed if aseModel is given)
    '''
    lab = None
    if isinstance(model, analytics.BaseModel):
        ptimes = converter.createPTimeList(refDate, expiries)    
        for i in range(len(expiries)):
            expiries[i] = i
        lab = analytics.ModelLab(model, refDate)
        lab.simulate(ptimes, n_sims, n_times)
    else:
        if isinstance(model, analytics.ModelLab):
            for k in expiries:
                if model.nSimTimePoints() <= k:
                    raise('Timeslice not simulated in model lab.')
            lab = model

    if lab == None:
        raise("Either an object of type BaseModel or a ModelLab must be given.")

    for i in range(0,len(expiries)):
        sims = [analytics.vectorDouble(),analytics.vectorDouble()]
        for k in range(2):
            lab.getTimeSlice(sims[k], expiries[i], n_component[k])
            if transformation[i] is not None:
                for j in range(len(sims)):
                    sims[k][j] = transformation(sims[k][j])
        plt.subplot(len(expiries), 1, i+1)
        plt.hist2d(sims[0], sims[1], nBins, norm=LogNorm())
        if isinstance(expiries[i], analytics.ptime):
            plt.title(expiries[i].to_string())
        else:
            plt.title(str(expiries[i]))
        plt.colorbar()
    
def paths(model_lab, paths,  n_component, legend=True):
    '''
    plot simulated paths
    model_lab: ModelLab containing simulated paths
    paths: array of integers defining the paths plotted
    '''
    plot_paths = []
    for j in paths:
        plot_paths.append([])
    simtimes = []
    model_lab
    for i in range(model_lab.nSimTimePoints()):
        sims = analytics.vectorDouble()
        model_lab.getTimeSlice(sims, i, n_component)
        for j in range(len(paths)):
            plot_paths[j].append(sims[paths[j]])
    for j in range(len(paths)):
       plt.plot(plot_paths[j],'-x', label = str(paths[j]))
    plt.xlabel('Time')
    plt.ylabel('Value')
    if legend:
        plt.legend()
