# -*- coding: utf-8 -*-
"""
Description: 

Wraps spectral connectivity function of MNE, as well as plot_circular_connectivity

"""
import nipype.pipeline.engine as pe
from nipype.interfaces.utility import IdentityInterface
#,Function

from neuropype_ephy.interfaces.mne.spectral import  SpectralConn,PlotSpectralConn

### to modify and add in "Nodes"
#from neuropype_ephy.spectral import  filter_adj_plot_mat

def create_pipeline_time_series_to_spectral_connectivity( main_path, pipeline_name = "ts_to_conmat",con_method = "coh", multicon = False, export_to_matlab = False, temporal_windows = []):
    
    
    pipeline = pe.Workflow(name= pipeline_name)
    pipeline.base_dir = main_path
    
    inputnode = pe.Node(IdentityInterface(fields=['ts_file','freq_band','sfreq','labels_file','epoch_window_length','is_sensor_space']), name='inputnode')
    
    if multicon == False:
            
        #### spectral
        spectral = pe.Node(interface = SpectralConn(), name = "spectral")
        
        spectral.inputs.con_method = con_method  
        spectral.inputs.export_to_matlab = export_to_matlab
        
        pipeline.connect(inputnode, 'sfreq', spectral, 'sfreq')
        pipeline.connect(inputnode, 'ts_file', spectral, 'ts_file')
        pipeline.connect(inputnode, 'freq_band', spectral, 'freq_band')
        pipeline.connect(inputnode, 'epoch_window_length', spectral, 'epoch_window_length')

        #### plot spectral
        plot_spectral = pe.Node(interface = PlotSpectralConn(), name = "plot_spectral")
        
        pipeline.connect(inputnode,  'labels_file',plot_spectral,'labels_file')
        pipeline.connect(inputnode,  'is_sensor_space',plot_spectral,'is_sensor_space')
        
        pipeline.connect(spectral, "conmat_file",    plot_spectral, 'conmat_file')
        
        #if filter_spectral == True:
                
            #### filter spectral
            #filter_spectral = pe.Node(interface = Function(input_names = ["conmat_file","labels_file","sep_label_name","k_neigh"], 
                                                        #output_names = "filtered_conmat_file", 
                                                        #function = filter_adj_plot_mat), name = "filter_spectral_" + str(k_neigh))
            #filter_spectral.inputs.sep_label_name = sep_label_name
            #filter_spectral.inputs.k_neigh = k_neigh
            
            #pipeline.connect(split_ascii,  'elec_names_file',filter_spectral,'labels_file')
            #pipeline.connect(spectral, "conmat_file",    filter_spectral, 'conmat_file')
            
            
            
            ##### plot filter_spectral
            #plot_filter_spectral = pe.Node(interface = Function(input_names = ["conmat_file","labels_file","nb_lines","vmin","vmax"],
                                                        #output_names = "plot_conmat_file",
                                                        #function = plot_circular_connectivity), name = "plot_filter_spectral_" + str(k_neigh))
            
            ## plot_spectral.inputs.labels_file = MEG_elec_names_file AP 021015
            #plot_filter_spectral.inputs.nb_lines = 50
            
            #plot_filter_spectral.inputs.vmin = 0.3
            #plot_filter_spectral.inputs.vmax = 1.0
        
        
            #pipeline.connect(split_ascii,  'elec_names_file',plot_filter_spectral,'labels_file')
            #pipeline.connect(filter_spectral, "filtered_conmat_file",    plot_filter_spectral, 'conmat_file')
        
    elif len(temporal_windows) != 0:
      print "Not done yet...."
      
    #else:
       
        
        
        ##### spectral
        #spectral = pe.Node(interface = Function(input_names = ["ts_file","sfreq","freq_band","con_method"],
                                                #output_names = "conmat_files",
                                                #function = multiple_spectral_proc),name = "spectral")
        
        #spectral.inputs.con_method = con_method    
        #spectral.inputs.sfreq = sfreq
        
        #pipeline.connect(split_ascii, 'splitted_ts_file', spectral, 'ts_file')

    return pipeline
    