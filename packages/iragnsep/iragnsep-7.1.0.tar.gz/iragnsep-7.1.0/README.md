# iragnsep

iragnsep performs IR (i.e. 8--1000 microns) SED fits, separated into AGN and galaxy contributions, and measure host galaxy properties (e.g. SFRs) free of AGN contamination. The advantage of iragnsep is that, in addition to fitting observed broadband photometric fluxes, it also allows to incorporate IR spectra in the fits which, if available, greatly  improves the robustness of the galaxy-AGN separation. 

For the galaxy component iragnsep uses a library of galaxy templates built and presented in Bernhard et al. (in prep.). In terms of the AGN contribution, if the input dataset is a mixture of spectral and photometric data, iragnsep uses a combination of power-laws for the AGN continuum and some broad features for the silicate emission. If, instead, the dataset contains photometric data alone, the AGN contribution is accounted for by using the library of AGN templates presented in Bernhard et al. (in prep.).

The advanced fitting techniques used by iragnsep (i.e. MLE optimised with MCMC) combined with the powerful model comparison tests (i.e. AIC) allow iragnsep to provide a statistically robust interpretation of IR SEDs in terms of AGN–galaxy contributions, even when the AGN contribution is highly diluted by the host galaxy emission.

The aim of this README is to show how to use iragnsep. This document also contains important information such as limitations and cautions and the modules and functions which define iragnsep.

For a detailed description on the templates and fitting technique, see Bernhard et al. (in prep.).

Contacts: e.p.bernhard[at]sheffield.ac.uk

## Getting Started
These instructions should assist you in getting iragnsep running on your machine. iragnsep is written in python 3 and is available on PyPI.

### Prerequisites
iragnsep requires some non-standard libraries (dependencies) to run. These should automatically get installed when downloading and installing iragnsep via PyPi. If not, these can be manually installed using the pip3 command. The dependencies are as follow,

* [NumPy](https://numpy.org) - NumPy is the fundamental package for scientific computing with Python.
* [Matplotlib](https://matplotlib.org) - Matplotlib is a Python 2D plotting library.
* [Astropy](https://www.astropy.org) - The Astropy Project is a community effort to develop a common core package for Astronomy in Python and foster an ecosystem of inter-operable astronomy packages.
* [SciPy](https://www.scipy.org) - SciPy is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
* [pandas](https://pandas.pydata.org) - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
* [emcee](https://emcee.readthedocs.io/en/stable/#) - emcee is an MIT licensed pure-Python implementation of Goodman & Weare’s Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler.
* [Numba](http://numba.pydata.org) - Numba translates Python functions to optimised machine code at runtime using the industry-standard LLVM compiler library. Numba-compiled numerical algorithms in Python can approach the speeds of C or FORTRAN.

### Installation
We recommend to install iragnsep and its dependencies using pip,

```
pip3 install iragnsep
```
The project is also publicly available on bitbucket (GIT) at https://bitbucket.org/ebernhard/iragnsep/src/master/ .

## Quick start

In this section we show how to infer the SFR of the galaxy mrk1066 using iragnsep.

### Step 1: Get the data and the script

You can download the data at https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/. The file data_mrk1066.csv contains the Herschel fluxes of mrk1066, and the file data_mrk1066_spec.csv contains the Spitzer-IRS spectrum of mrk1066. The file main.py is the main script. Once downloaded, create a folder with all of these files.

### Step 2: Run the script

In a terminal simply cd to the folder that contains the files and run,

```
python3 main.py
```

iragnsep is now fitting mrk1066, first using a combination of the IRS spectrum and Herschel photometry, then using photometry only as if the IRS spectrum was not available. The user can open the file main.py which is commented and can be used as a template for future use of iragnsep.

### Step 3: Output

Once the fits are performed the plots and tables are generated and saved in the same folder. 

* **mrk1066_fitRes_spec.csv** - ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitRes_spec.csv)) contains the results of the fits for the 12 possible combinations of models considered by iragnsep. Each row corresponds to a specific model. This file contains the results of the fits performed on data which included the IRS spectrum. The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See section ** Description of the tables** for a full description.
* **mrk1066_fitResAll_spec.pdf** - ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitResAll_spec.pdf)) shows each of the 12 possible models fit to the data which included the IRS spectrum.
* **mrk1066_fitResBM_spec.pdf** -  ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitResBM_spec.pdf)) shows the best fit to the data which included the IRS spectrum. The best fit corresponds to a statistically weighted sum of all of the 12 different models.
* **mrk1066_fitRes_photo.csv** - ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitRes_photo.csv)) contains the results of the fits for the 18 possible combinations of templates. Each row corresponds to a specific model. This file contains the results of the fits performed in photometry only (i.e. the IRS spectrum was replaced by photometry). The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See the section ** Description of the tables** for a full description.
* **mrk1066_fitResAll_photo.pdf** - ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitResAll_photo.pdf)) shows each of the 18 models fit to the photometric data.
* **mrk1066_fitResBM_photo.pdf** - ([Available here](https://bitbucket.org/ebernhard/iragnsep/src/master/Mrk1066/mrk1066_fitResBM_photo.pdf)) shows the best fit to the photometric data. The best fit corresponds to a statistically weighted sum of all of the 18 different models..

## Preparing your data
As this is the first release of iragnsep it is important to make sure that the input data are compatible with the code. Future versions will allow more flexibility in the format of the input data. The main input are the wavelengths of the SED (or combined spectrum and photometry) and the corresponding fluxes and their uncertainties. Here is a (non-exhaustive) check list of points that are required to ensure a robust behaviour of iragnsep.

* the wavelengths are in microns, the fluxes and the uncertainties are in Jy.
* the vector wavelength is in monotonically increasing order.
* their is no negative or undefined (e.g. nan) values in the fluxes and their uncertainties (upper-limits can be passed via the keywords UL and ULphot).
* if using iragnsep with a combination of a spectrum and photometry, make sure that no photometric points are overlapping with the spectral data (e.g. IRS spectra and MIPS 24 micron would be overlapping).
* from practice, a good value for Nmc (the number of steps in the MCMC) is at least 10000 steps.
* do not forget to set the redshift of the source using the keyword z.
* for the photometric version, avoid photometry below roughly 5 microns rest-frame as iragnsep has not been designed to account for emissions below this value (e.g. old stellar population and very host dust component).

Should you find anything non-intuitive missing from the above list, contact us at: e.p.bernhard[at]sheffield.ac.uk

## Description of the tables

The output of the fits can be saved using the keyword saveRes as shown in the main.py of the Quick Start example on mrk1066. In particular two types of tables can be generated whether using the version of the code with spectra or that of with photometry alone.

The table sourceName_fitRes_spec.csv (where sourceName is the name of the source passed by the user) is a comma separated values (CSV) table which contains the results of the fits performed on data which included spectra. Each table row corresponds to one of the 12 possible models considered by iragnsep. Columns are as follow,

* **tplName** - the name of the galaxy template [gal1_dust, gal2_dust, gal3_dust, gal4_dust, gal1_emp, gal2_emp].
* **AGNon** - if  0.0, the results are for a fit that does not contain any AGN contribution, while if 1.0 the results are for a fit that accounts for AGN contribution.
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum template and its uncertainties.
* **logNormGal_PAH, elognNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN_PL, elogNormAGN_PL** - the overall normalisation of the continuum emission for AGN (combination of borken power-laws) and its uncertainties.
* **lBreak_PL, elBreak_PL** - the position of the main break for the AGN emission and its uncertainties.
* **alpha1_PL, ealpha1_PL** - the slope of the AGN power-law below 15 micron and its uncertainties.
* **alpha2_PL, ealpha2_PL** - the slope of the AGN power-law above 15 micron and below lbreak_PL and its uncertainties.
* **logNorm_Si11, elogNorm_Si11** - the log-normalisation of the silicate emission at 11 micron and its uncertainties.
* **logNorm_Si18, elogNorm_Si18** - the log-normalisation of the silicate emission at 18 micron and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **tau9p7** - the total extinction at 9.7 micron.
* **bestModelFlag** - a value of 1.0 indicates the best model.

The table sourceName_fitRes_photo.csv is a CSV table which contains the results of the fits performed on data with photometry alone. Each table row corresponds to one of the 18 possible models considered by iragnsep. Columns are as follow,

* **tplName_gal** - the name of the galaxy template [gal1_dust, gal2_dust, gal3_dust, gal4_dust, gal1_emp, gal2_emp].
* **AGNon** - if  0.0, the results are for a fit that does not contain any AGN contribution, while if 1.0 the results are for a fit that accounts for AGN contribution.
* **tplName_AGN** - the name of the AGN continuum template [AGN_A, AGN_B].
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum template and its uncertainties.
* **logNormGal_PAH, elogNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN, elogNormAGN** - the log-normalisation of the AGN continuum template and its uncertainties.
* **logNormSiem, elogNormSiem** - the log-normalisation of the silicate emission template (if included in the fit) and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **bestModelFlag** - a value of 1.0 indicates the best model.

## The templates

irasgnsep uses a library of templates for the galaxy and the AGN emission. Interested reader are referred to Bernhard et al. (in prep.) for a detailed description of the templates. The templates are available as a CSV table at: https://bitbucket.org/ebernhard/iragnsep/src/master/iragnsep/iragnsep_templ.csv . Columns are as follow,

* **lambda_mic** - the wavelength in micron spanning 1--1000 microns.
* **gal1_dust, egal1_dust** - the nuLnu of the first semi-empirical galaxy continuum template, normalised to Lir (i.e. integrated from 1-1000microns), and its uncertainties.
* **gal2_dust, egal2_dust** - the nuLnu of the second semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal3_dust, egal3_dust** -  the nuLnu of the third semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal4_dust, egal4_dust** -  the nuLnu of the fourth semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal1_emp, egal1_emp** -  the nuLnu of the first empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal2_emp, egal2_emp** -  the nuLnu of the second empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal_PAH, egal_PAH** -  the nuLnu of the PAH emission template, normalised to Lir, and its uncertainties.
* **AGN_Siem** -  the nuLnu of the silicate emission template, normalised to Lir, and its uncertainties.
* **AGN_A** -  the nuLnu of the first AGN continuum template, normalised to Lir, and its uncertainties.
* **AGN_B** - the nuLnu of the second AGN continuum template, normalised to Lir, and its uncertainties.

## iragnsep: modules

--

### run_all

--

Description:

The module run_all eases the use of iragnsep by running everything from the fits to the plots and give the possibility to save the result of the fits as CSV tables. run_all contains two functions. fitSpec performs everything on datasets which combine spectral and photometric data, and fitPhoto does the same but on photometry alone datasets.

----

**res, resBM = fitSpec(wavSpec, fluxSpec, efluxSpec,\
			wavPhot, fluxPhot, efluxPhot, \
			filters, \
			z = -0.01,\
			ULPhot = [],\
			obsCorr = True,\
			S9p7_fixed = -99.,\
			Nmc = 10000, pgrbar = 1, \
			Pdust = [10., 3.], PPAH = [9., 3.], Ppl = [-1., 3.], Pbreak = [1.603, 0.01], Pslope1 = [1., 2.], Pslope2 = [1., 2.], \
			Plsg = [-1., 3.], Pllg = [-1., 3.],\
			sourceName = 'NoName', pathTable = './', pathFig = './', \
			redoFit = True, saveRes = True)**


This function fits the observed SED when a spectrum is combined to photometric data. The observed wavelengths, fluxes and uncertainties on the fluxes are passed separately for the spectrum and the photometric data.
  
INPUT:

* **wavSpec** - observed wavelengths for the spectrum (in microns).
* **fluxSpec** - observed fluxes for the spectrum (in Jansky).
* **efluxSpec** - observed uncertainties on the fluxes for the spectrum (in Jansky).
* **wavPhot** - observed wavelengths for the photometry (in microns).
* **fluxPhot** - observed fluxes for the photometry (in Jansky).
* **efluxPhot** - observed uncertainties on the fluxes for the photometry (in Jansky).
* **filters** - name of the photometric filters corresponding to the observed photometry passed in wavPhot.

OUTPUT:

* **res_fit** - dataframe containing the results of all the possible fits.
* **res_fitBM** - dataframe containing the results of the best fit only.

KEYWORDS:
    
* **z** - redshift of the source. Default = 0.01.
* **ULPhot** - vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
* **obsCorr** - if set to True, iragnsep attempt to calculate the total silicate absorption at 9.7micron, and to correct the observed fluxes for obscuration. Default = True
* **S9p7_fixed** - can be used to pass a fixed value for the total silicate absorption at 9.7 micron. Default = -99.
* **Nmc** - numer of MCMC run. The final chain discards the first 20% of the Nmc steps as burnin and a thinning of 10 is applied. Default = 10000.
* **pgrbar** - if set to 1, displays a progress bar while fitting the SEDs. Default = 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.], ([mean, std dev]).
* **PPAH** - normal prior on the log-normalisation of the PAH template. Default = [9., 3.].
* **Ppl** - normal prior on the log-normalisation of the AGN continuum (defined at 10 micron). Default = [-1., 3.].
* **Pbreak** - normal prior on lbreak, the position of the log-break. Default = [1.6, 0.01].
* **Pslope1** - normal prior on alpha1, the slope of the first power-law defined between 1--15 microns. Default = [1., 2.].
* **Pslope2** - normal prior on alpha2, the slope of the second power-law defined between 15-lbreak microns. Default = [1., 2.].
* **Plsg** - normal prior on the log-normalisation of the silicate emission at 11micron. Default = [-1., 3.].
* **Pllg** - normal prior on the log-normalisation of the silicate emission at 18micron. Default = [-1., 3.].
* **sourceName** - name of the source. Default = 'NoName'.
* **pathTable** - if saveRes is set to True, the tables containing the results of the fits will be saved at the location pathTable. Default = './'.
* **pathFig** - if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
* **redoFit** - if set to True, re-performs the fits. Otherwise, find the table saved at pathTable and reproduces the analysis and the figures only. Default = True.
* **saveRes** - if set to True, the tables containing the results of the fits, as well as the figures are saved. Default = True.

----

**res, resBM = fitPhoto(wav, flux, eflux,\
			 filters, \
			 z = -0.01,\
			 UL = [], \
			 Nmc = 10000, pgrbar = 1, \
			 NoSiem = False, \
			 Pdust = [10., 3.], PPAH = [9., 3.], PnormAGN = [10., 3.], PSiEm = [10., 3.], \
			 sourceName = 'NoName', pathTable = './', pathFig = './', \
			 redoFit = True, saveRes = True, NOAGN = False)**

This function fits the observed photometric SED.

INPUT:

* **wav** - observed wavelengths (in microns).
* **fluxSpec** - observed fluxes (in Jansky).
* **efluxSpec** - observed uncertainties on the fluxes (in Jansky).
* **filters** - name of the photometric filters corresponding to the observed photometry passed in wav.

OUTPUT:

* **res_fit** - dataframe containing the results of all the possible fits.
* **res_fitBM** - dataframe containing the results of the best fit only.

KEYWORDS:

**z** - redshift of the source. Default = 0.01.
**UL** - vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
**Nmc** - * **Nmc** - numer of MCMC run. The final chain discards the first 20% of the Nmc steps as burnin and a thining of 10 is applied. Default = 10000.
**pgrbar** - if set to 1, display a progress bar while fitting the SED. Default = 1.
**NoSiem** - if set to True, no silicate emission template is included in the fit. Default = False.
**Pdust** - normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.], ([mean, std dev]).
**PPAH** - normal prior on the log-normalisation of the PAH template. Default = [9., 3.].
**PnormAGN** - normal prior on the log-normalisation of the AGN template. Default = [10., 3.].
**PSiem** - normal prior on the log-normalisation of the silicate emission template. Default = [10., 3.].
**sourceName** - name of the source. Default = 'NoName'.
**pathTable** - if saveRes is set to True, the tables containing the results of the fits will be saved at the location pathTable. Default = './'.
**pathFig** - if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
**redoFit** - if set to True, re-performs the fits. Otherwise, find the table saved at pathTable and reproduces the analysis and the figures only. Default = True.
**saveRes** - if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
**NOAGN** - if set to True, the AGN component is not included in the fits, Default = False.

----

--

### SEDanalysis

--

Description:

The module SEDanalysis is the module which runs the fits (yet see the **run_all** module for an easier use of iragnsep, including generating plots and tables). SEDanalysis contains two main functions. **runSEDspecFit** is for dataset which combines spectral and photometric fluxes, and **runSEDphotFit** is for dataset which contains photometric data only.

-- --

**dfRes = runSEDspecFit(wavSpec, fluxSpec, efluxSpec,\
				  wavPhot, fluxPhot, efluxPhot, filters, \
				  z = -0.01,\
				  ULPhot = [], \
				  obsCorr = True,\
				  S9p7_fixed = -99., \
				  Nmc = 10000, pgrbar = 1, \
				  Pdust = [10., 3.], PPAH = [9., 3.], Ppl = [-1., 3.], Pbreak = [1.603, 0.01], Pslope1 = [1., 2.], Pslope2 = [1., 2.], \
				  Plsg = [-1., 3.], Pllg = [-1., 3.],\
				  templ = '')**

This function fits the observed SED when a spectrum is combined to photometric data. The observed wavelengths, fluxes and uncertainties on the fluxes are passed separately for the spectrum and the photometric data.

INPUT:

* **wavSpec** - observed wavelengths for the spectrum (in microns).
* **fluxSpec** - observed fluxes for the spectrum (in Jansky).
* **efluxSpec** - observed uncertainties on the fluxes for the spectrum (in Jansky).
* **wavPhot** - observed wavelengths for the photometry (in microns).
* **fluxPhot** - observed fluxes for the photometry (in Jansky).
* **efluxPhot** - observed uncertainties on the fluxes for the photometry (in Jansky).
* **filters** - name of the photometric filters corresponding to the observed photometry passed in wavSpec.

OUTPUT:

* **dfRes** - dataframe containing the results of all the possible fits.

KEYWORDS:
    
* **z** - redshift of the source. Default = 0.01.
* **ULPhot** - vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
* **obsCorr** - if set to True, iragnsep attempt to calculate the total silicate absorption at 9.7micron, and to correct the observed fluxes for obscuration. Default = True
* **S9p7_fixed** - can be used to pass a fixed value for the total silicate absorption at 9.7 micron. Default = -99.
* **Nmc** - numer of MCMC run. The final chain discards the first 20% of the Nmc steps as burnin and a thining of 10 is applied. Default = 10000.
* **pgrbar** - if set to 1, displays a progress bar while fitting the SEDs. Default = 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.], ([mean, std dev]).
* **PPAH** - normal prior on the log-normalisation of the PAH template. Default = [9., 3.].
* **Ppl** - normal prior on the log-normalisation of the AGN continuum (defined at 10 micron). Default = [-1., 3.].
* **Pbreak** - normal prior on lbreak, the position of the log-break. Default = [1.6, 0.01].
* **Pslope1** - normal prior on alpha1, the slope of the first power-law defined between 1--15 microns. Default = [1., 2.].
* **Pslope2** - normal prior on alpha2, the slope of the second power-law defined between 15-lbreak microns. Default = [1., 2.].
* **Plsg** - normal prior on the log-normalisation of the silicate emission at 11micron. Default = [-1., 3.].
* **Pllg** - normal prior on the log-normalisation of the silicate emission at 18micron. Default = [-1., 3.].
* **templ** - pass the templates to be used. If none, use the library of templates from Bernhard et al. (in prep.). Default: ''.

-- --

**dfRes = runSEDphotFit(lambdaObs, fluxObs, efluxObs, \
				  filters, \
				  z = 0.01, \
				  UL = [], \
				  Nmc = 10000, pgrbar = 1, \
				  NoSiem = False, \
				  Pdust = [10., 13], PPAH = [9., 3.], PnormAGN = [10., 3.], PSiEm = [10., 3.], \
				  templ = '', NOAGN = False)**

This function fits the observed photometric SED.

INPUT:

**lambdaObs** - observed wavelengths (in microns).
**fluxObs** - observed fluxes (in Jansky).
**efluxObs** - observed uncertainties on the fluxes (in Jansky).
**filters** - name of the photometric filters to include in the fit.

OUTPUT:

**dfRes** - dataframe containing the results of all the possible fits.

KEYWORDS:

* **z** - redshift of the source. Default = 0.01.
* **ULPhot** - vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
* **obsCorr** - if set to True, iragnsep attempt to calculate the total silicate absorption at 9.7micron, and to correct the observed fluxes for obscuration. Default = True
* **tau9p7_fixed** - can be used to pass a fixed value for the total silicate absorption at 9.7 micron. Default = -99.
* **Nmc** - numer of MCMC run. The final chain discards the first 20% of the Nmc steps as burnin and a thining of 10 is applied. Default = 10000.
* **pgrbar** - if set to 1, displays a progress bar while fitting the SEDs. Default = 1.
* **Pdust** - normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.], ([mean, std dev]).
* **PPAH** - normal prior on the log-normalisation of the PAH template. Default = [9., 3.].
* **Ppl** - normal prior on the log-normalisation of the AGN continuum (defined at 10 micron). Default = [-1., 3.].
* **Pbreak** - normal prior on lbreak, the position of the log-break. Default = [1.6, 0.01].
* **Pslope1** - normal prior on alpha1, the slope of the first power-law defined between 1--15 microns. Default = [1., 2.].
* **Pslope2** - normal prior on alpha2, the slope of the second power-law defined between 15-lbreak microns. Default = [1., 2.].
* **Plsg** - normal prior on the log-normalisation of the silicate emission at 11micron. Default = [-1., 3.].
* **Pllg** - normal prior on the log-normalisation of the silicate emission at 18micron. Default = [-1., 3.].
* **templ** - pass the templates to be used. If none, use the library of templates from Bernhard et al. (in prep.). Default: ''.
* **NOAGN** - if set to True, the AGN contribution is not included in the fits. Default: False.

-- --

--


### toolplot

--

Description:

The module toolplot generates plots based on the results of the fits. toolplot contains two functions. plotFitSpec generates a plot showing all of the possible combinations of models and generates a plot showing that of the best model for dataset which combines spectral and photometric data. plotFitPhoto is the same as plotFitSpec but for photometric datasets.

-- --

**plotFitSpec(df, wavSpec, fluxSpec, efluxSpec, wavPhot, fluxPhot, efluxPhot, UL = np.array([]), pathFig = './', sourceName = 'NoName', templ = '', z = 0.01, saveRes = True)**

This function plots the results of the fits for data which contain spectral + photometric fluxes.

INPUT:

**df** - data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDspecFit.
**wavSpec** - observed wavelengthts for the spectrum (in microns).
**fluxSpec** - observed fluxes for the spectrum (in Jansky).
**efluxSpec** - observed uncertainties on the fluxes for the spectrum (in Jansky).
**wavPhot** - observed wavelengths for the photometry (in microns).
**fluxPhot** - observed fluxes for the photometry (in Jansky).
**efluxPhot** - observed uncertainties on the fluxes for the photometry (in Jansky).

KEYWORDS:

**z** - redshift of the source. Default = 0.01.
**UL** - vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
**sourceName** - name of the source. Default = 'NoName'.
**pathFig** - if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
**saveRes** - if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
**templ** - pass the templates that have been used in the fits.

-- --

**plotFitPhoto(df, wav, flux, eflux, UL = np.array([]), pathFig = './', sourceName = 'NoName', templ = '', z = 0.01, saveRes = True)**
	
This function plots the results of the fits for photometric data.

INPUT:

**df** - data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDphotFit.
**wav** - observed wavelengthts (in microns).
**flux** - observed fluxes (in Jansky).
**eflux** - observed uncertainties on the fluxes (in Jansky).

KEYWORDS:

**z** - redshift of the source. Default = 0.01.
**UL** - vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
**sourceName** - name of the source. Default = 'NoName'.
**pathFig** - if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
**saveRes** - if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
**templ** - set the templates that have been used in the fits.

-- --

--

### func

--

Description:

The module func contains the functions used to run the fits, the best model selection and the analysis.

-- --

**get_prop(df, echar, z = 0.01, specOn = True, templ = '')**

This function calculates the IR properties of the AGN and their hosts.

INPUT:

**df** - data-frame containing the results from the fits (i.e. optimised parameters) as returned by SEDanalysis.
**echar** - characteristic uncertainties to calculate the uncertainties on the parameters.
    
OUTPUT:

**loglum_hostIR** - the host IR (8--1000microns) log-luminosity free of AGN contamination (Lsun).
**eloglum_hostIR** - uncertainties on loglum_hostIR.
**loglum_hostMIR** - the host IR (5--35microns) log-luminosity free of AGN contamination (Lsun).
**eloglum_hostIR** - uncertainties on loglum_hostMIR.
**loglum_hostFIR** - the host IR (40--1000microns) log-luminosity free of AGN contamination (Lsun).
**eloglum_hosFIR** - uncertainties on loglum_hostFIR.
**loglum_AGNIR** - the AGN IR log-luminosity free of host contamination (Lsun).
**loglum_AGNMIR** - the AGN MIR log-luminosity free of host contamination (Lsun).
**loglum_AGNFIR** - the AGN FIR log-luminosity free of host contamination (Lsun).
**AGNfrac_IR** - the AGN fraction in the IR.
**AGNfrac_MIR** - the AGN fraction in the MIR.
**AGNfrac_FIR** - the AGN fraction in the FIR.
**SFR** - the SFR of the galaxy free of AGN contamination.
**eSFR** - the uncertainties on SFR.
**wSFR** - the SFR of the galaxy free of AGN contamination weighted by its Akaike weight.
**ewSFR** - the uncertainties on wSFR.

KEYWORDS:

**z** - redshift
**specOn** - set to True if the data contain a spectrum in addition to the photometry.
**templ** - set the templates that have been used in the fits.

-- --

**basictests(wavSpec, fluxSpec, efluxSpec, wavPhot, fluxPhot, efluxPhot, filters, z, specOn = True)**

This function runs some basic tests prior to run the main fitting code.

INPUT:

**wavSpec** - observed wavelengths for the spectrum (in microns).
**fluxSpec** - observed fluxes for the spectrum (in Jansky).
**efluxSpec** - observed uncertainties on the fluxes for the spectrum (in Jansky).
**wavPhot** - observed wavelengths for the photometry (in microns).
**fluxPhot** - observed fluxes for the photometry (in Jansky).
**efluxPhot** - observed uncertainties on the fluxes for the photometry (in Jansky).
**filters** - name of the photometric filters to include in the fit.
**z** - redshift.

KEYWORDS:

**specOn** - set to True if the data contain a spectrum in addition to the photometry.

-- --

**exctractBestModel(logl, k, n, corrected = True)**

This function extracts the best model and calculates the Akaike weights based on the log-likelihood returned by the fits.

INPUT:

**logl** - log-likelihood returned by the fits.
**k** - number of free parameters.
**n** - number of data points.

OUTPUTS:

**bestModelInd** - the index of the best model fit.
**Awi** - Akaike weights of each of the models, with respect to the best model.

KEYWORDS:

**corrected** - if set to True, calculates the corrected AIC for small number of data points.

-- -- 

**nuLnuToFnu(spec_wav, nuLnu, z)**

This function calculates the observed flux from nuLnu.

INPUT:

**spec_wav** - rest-wavelengths (in microns).
**nuLnu** -  nuLnu.
**z** - redshift.

OUTPUT:

**Fnu** - observed flux on Earth of the source located at redshift z (in Jansky).

-- --

**getFluxInFilt(filt_wav, filt_QE, spec_wav, nuLnu, z):**

This function calculates the synthetic flux in a given filter and at a given redshift from a source with luminosity nuLnu.

INPUT:

**filt_wav** - passband of the filter.
**filt_QE** - quantum efficient of the filter.
**spec_wav** - rest-wavelengths (in microns).
**nuLnu** - nuLnu.
**z** - redshift.
 
OUTPUT:

**flux_Obs** - observed flux on Earth of the source located at redshift z with luminosity nuLnu (in Jansky).

-- --

**logldet(ym, ydat, eydat, wei):**

This function calculates the log-likelihood of detected data.

INPUT:

**ym** - model values.
**ydat** - observed values.
**eydat** - observed uncertaities.
**wei** - weights of the data points.

OUTPUT:

**logl** - log-likelihood of the model.

-- --

**erf_approx(x)**

This function calculates an approximation of the error function.

INPUT:

**x** - x values to which the error function is calculated at.

OUTPUT:

**erf_approx_eval** - approximate value of the error function.

-- --

**loglUL(ym, ydat)**

This function calculates the log-likelihood of undetected data.

INPUT:

**ym** - model values.
**ydat** - observed values.

OUTPUT:

**logl** - log-likelihood of the model.

-- --

**Gauss_jit(x, mu, sigma)**

This function calculates a Gaussian normalised to its maximum.

INPUT:

**x** - x-values.
**mu** - mean.
**sigma** - standard deviation.

OUTPUT:

**Bnu** Gaussian evaluated at x, normalised to its maximum.

-- --

**AGNmodel_firstPL_jit(x, lambdab, alpha1, alpha2, s)**

This function calculates the first broken power-law of the AGN model.

INPUT:

**x** - x-values.
**lambdab** - position of the break.
**alpha1** - slope of the first power-law.
**alpha2** - slope of the second power-law.
**s** - sharpness parameter for the break between alpha1 and alpha2. 

OUTPUT:

**Bnu** - corresponding broken power law evaluated at x, and normalised at 10 microns.

-- --

**AGNmodel_jit(x, lambdab1, lambdab2, alpha1, alpha2, alpha3)**

This function calculates the second broken power-law of the AGN model.

INPUT:

**x** - x-values.
**lambdab1** - position of the break for the first broken power law.
**lambdab2** - position of the break for the second broken power law.
**alpha1** - slope of the first power-law.
**alpha2** - slope of the second power-law.
**alpha2** - slope of the third power-law.

OUTPUT:

**Bnu** - corresponding double-broken power law evaluated at x, and normalised at 10 microns.

-- --

**KVTextinctCurve(lambda_obs)**

This function calculates the extinction curve from Kemper et al. (2004).

INPUT:

**lambda_obs** - observed wavelengths.

OUTPUT:

**tau_return** - absorption coefficient tau per wavelength.

-- --

**drude(x, gamma_r, lambda_r, normed = True)**

This function calculates a Drude profile.

INPUT:

**x** - x-values.
**gamma_r** - central wavelengths.
**lambda_r** - fractional FWHM.

OUTPUT:

**drudeVal** - the Drude profile evaluated at x.

KEYWORDS:

**normed** - if set to True, normalise to the maximum value.

-- -- 

obsC(wavRest, flux, eflux):

This function calculates the total obscuration at 9.7micron.

INPUT:

**wavRest** -rest-wavelength.
**flux** - observed fluxes.
**eflux** - uncertainties on the observed fluxes.

OUTPUT:

**_tau9p7** - the total obscuration at 9.7micron.

-- --

--

### classes

--

The module classes contains one class called 'modelToSED' which calls various functions to return the photometric point at a given wavelengths in a given filters for a model nuLnu. The available filters are as follow:

* **IRAC1** - Spitzer IRAC, 3.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC2** - Spitzer IRAC, 4.5 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC3** - Spitzer IRAC, 5.8 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC4** - Spitzer IRAC, 8.0 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **WISE_W1** - WISE, 3.4 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W2** - WISE, 4.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W3** - WISE, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W4** - WISE, 22 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **IRAS12** - IRAS, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS60** - IRAS, 60 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS100** - IRAS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **MIPS24** - Spitzer MIPS, 24 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS70** - Spitzer MIPS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS160** - Spitzer MIPS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **PACS70** - Herschel PACS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS100** - Herschel PACS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS160** - Herschel PACS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **SPIRE250ps** - Herschel SPIRE, 250 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE350ps** - Herschel SPIRE, 350 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE500ps** - Herschel SPIRE, 500 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE

Note: to add filter please contact e.p.bernhard[at]sheffield.ac.uk.

-- --

## Cautionary notes

As this is the first version of iragnsep we suggest the user to carefully check results, and to report anything that is possibly a bug. To do this, please contact us at: e.p.bernhard[at]sheffield.ac.uk.

The templates and models built for iragnsep are based on observations out to z=0.3. We have tested these on photometry of galaxies in the COSMOS field at higher redshifts, and the results appear to be reliable. However, there is no formal proof, and we suggest that the user carefully check results for these sources.

The templates have been derived on moderate luminosity AGNs 41.6 erg/s<Log10(Lx2-10kev)<45.2 erg/s. As a consequence, using iragnsep for, let's say, bright QSOs is at the User's own risks. We stress however that our AGN templates are in agreement with AGN templates for quasars.

## Future work

Future version will allow a more flexible input for the observed data. In addition it will be possible for the user to choose a complete different set of templates, if necessary.

For this version we use Numba to speed up the code. This python dependency pre-compiles the code allowing iragnsep to run faster. Using Numba, we have sped up iragnsep by a factor of 10. Since MCMC are time expensive, we are planning to further incorporate multi-threading for a possible increase in the speed.

So far we have tested iragnsep using data from the IRS spectra and  the Herschel photometry. We plan to test the possibility to incorporate other spectral data such as future JWST data.

## Versioning

We use three numbers for the versions defined as x.y.z. If only y and z are changed the output of iragnsep is unchanged and minor patches are applied. If x changes it means that major changes has been applied and results are likely to differ from the x-1 version.

The first released version starts at x=5.

## Authors

* **Emmanuel Bernhard** - *Initial work*
* James Mullaney
* Clive Tadhunter

The associated paper can be found at Bernhard et al. (in prep).

## Citation

Please cite Bernhard et al. (in prep) when using iragnsep.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details