
Generate cloud masks (scene classification, actually) for a general
class of optical sensors by using Hyperion data to transfer already
labeled spectra from Sentinel-2 to any other (suitable) sensor.

Imports and Tables
==================

.. code:: python

    %load_ext autoreload
    %autoreload 2

.. code:: python

    import numpy as np
    import h5py
    from scipy.interpolate import interp1d
    from tqdm import tqdm
    from os import path, makedirs
    import matplotlib.image as mpimg
    from glob import glob
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    %matplotlib inline
    
    from sicor.sensors import SensorSRF
    from sicor.tables import get_tables

.. code:: python

    def get_srf(sensor):
        """Get needed parameters from sicor.SensorSRF instance.
        :param sensor: Name of Sensor, e.g. one of ("S2A", "Landsat-7", "Landsat-8")
        :return dict
        """
        srf_obj = SensorSRF(sensor=sensor)
        srfs_wvl = np.array(srf_obj.srfs_wvl,dtype=np.float)
        srf_bands = [band for band in srf_obj.bands if np.trapz(x=srfs_wvl,y=srf_obj.srfs[band])>0.0]    
        srf_stack = np.stack([np.array(srf_obj.srfs[band],dtype=np.float) for band in srf_bands])
        srf_stack = (srf_stack.transpose() / np.trapz(x=srfs_wvl,y=srf_stack,axis=1)).transpose()
        bands_wvl = np.trapz(x=srfs_wvl, y=srf_stack * srf_obj.srfs_wvl,axis=1) / np.trapz(x=srfs_wvl, y=srf_stack,axis=1)
        return {
            "srf_obj":srf_obj,
            "srf_stack":srf_stack,
            "srf_wvl":srfs_wvl,
            "bands_wvl":bands_wvl,
            "bands":srf_bands
        }

.. code:: python

    sensors = ("S2A","Landsat-4", "Landsat-5", "Landsat-7", "Landsat-8")
    srfs = {sensor:get_srf(sensor) for sensor in sensors}

Prepare Transfer Tables
=======================

Use a library oy Hyperion spectra (hyperspectral\_sample.hdf5, included
in sicor), use sensor response function to compute corresponding
spectral libraries for a range of sensors.

.. code:: python

    # download tables if needed
    get_tables(optional_downloads=("hyperspectral_sample",))

.. code:: python

    if True:
        # read hyper spectral data from database
        h5f = h5py.File("./../sicor/tables/hyperspectral_sample.hdf5")
        data = np.array(h5f["data"],dtype=np.float)
        wvl = np.array(h5f["wvl"],dtype=np.float)
        fwhm = np.array(h5f["fwhm"],dtype=np.float)
        h5f.close()
    
    if False:    
        data_transfer = {ii:np.zeros((data.shape[0],len(srfs[ii]["bands"])),dtype=np.float) for ii in sensors}
        for sensor in sensors:
            print(sensor)
            print(", ".join(["%s:%.0fnm" % (band,wv) for band,wv in zip(srfs[sensor]["bands"],srfs[sensor]["bands_wvl"])]))
    
        for ii in tqdm(range(data.shape[0])):
            for sensor in sensors:
                data_transfer[sensor][ii,:] = np.trapz(
                    interp1d(x=wvl,y=data[ii,:],kind='cubic',fill_value=0,bounds_error=False)(srfs[sensor]["srf_wvl"]) * srfs[sensor]["srf_stack"],
                    axis=1)
    
        ii = 10
        plt.plot(wvl,data[ii,:])
        for sensor in sensors:
            plt.plot(srfs[sensor]["bands_wvl"],data_transfer[sensor][ii,:],".",label=sensor)
        plt.legend()   
    
        h5f = h5py.File("./../sicor/tables/transfer_spectra.hdf5","w")
        h5f.create_dataset(name="sensors",data=",".join(sensors))
        for sensor in sensors:
            h5f.create_dataset(name=sensor,data=data_transfer[sensor])
            h5f.create_dataset(name="%s_bands" % sensor,data=",".join(srfs[sensor]["bands"]))
            h5f.create_dataset(name="%s_bands_wvl" % sensor,data=np.array(srfs[sensor]["bands_wvl"]))
        h5f.close()

.. code:: python

    h5f = h5py.File("./../sicor/tables/transfer_spectra.hdf5","r")

.. code:: python

    list(h5f.keys())




.. parsed-literal::

    ['Landsat-4',
     'Landsat-4_bands',
     'Landsat-4_bands_wvl',
     'Landsat-5',
     'Landsat-5_bands',
     'Landsat-5_bands_wvl',
     'Landsat-7',
     'Landsat-7_bands',
     'Landsat-7_bands_wvl',
     'Landsat-8',
     'Landsat-8_bands',
     'Landsat-8_bands_wvl',
     'S2A',
     'S2A_bands',
     'S2A_bands_wvl',
     'sensors']



.. code:: python

    sensors_colors = {
        'S2A':colors['firebrick'],
        'Landsat-4': colors['darkgreen'], 
        'Landsat-5': colors['darkcyan'], 
        'Landsat-7': colors["darkorchid"], 
        'Landsat-8': colors["sienna"],
        'HyerSpectral': colors['gray'],
    }

.. code:: python

    ii = 10
    fig = plt.figure(figsize=(10,7))
    ax = plt.subplot(1,1,1)
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
    
    bfd = np.copy(data[ii,:])
    ax.plot(wvl,bfd / np.max(bfd),label='HyerSpectral',color=sensors_colors['HyerSpectral'])
    ax.text(txt_x,0.5,"Hyper Spectral",verticalalignment='center', horizontalalignment='left', color=sensors_colors['HyerSpectral'])
    
    
    
    for isensor, sensor in enumerate(sensors,1):
        ax.plot(srfs[sensor]["bands_wvl"],data_transfer[sensor][ii,:] / np.max(bfd),".",label=sensor, color=sensors_colors[sensor])
        
        jj = np.argsort(srfs[sensor]["bands_wvl"])
        bf = np.copy(data_transfer[sensor][ii,jj])
        bf -= np.min(bf)
        bf /= np.max(bf)
        
        ax.plot(srfs[sensor]["bands_wvl"][jj],isensor + bf,"-o",label=sensor, color=sensors_colors[sensor])
        
        for i,jjj in enumerate(jj):
            ax.vlines(
                srfs[sensor]["bands_wvl"][jjj],
                data_transfer[sensor][ii, jjj] / np.max(bfd),
                isensor + bf[i],
                color=sensors_colors[sensor],
                linestyle="--",
                linewidth=1
            )
        
        
        ax.text(txt_x,isensor + 0.5,sensor,verticalalignment='center', horizontalalignment='left',color=sensors_colors[sensor])
    
        
    plt.xlabel("wavelenght in nm")
    plt.ylabel("same scene sampled\n by different instruments")
    
    for isp,spine in enumerate(plt.gca().spines.values()):
        spine.set_visible(False)
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/same_target_different_sensors.pdf",bbox_inches="tight")
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/same_target_different_sensors.jpg",bbox_inches="tight",dpi=400)



.. image:: examples/sicor_scene_detection/sicor_scene_detection_13_0.png

.. code:: python

    SMALL_SIZE = 16
    MEDIUM_SIZE = 20
    BIGGER_SIZE = 20
    
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    fig = plt.figure(figsize=(10,7))
    ax = plt.subplot(1,1,1)
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')
    
    txt_x = 0.99 * np.max(srfs[sensor]['srf_wvl'])
    
    def gauss(x, w, s):
        return np.exp(-(x-w)**2/(2*s**2))
    
    for wv in wvl[::3]:
        bf = 0.7 * gauss(srfs[sensor]['srf_wvl'],wv,10)
        bf[bf < 0.01] = np.NaN
        ax.plot(srfs[sensor]['srf_wvl'],bf,color=sensors_colors['HyerSpectral'])
    ax.text(txt_x,0.5,"Hyper Spectral",verticalalignment='center', horizontalalignment='left', color=sensors_colors['HyerSpectral'])
    
    
    for isensor,sensor in enumerate(sensors,1):
        bf = np.copy(srfs[sensor]["srf_stack"].transpose())
        bf[bf == 0.0] = np.NaN
        bf /= np.nanmax(bf)
        _ = ax.plot(srfs[sensor]['srf_wvl'],isensor+bf,color=sensors_colors[sensor],label=sensor)
        ax.text(txt_x,isensor + 0.5,sensor,verticalalignment='center', horizontalalignment='left',color=sensors_colors[sensor])
        
    plt.xlabel(r"wavelenght in nm")
    plt.ylabel(r"instrument response functions")
    
    for isp,spine in enumerate(plt.gca().spines.values()):
        spine.set_visible(False)
        
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/response_fuctions.pdf",bbox_inches="tight")    
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/response_fuctions.jpg",bbox_inches="tight",dpi=400)



.. image:: examples/sicor_scene_detection/sicor_scene_detection_14_0.png

.. code:: python

    nbins=20
    s1,s2 = ('S2A', 'Landsat-8')
    
    def hh_scale(hh):
        hh /= np.max(hh)
        hh = hh**0.1
        hh[hh<0.1] = np.NaN
        return hh[::-1,:]
    
    hh = np.hstack([np.vstack([hh_scale(np.histogram2d(data_transfer[s1][:,i1], data_transfer[s2][:,i2], bins=nbins, normed=True)[0]) for i2 in range(n2)]) for i1 in range(n1)])

.. code:: python

    s1




.. parsed-literal::

    'S2A'







.. parsed-literal::

    array([  443.92944484,   496.54106969,   560.00637495,   664.4491622 ,
             703.88697894,   740.22345252,   782.47351198,   835.11018679,
             945.02752948,  1373.46188255,  1613.65940666,  2202.36668717,
             864.80125832])



.. code:: python

    fig = plt.figure(figsize=(10,10))
    plt.imshow(hh,cmap=plt.cm.Oranges)
    ax = plt.subplot(1,1,1)
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='off')
    for isp,spine in enumerate(plt.gca().spines.values()):
        spine.set_visible(False)
    
    for i1 in range(0,n1):
        ax.text(i1*nbins+nbins / 2,0,"%s = %.1f nm" % (s1,srfs[s1]['bands_wvl'][i1]), rotation=45, **{'ha': 'left', 'va': 'bottom'})
    for i2 in range(0,n2):
        ax.text(nbins*n1, i2*nbins+1.3*(nbins / 2),"%s = %.1f nm" % (s2,srfs[s2]['bands_wvl'][i2]), rotation=45, **{'ha': 'left', 'va': 'bottom'})
        
    for i1 in range(1,n1):
        for i2 in range(1,n2):
            ax.vlines(i1 * nbins,0,n2*nbins,linestyle="--",linewidth=1)
            ax.hlines(i2 * nbins,0,n1*nbins,linestyle="--",linewidth=1)
            
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/sensor_to_sensor.pdf",bbox_inches="tight")
    plt.savefig("/home/hollstei/dat/projekte/GeoMultiSens/paper/sensor_to_sensor.jpg",bbox_inches="tight",dpi=400)



.. image:: examples/sicor_scene_detection/sicor_scene_detection_18_0.png


Build Transfer Models
=====================

.. code:: python

    from sklearn.pipeline import Pipeline
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import Normalizer
    from sklearn.model_selection import train_test_split
    from random import sample
    from sklearn.model_selection import GridSearchCV
    from random import choice
    from inspect import getargspec
    
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.cluster import DBSCAN
    from sicor.Tools.cB.classical_bayesian import write_classical_bayesian_to_hdf5_file
    from sicor.Tools.cB.classical_bayesian import read_classical_bayesian_from_hdf5_file
    from sicor.Tools.cB.classical_bayesian import __test__
    from sicor.Tools.cB.classical_bayesian import ClassicalBayesianFit, ToClassifierDef, get_clf_functions, ClassicalBayesian

.. code:: python

    class_names = {'Shadow': 30, 'Clear': 10, 'Snow': 60, 'Water': 20, 'Cirrus': 40, 'Cloud': 50}
    class_ids = {v:k for k,v in class_names.items()}
    mask_legend = {value:key for key,value in class_names.items()}
    # RGB color coding of classes
    clf_to_col = {10: (0.0, 0.39215686274509803, 0.0),
                  20: (0.0, 0.0, 0.5019607843137255),
                  30: (0.5450980392156862, 0.0, 0.5450980392156862),
                  40: (0.5450980392156862, 0.0, 0.0),
                  50: (0.27450980392156865, 0.5098039215686274, 0.7058823529411765),
                  60: (1.0, 0.5490196078431373, 0.0)}

.. code:: python

    h5f = h5py.File("./../sicor/tables/transfer_spectra.hdf5","r")
    data_transfer = {sensor:np.array(h5f[sensor]) for sensor in h5f["sensors"].value.split(",")}
    print(data_transfer.keys())
    h5f.close()


.. parsed-literal::

    dict_keys(['S2A', 'Landsat-4', 'Landsat-5', 'Landsat-7', 'Landsat-8'])


.. code:: python

    h5f = h5py.File("./../sicor/tables/20170523_s2_manual_classification_data.h5")
    clf_spectra = np.array(h5f["spectra"])
    clf_classes = np.array(h5f["classes"])
    clf_product = np.array(h5f['product_id'])
    clf_granule = np.array(h5f['granule_id'])
    clf_lats = np.array(h5f['latitude'])
    clf_lons = np.array(h5f['longitude'])
    clf_ids = h5f["class_ids"][:]
    clf_names = [cls.decode('unicode_escape') for cls in h5f["class_names"]]
    h5f.close()

Recover Polygons from labeled data
==================================

The labeled spectra originate from polygons, which are lost due to
processing with ENVI. It makes much sense to sample equally from the
polygons than from the whole dataset to give each polygon the same
weight. I try to recover the polygons now using a simple clustering
approach.

.. code:: python

    figpath = "./clf_figs"
    clf_polygons = np.zeros(len(clf_classes),dtype=np.int)
    clf_polygons[-2] = -2
    
    poly_id = 1
    products = np.unique(clf_product)
    noisy_data = 0
    for product in tqdm(products):
        
        sel = clf_product == product 
        granules = np.unique(clf_granule[sel])
        
        for granule in granules:
            
            sel_gran = np.logical_and(sel,clf_granule == granule)
            clfs = np.unique(clf_classes[sel_gran])
            
            # scale lon and lat such they live on the [0,1] intervall -> this helps to use DBSCAN
            scaler = MinMaxScaler().fit(np.stack((clf_lons[sel_gran],clf_lats[sel_gran])).transpose())
            
            
            fig = plt.figure(figsize=(10,10))
            ax = plt.subplot(1,1,1)
            fig_fn = path.join(
                figpath,
                "{product}_{tile}.jpg".format(product=product.decode("utf8"), tile=granule.decode("utf8")))
            
            for clf in clfs:
                sel_clf = np.logical_and(sel_gran,clf_classes == clf)
                
                xx = scaler.transform(np.stack((clf_lons[sel_clf],clf_lats[sel_clf])).transpose())
                dbs = DBSCAN(eps=0.01)
                yy = dbs.fit_predict(X=xx)
                
                
                if np.max([np.sum(yy == ii) for ii in np.unique(yy)]) > 200000:
                    xx_centers = np.array([[np.mean(xx[yy == cl,0]),np.mean(xx[yy == cl,1])] for cl in np.arange(np.max(yy))])
                    _ = plt.plot(xx[:,0], xx[:,1],"b.")
                    _ = plt.plot(xx_centers[:,0], xx_centers[:,1],"r.")
                    
                    raise
                
                ax.plot(xx[:,0], xx[:,1],"%s." % {10:"b", 20:"c", 30:"r", 40:"g", 50:"c", 60:"m"}[clf])
                
                if np.max(yy)>1:
                    xx_centers = np.array([[np.mean(xx[yy == cl,0]),np.mean(xx[yy == cl,1])] for cl in np.arange(np.max(yy))])            
                    ax.scatter(xx_centers[:,0], xx_centers[:,1],c="y",s=10,edgecolor="k",linewidth=0.6, zorder=10)
                
                noisy_data += np.sum(yy == -1)
                yy[yy == -1] = -1 - poly_id
                clf_polygons[sel_clf] = poly_id + yy
                clf_polygons[sel_clf][yy == -1] = -1
                
                poly_id += np.max(yy)
                
            makedirs(path.dirname(fig_fn), exist_ok=True)
            plt.savefig(fig_fn, bbox_inches="tight", dpi=150,quality=60)
            plt.close(fig)
    
    spectra_per_polygon = np.array([np.sum(clf_polygons == ii) for ii in np.arange(np.max(clf_polygons))])
    plt.plot(spectra_per_polygon)


.. parsed-literal::

    100%|██████████| 48/48 [03:50<00:00,  4.09s/it]




.. parsed-literal::

    [<matplotlib.lines.Line2D at 0x2b8b670557b8>]




.. image:: examples/sicor_scene_detection/sicor_scene_detection_27_2.png

.. code:: python

    fns  = glob("./clf_figs/*.jpg")
    nx = 3
    ny = np.floor(len(fns) / nx)
    fig = plt.figure(figsize=np.array((nx,ny))*20)
    
    for ifn,fn in enumerate(glob("./clf_figs/*.jpg"),1):
        ax = plt.subplot(ny,nx,ifn)
        ax.set_axis_off()
        ax.imshow(mpimg.imread(fn))
    
    fig.tight_layout()



.. image:: examples/sicor_scene_detection/sicor_scene_detection_28_0.png

Functions
=========

.. code:: python

    def transfer_data_to(tgt,ref="S2A",param_grid=None):
    
        XX_train, XX_test, YY_train, YY_test = train_test_split(
            data_transfer[ref], 
            data_transfer[tgt],
            test_size=0.3)
        print("Test / Train data")
        print(XX_train.shape,XX_test.shape,YY_train.shape,YY_test.shape)
    
    
        if param_grid is None:
            clf = Pipeline([
                ('normalize', Normalizer()),
                ('mpl',MLPRegressor(solver='adam', alpha=1e-5,hidden_layer_sizes=(50,50,50), random_state=42,
                                    activation='relu',
                                    max_iter=500))
            ]).fit(X=XX_train,y=YY_train) 
        else:
            clf = GridSearchCV(
                estimator=Pipeline([
                    ('normalize', Normalizer()),
                    ('mpl',MLPRegressor(alpha=1e-5,random_state=42,max_iter=100))
                ]),
                param_grid=param_grid,
                verbose=10,n_jobs=3
            ).fit(X=XX_train,y=YY_train)
        
        print("Model scores:")
        print(clf.score(XX_test,YY_test),clf.score(XX_train,YY_train)) 
    
        diff = clf.predict(XX_test) - YY_test
        sel = sample(range(YY_test.shape[0]),30)
        _ = plt.plot(YY_test[sel,:].transpose(),"r")
        _ = plt.plot(diff[sel,:].transpose(),"0.8")
    
        cld_data_transfer = clf.predict(clf_spectra)
        clf_data = {}
        clf_data["XX_train"],clf_data["XX_test"],clf_data["YY_train"],clf_data["YY_test"] = train_test_split(
            cld_data_transfer, clf_classes, test_size=0.3)
    
        return clf_data

.. code:: python

    def update_cB_parameters(smooth, classifiers_fk, classifiers_id,n_steps_random_search=3, smooth_search=(0,1,3),clf_functions_names=['ratio', 'difference', 'channel']):
        if None in (classifiers_fk, classifiers_id):
            clf_functions = get_clf_functions()
            res = []
            for ii in tqdm(range(n_steps_random_search)):
                classifiers_fk = [choice(clf_functions_names) for ii in range(5)]
                classifiers_id = [tuple(sample(range(clf_data["XX_train"].shape[1]),
                                               len(getargspec(clf_functions[fn]).args))) for fn in classifiers_fk]
    
                clf = ClassicalBayesianFit(
                    fit_method="chosen_one",
                    mk_clf=ToClassifierDef(
                        clf_functions=get_clf_functions(),
                        classifiers_id=classifiers_id,
                        classifiers_fk=classifiers_fk))
                res.append((clf.set(xx=clf_data["XX_train"],yy=clf_data["YY_train"],smooth=0.2,n_bins=25),classifiers_fk,classifiers_id))
    
            score, classifiers_fk, classifiers_id = sorted(res,key=lambda x:x[0],reverse=True)[0]
            print("best result:")
            print(score)
            print(classifiers_fk)
            print(classifiers_id)
    
        print(smooth)    
        if smooth is None:
            res_smoth = []
            for smooth in tqdm(np.linspace(*smooth_search)):
                clf = ClassicalBayesianFit(
                    fit_method="chosen_one",
                    mk_clf=ToClassifierDef(
                        clf_functions=get_clf_functions(),
                        classifiers_id=classifiers_id,
                        classifiers_fk=classifiers_fk))
                res_smoth.append((clf.set(xx=clf_data["XX_train"],yy=clf_data["YY_train"],smooth=smooth,n_bins=25),smooth))
            smooth = sorted(res_smoth,key=lambda x:x[0],reverse=True)[0][1]
            print(sorted(res_smoth,key=lambda x:x[0],reverse=True)[0])
            
        return smooth, classifiers_fk, classifiers_id

.. code:: python

    def write_to_file(smooth, classifiers_fk, classifiers_id,out_path):
       
        clf = ClassicalBayesianFit(
            fit_method="chosen_one",
            mk_clf=ToClassifierDef(
                clf_functions=get_clf_functions(),
                classifiers_id=classifiers_id,
                classifiers_fk=classifiers_fk))
        clf.set(xx=clf_data["XX_train"],yy=clf_data["YY_train"],smooth=smooth,n_bins=25)
    
        t1, t2 = __test__(clf,xx=clf_data["XX_test"],yy=clf_data["YY_test"]),__test__(clf,xx=clf_data["XX_train"],yy=clf_data["YY_train"])
        
        print(t1,t2)
        fn = ("cld_%s_smoth_%.2f_" % (tgt.replace("-","_"),smooth) + 
              "_".join([("%s" % fk) + len(ii)*"_%i" % ii for fk,ii in zip(classifiers_fk,classifiers_id)]) + 
              "_score_%.2f.h5" % t1)
        fn_out = path.join(out_path,fn)
        print(fn_out)
        
        
        for cl in [10,20,30,40,50,60]:
            print(cl,class_ids[cl],np.sum(clf.predict(clf_data["XX_test"][clf_data["YY_test"]==cl,:]) == cl) / (np.sum(clf_data["YY_test"]==cl)))
        write_classical_bayesian_to_hdf5_file(
            clf=clf,filename=fn_out,class_names=class_names,
            mask_legend=mask_legend,clf_to_col=clf_to_col,band_names=band_names)
        data = read_classical_bayesian_from_hdf5_file(fn_out)
        print(data.keys())   

Sampling From Database
======================

Now that polygons are recovered, we can perform a more sane sampling.
Proposal: \* Randomly select 200 polygons for each class and select up
to 200 spectra from each polygon. Use this as a balanced test sample. \*
For training, sample constant number of spectra from each polygon and
use as training data. This way, each polygon has the same weight or
impact on the training.

.. code:: python

    raise NotImplementedError("please implement above")


::


    ---------------------------------------------------------------------------

    NotImplementedError                       Traceback (most recent call last)

    <ipython-input-270-332ce82006ec> in <module>()
    ----> 1 raise NotImplementedError("please implement above")
    

    NotImplementedError: please implement above


Sentinel-2
==========

.. code:: python

    raise NotImplementedError("please implement, check other jupyter notebook")


::


    ---------------------------------------------------------------------------

    NotImplementedError                       Traceback (most recent call last)

    <ipython-input-271-9f385dcbee7e> in <module>()
    ----> 1 raise NotImplementedError("please implement, check other jupyter notebook")
    

    NotImplementedError: please implement, check other jupyter notebook


Derived Sensors
===============

Use a simple perceptron neural net to transfer spectra from Sentinel-2
to a given target sensor. Use a grid search for best parameters for each
sensor. Then, train a cloud mask. It might be necessary to change
features for each sensor to optimize results.

Landsat-4
=========

.. code:: python

    ref = "S2A"
    tgt = "Landsat-4"
    band_names = srfs[tgt]["bands"]
    out_path = "./"
    n_steps_random_search = 3
    smooth_search = (0,1,3)
    if True:
        param_grid={
                    "mpl__solver":['adam', 'lbfgs', 'sgd'],
                    "mpl__hidden_layer_sizes":[(50,50),(100,100),(50,50,50)],
                    "mpl__activation":['relu', 'tanh', 'logistic', 'identity'],
                }
        
        param_grid={
                    "mpl__solver":['adam'],
                    "mpl__hidden_layer_sizes":[(50,50),],
                    "mpl__activation":['relu',],
                }      
        
        smooth, classifiers_fk, classifiers_id = None, None, None
    else:
        param_grid = None
        smooth, classifiers_fk, classifiers_id = (
               1.0, ['ratio', 'difference', 'channel', 'ratio', 'channel'], [(2, 0), (3, 5), (4,), (3, 0), (1,)])
        
    clf_data = transfer_data_to(tgt=tgt,param_grid=param_grid)
    print(smooth, classifiers_fk, classifiers_id)
    smooth, classifiers_fk, classifiers_id = update_cB_parameters(smooth, classifiers_fk, classifiers_id,n_steps_random_search=n_steps_random_search, smooth_search=smooth_search)
    print(smooth, classifiers_fk, classifiers_id)
    write_to_file(smooth, classifiers_fk, classifiers_id,out_path)    

Landsat-5
=========

.. code:: python

    ref = "S2A"
    tgt = "Landsat-5"
    band_names = srfs[tgt]["bands"]
    out_path = "./"
    n_steps_random_search = 3
    smooth_search = (0,1,3)
    if True:
        param_grid={
                    "mpl__solver":['adam', 'lbfgs', 'sgd'],
                    "mpl__hidden_layer_sizes":[(50,50),(100,100),(50,50,50)],
                    "mpl__activation":['relu', 'tanh', 'logistic', 'identity'],
                }
        
        param_grid={
                    "mpl__solver":['adam', 'lbfgs'],
                    "mpl__hidden_layer_sizes":[(50,50),],
                    "mpl__activation":['relu',],
                }    
        
        smooth, classifiers_fk, classifiers_id = None, None, None
    else:
        param_grid = None
        smooth, classifiers_fk, classifiers_id = (
               0.5, ['channel', 'channel', 'ratio', 'channel', 'ratio'], [(5,), (1,), (5, 1), (4,), (4, 0)])
        
    clf_data = transfer_data_to(tgt=tgt,param_grid=param_grid)
    print(smooth, classifiers_fk, classifiers_id)
    smooth, classifiers_fk, classifiers_id = update_cB_parameters(smooth, classifiers_fk, classifiers_id,n_steps_random_search=n_steps_random_search, smooth_search=smooth_search)
    print(smooth, classifiers_fk, classifiers_id)
    write_to_file(smooth, classifiers_fk, classifiers_id,out_path)

Landsat-7
=========

.. code:: python

    ref = "S2A"
    tgt = "Landsat-7"
    band_names = srfs[tgt]["bands"]
    out_path = "./"
    n_steps_random_search = 3
    smooth_search = (0,1,3)
    if True:
        param_grid={
                    "mpl__solver":['adam', 'lbfgs', 'sgd'],
                    "mpl__hidden_layer_sizes":[(50,50),(100,100),(50,50,50)],
                    "mpl__activation":['relu', 'tanh', 'logistic', 'identity'],
                }
        smooth, classifiers_fk, classifiers_id = None, None, None
    else:
        param_grid = None
        smooth, classifiers_fk, classifiers_id = (
               1.00, ['difference', 'ratio', 'channel', 'ratio', 'channel'], [(2, 1), (1, 0), (5,), (4, 3), (5,)])
        
    clf_data = transfer_data_to(tgt=tgt,param_grid=param_grid)
    print(smooth, classifiers_fk, classifiers_id)
    smooth, classifiers_fk, classifiers_id = update_cB_parameters(smooth, classifiers_fk, classifiers_id,n_steps_random_search=n_steps_random_search, smooth_search=smooth_search)
    print(smooth, classifiers_fk, classifiers_id)
    write_to_file(smooth, classifiers_fk, classifiers_id,out_path)    

Landsat-8
=========

.. code:: python

    ref = "S2A"
    tgt = "Landsat-8"
    band_names = srfs[tgt]["bands"]
    out_path = "./"
    n_steps_random_search = 3
    smooth_search = (0,1,3)
    if True:
        param_grid={
                    "mpl__solver":['adam', 'lbfgs', 'sgd'],
                    "mpl__hidden_layer_sizes":[(50,50),(100,100),(50,50,50)],
                    "mpl__activation":['relu', 'tanh', 'logistic', 'identity'],
                }
        smooth, classifiers_fk, classifiers_id = None, None, None
    else:
        param_grid = None
        smooth, classifiers_fk, classifiers_id = (
               0.22, ['ratio', 'difference', 'difference', 'difference', 'difference'], [(6, 5), (4, 0), (0, 3), (5, 1), (3, 6)])
        
    clf_data = transfer_data_to(tgt=tgt,param_grid=param_grid)
    print(smooth, classifiers_fk, classifiers_id)
    smooth, classifiers_fk, classifiers_id = update_cB_parameters(smooth, classifiers_fk, classifiers_id,n_steps_random_search=n_steps_random_search, smooth_search=smooth_search)
    print(smooth, classifiers_fk, classifiers_id)
    write_to_file(smooth, classifiers_fk, classifiers_id,out_path)
