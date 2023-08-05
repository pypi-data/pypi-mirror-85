import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from .func import *
from .classes import *
from matplotlib.lines import Line2D
from matplotlib import cm
from matplotlib.colors import ListedColormap

from matplotlib.font_manager import FontProperties
font0 = FontProperties(family = 'serif', variant = 'small-caps', size = 22)

import pdb
############################
## Plot all the results for all the possible fit. Tag the best model in blue.
############################
def plotFitSpec(df, wavSpec, fluxSpec, efluxSpec,\
				wavPhot, fluxPhot, efluxPhot, \
				UL = np.array([]), pathFig = './', \
				sourceName = 'NoName', templ = '', z = 0.01, saveRes = True, ExtCurve = 'iragnsep'):
	

	"""
    This function plots the results of the fits for data which contain spectral + photometry fluxes.
    ------------
    :param df: data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDspecFit.
    :param wavSpec: observed wavelengthts for the spectrum (in microns).
    :param fluxSpec: observed fluxes for the spectrum (in Jansky).
    :param efluxSpec: observed uncertainties on the fluxes for the spectrum (in Jansky).
    :param wavPhot: observed wavelengths for the photometry (in microns).
    :param fluxPhot: observed fluxes for the photometry (in Jansky).
    :param efluxPhot: observed uncertainties on the fluxes for the photometry (in Jansky).
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword UL: vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
  	:keyword sourceName: name of the source. Default = 'NoName'.
	:keyword pathFig: if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
	:keyword saveRes: if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
	:keyword templ: set the templates that have been used in the fits.
	------------
    :return 0
    """
	
	path_iragnsep = os.path.dirname(iragnsep.__file__)

    # concatenate the spectral and photo fluxes
	flux = np.concatenate([fluxSpec, fluxPhot])

	# define the upper limits if not.
	if len(UL) == 0.:
		UL = np.zeros(len(wavPhot))

	# define the templates to Bernhard+20 if not.
	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the name of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_PAH = []
	for key in keys:
		if str(key).startswith('gal'):
			if str(key).endswith('PAH') == False:
				nameTempl_gal.append(key)
			else:
				nameTempl_PAH.append(key)

	# Test that we have templates for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')
	
	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic'].values
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# Open 2 figures, 1 for all the possible fits and 1 for the best weighted average model.
	fig1, axs1 = plt.subplots(2,len(nameTempl_gal), sharex = True, sharey = True, figsize = (37, 12))
	fig1.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.06, right = 0.99, bottom = 0.10, top = 0.95)
	axs1 = axs1.ravel()

	fig2, axs2 = plt.subplots(figsize = (11, 8))
	fig2.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.15, right = 0.95, bottom = 0.15, top = 0.95)
	axs2.tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
	axs2.tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

	# Loop on all the possible combinations of models
	count = 0
	for i in range(0, len(df)):
		obj = df.iloc[i]

		# Extract the optimised best parameters and their uncertainties
		normDust = 10**obj['logNormGal_dust']
		nuLnuDust = normDust * templ[obj['tplName']].values
		enuLnuDust = normDust * templ['e'+obj['tplName']].values

		normPAH = 10**obj['logNormGal_PAH']
		nuLnuPAH = normPAH * templ['gal_PAH'].values
		enuLnuPAH = normPAH * templ['egal_PAH'].values

		# Add the extinction if measured
		_tau9p7 = obj['tau9p7']
		if _tau9p7 > 0.:

			EC_wav, EC_tau = getExtCurve(ExtCurve)
			tau = np.interp(wavTempl, EC_wav, EC_tau)* _tau9p7
			extCorr = (1 - np.exp(-tau))/tau

			EC_wav, EC_tau = getExtCurve('PAHfit')
			tau = np.interp(wavTempl, EC_wav, EC_tau)* _tau9p7
			extCorr_AGN = (1 - np.exp(-tau))/tau

		else:

			extCorr = 1.
			extCorr_AGN = 1.

		# Differential obscured galaxy emission
		nuLnuGal = nuLnuDust * extCorr + nuLnuPAH
		enuLnuGal = np.sqrt((enuLnuDust * extCorr)**2. + enuLnuPAH**2.)

		# Calculate the observed flux, affected by attenuation
		FnuGal = nuLnuToFnu(wavTempl, nuLnuGal, z)
		eFnuGal = nuLnuToFnu(wavTempl, enuLnuGal, z)

		# Define the AGN contribution
		if obj['AGNon'] == 1:
			
			modelPL = 10**(obj['logNormAGN_PL']) * contmodel_jit(wavTempl*(1.+z), 20.*(1.+z), obj['lBreak_PL']*(1.+z), obj['alpha1'], obj['alpha2'], -3.5)
			modelSi10 = 10**(obj['logNorm_Si10']) * Simodel_jit(wavTempl*(1.+z), 10.3*(1.+z), 12., -3.5, 3.)
			modelSi18 = 10**(obj['logNorm_Si18']) * Simodel_jit(wavTempl*(1.+z), 16.5*(1.+z), 9., -2.5, 1.)

			FnuAGN = (modelPL + modelSi10 + modelSi18) * extCorr_AGN

			FnuTot = FnuGal + FnuAGN
		else:
			FnuTot = FnuGal

		# Figure with all the fits.
		o = np.where(UL < 1.)[0]
		axs1[count].errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = efluxPhot[o], fmt = '.', color = '#292F33', alpha = 1.0, label = 'Observed SED')
		o = np.where(UL > 0.)[0]
		axs1[count].errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = fluxPhot[o]/3., fmt = '.', color = '#292F33', alpha = 1.0, label = '_no_label_', uplims = True)
		axs1[count].errorbar(wavSpec/(1.+z), fluxSpec, yerr = efluxSpec, fmt = '.', color = '#292F33', alpha = 1.0, label = '_no_label_')

		if obj['AGNon'] == 1:
			axs1[count].plot(wavTempl, FnuGal, '--', color = '#66757F', label = 'Galaxy comp. ('+obj['tplName']+')')
			axs1[count].plot(wavTempl, FnuAGN, '-.', color = '#66757F', label = 'AGN comp. (full model)')
			# axs1[count].plot(wavTempl, modelPL*extCorr_AGN, '.', color = '#66757F', label = 'Si 11')
			# axs1[count].plot(wavTempl, modelSi10*extCorr_AGN, '.', color = '#66757F', label = 'Si 18')
			# axs1[count].plot(wavTempl, modelSi18*extCorr_AGN, '.', color = '#66757F', label = 'Cont.')
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 10)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 10)
		else:
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total ('+obj['tplName']+')', errorevery = 10)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total ('+obj['tplName']+')', errorevery = 10)


		axs1[count].set_xscale('log')
		axs1[count].set_yscale('log')
		axs1[count].set_xlim([3./(1.+z), 800./(1.+z)])
		axs1[count].set_ylim([min(flux)/10., max(flux)*20.])
		axs1[count].set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', fontsize = 28)
		if (count == 0) or (count == len(nameTempl_gal)):
			axs1[count].set_ylabel(r'Flux (Jy)', fontsize = 28)
		
		if round(obj['Aw']*100.) > 50.:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = '#ff4d4d')
		else:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = 'k')
		axs1[count].tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
		axs1[count].tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')
		axs1[count].legend(frameon = False, fontsize = 16, ncol = 1)
		count += 1

		# Best model Figure
		if obj['Aw'] > 0.1:
			if obj['AGNon'] == 1:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName']+' + AGN ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw']/2.)				
			else:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName']+' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw']/2.)

		try:
			FnuTot_Aw += FnuTot * obj['Aw']
			eFnuTot_Aw += (eFnuGal*obj['Aw'])**2.
			FnuGal_Aw += FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw += FnuAGN * obj['Aw']
		except:
			FnuTot_Aw = FnuTot * obj['Aw']
			eFnuTot_Aw = (eFnuGal * obj['Aw'])**2.
			FnuGal_Aw = FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw = FnuAGN * obj['Aw']
			else:
				FnuAGN_Aw = FnuGal_Aw * 0.
		# pdb.set_trace()

	axs2.errorbar(wavTempl, FnuTot_Aw, yerr = np.sqrt(eFnuTot_Aw), fmt = '-', color = 'k', elinewidth = 0.5, linewidth = 3, label = 'Best weighted fit [Total]',\
			 ecolor = 'k', alpha = 0.4, errorevery = 3)
	axs2.plot(wavTempl, FnuGal_Aw, '--', color = '#E94B3C', \
						 linewidth = 2, label = 'Best weighted fit [Galaxy]', alpha = 0.7)
	axs2.plot(wavTempl, FnuAGN_Aw, '-.', color = '#6395F2', \
						 linewidth = 2, label = 'Best weighted fit [AGN]', alpha = 0.7)

	o = np.where(UL < 1.)[0]
	axs2.errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = efluxPhot[o], fmt = 'o', color = '#292F33', alpha = 0.9, label = 'Observed Photometry', mfc = 'none', mew = 1, ms = 10)

	o = np.where(UL > 0.)[0]
	axs2.errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = fluxPhot[o]/5., fmt = 'o', color = '#292F33', alpha = 0.9, label = '_no_label_', uplims = True, mfc = 'none', mew = 1, ms = 10)

	axs2.errorbar(wavSpec/(1.+z), fluxSpec, yerr = efluxSpec, fmt = '.', color = '#292F33', alpha = 0.9, label = 'Observed Spectrum')

	axs2.set_xscale('log')
	axs2.set_yscale('log')
	axs2.set_xlim([3./(1.+z), 800./(1.+z)])
	axs2.set_ylim([min(flux)/5., max(flux)*10.])
	axs2.set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', FontProperties = font0)
	axs2.set_ylabel(r'Flux (Jy)', FontProperties = font0)
	axs2.legend(frameon = False, fontsize = 16, ncol = 2)

	# If saveRes is True, then save the figures to the location specified in pathFig.
	if saveRes == True:
		fig1.savefig(pathFig+sourceName+'_fitResAll_spec.pdf')
		fig2.savefig(pathFig+sourceName+'_fitResBM_spec.pdf')
	else:
		plt.show()
	plt.close('all')


############################
## Plot all the results for all the possible fit. Tag the best model in blue.
############################
def plotFitPhoto(df, wav, flux, eflux, UL = np.array([]), pathFig = './', sourceName = 'NoName', templ = '', z = 0.01, saveRes = True, NOAGN = False, \
				 ExtCurve = 'iragnsep'):
	
	"""
    This function plots the results of the fits for photometric data.
    ------------
    :param df: data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDspecFit.
    :param wav: observed wavelengthts (in microns).
    :param flux: observed fluxes (in Jansky).
    :param eflux: observed uncertainties on the fluxes (in Jansky).
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword UL: vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
  	:keyword sourceName: name of the source. Default = 'NoName'.
	:keyword pathFig: if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
	:keyword saveRes: if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
	:keyword templ: set the templates that have been used in the fits.
	------------
    :return 0
    """

    # Open the Bernhard+20 templates if not defined
	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the name of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_PAH = []
	nameTempl_AGN = []
	nameTempl_Siem = []
	for key in keys:
		if str(key).startswith('gal'):
			if str(key).endswith('PAH') == False:
				nameTempl_gal.append(key)
			else:
				nameTempl_PAH.append(key)
		if str(key).startswith('AGN') == True:
			if str(key).endswith('Siem') == True:
				nameTempl_Siem.append(key)
			else:
				nameTempl_AGN.append(key)

	# Test that we have template for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')
	if len(nameTempl_AGN) == 0:
		raise ValueError('The AGN template does not exist. The name of the column defining nuLnu for the AGN template needs to start with "AGN".')

	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic']
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# Open 2 figures, 1 for all the possible fits and 1 for the best weighted average model.
	fig1, axs1 = plt.subplots(4,6, sharex = False, sharey = True, figsize = (27, 18))
	fig1.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.06, right = 0.99, bottom = 0.10, top = 0.95)
	axs1 = axs1.ravel()
	axs1[21].axis("off")
	axs1[22].axis("off")
	axs1[23].axis("off")

	# legend on the first figure
	line1 = Line2D([], [], label='Observed SED', color='k', marker='o', markeredgecolor='k', markeredgewidth=1.5, markersize=10, mfc = 'None')
	line2 = Line2D([1], [1], label='Best fit (Total)', color='k', lw = 2)
	line3 = Line2D([1], [1], label='Galaxy', ls = '--', color='#66757F', lw = 2)
	line4 = Line2D([1], [1], label='AGN', ls = '-.', color='#66757F', lw = 2)
	axs1[20].legend(frameon = False, handles=[line1, line2, line3, line4], numpoints=1, bbox_to_anchor=(3., 0.1), loc='lower right', fontsize = 25, ncol = 2)

	fig2, axs2 = plt.subplots(figsize = (11, 8))
	fig2.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.15, right = 0.95, bottom = 0.15, top = 0.95)
	axs2.tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
	axs2.tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

	# Open a cmap for the AW
	cmap = cm.get_cmap('magma', 101)
	cmap = ListedColormap(cmap(np.linspace(0.05, 0.7, 101)))

	# Loop over all the model combinations of templates.
	count = 0
	for i in range(0, len(df)):
		# Plot with all the possible models.
		o = np.where(UL < 1.)[0]
		axs1[count].errorbar(wav[o]/(1.+z), flux[o], yerr = eflux[o], fmt = 'o', color = 'k', alpha = 1.0, label = 'Observed SED', mew = 1, mfc = 'None', ms = 10)
		o = np.where(UL > 0.)[0]
		axs1[count].errorbar(wav[o]/(1.+z), flux[o], yerr = flux[o]/3., fmt = 'o', color = 'k', alpha = 1.0, uplims = True, mew = 1, mfc = 'None', ms = 10)

		obj = df.iloc[i]

		# Add the exctinction if measured
		_tau9p7 = obj['tau9p7']
		if _tau9p7 > 0.:

			# Get the extinction curve 
			EC_wav, EC_tau = getExtCurve(ExtCurve)
			tau = np.interp(wavTempl, EC_wav, EC_tau)* _tau9p7
			extCorr = (1 - np.exp(-tau))/tau

			EC_wav, EC_tau = getExtCurve('PAHfit')
			tau_AGN = np.interp(wavTempl, EC_wav, EC_tau) * _tau9p7
			extCorr_AGN = ((1. - np.exp(-tau_AGN))/tau_AGN)

		else:

			extCorr = 1.
			extCorr_AGN = 1.

		# Exrract the optimised parameters and their uncertainties
		normDust = 10**obj['logNormGal_dust']
		nuLnuDust = (normDust * templ[obj['tplName_gal']].values)*extCorr
		enuLnuDust = (normDust * templ['e'+obj['tplName_gal']].values)*extCorr

		normPAH = 10**obj['logNormGal_PAH']
		nuLnuPAH = normPAH * templ['gal_PAH'].values
		enuLnuPAH = normPAH * templ['egal_PAH'].values

		nuLnuGal = nuLnuDust + nuLnuPAH
		enuLnuGal = np.sqrt(enuLnuDust**2. + enuLnuPAH**2.)

		# Calculate the observed model fluxes
		FnuGal = nuLnuToFnu(wavTempl, nuLnuGal, z).values
		eFnuGal = nuLnuToFnu(wavTempl, enuLnuGal, z).values

		# Define the optimised model AGN template
		if obj['AGNon'] == 1:
			normAGN = 10**obj['logNormAGN']
			nuLnuAGN = normAGN * templ[obj['tplName_AGN']].values
			enuLnuAGN_up = normAGN * templ['e'+obj['tplName_AGN']+'_up'].values
			enuLnuAGN_down = normAGN * templ['e'+obj['tplName_AGN']+'_down'].values
			
			normSi = 10**obj['logNormSiem']
			nuLnuSi = normSi * templ[nameTempl_Siem[0]].values
			enuLnuSi_up = normSi * templ['e'+nameTempl_Siem[0]+'_up'].values
			enuLnuSi_down = normSi * templ['e'+nameTempl_Siem[0]+'_down'].values
		
			FnuAGN =  nuLnuToFnu(wavTempl, nuLnuAGN + nuLnuSi, z) * extCorr_AGN

			FnuTot = FnuGal + FnuAGN

			enuLnuTot_up = np.sqrt(enuLnuDust**2. + enuLnuPAH**2. + enuLnuAGN_up**2. + enuLnuSi_up**2.)
			eFnuTot_up = nuLnuToFnu(wavTempl, enuLnuTot_up, z)
			enuLnuTot_down = np.sqrt(enuLnuDust**2. + enuLnuPAH**2. + enuLnuAGN_down**2. + enuLnuSi_down**2.)
			eFnuTot_down = nuLnuToFnu(wavTempl, enuLnuTot_down, z)

			axs1[count].plot(wavTempl, FnuGal, '--', color = '#66757F')
			axs1[count].plot(wavTempl, FnuAGN, '-.', color = '#66757F')
			axs1[count].plot(wavTempl, FnuTot, '-', c = cmap.colors[int(obj['Aw']*100.)], linewidth = 3, alpha = 0.7)

		else:
			FnuTot = FnuGal
			eFnuTot_up = eFnuGal
			eFnuTot_down = eFnuGal

			axs1[count].plot(wavTempl, FnuTot, 'k-', c = cmap.colors[int(obj['Aw']*100.)], linewidth = 3, alpha = 0.7)

		axs1[count].set_xscale('log')
		axs1[count].set_yscale('log')
		axs1[count].set_xlim([3./(1.+z), 800./(1.+z)])
		
		if NOAGN != True:
			axs1[count].set_ylim([min(flux)/5., max(flux)*5.])
		else:
			axs1[count].set_ylim([min(flux)/5., max(FnuTot)*5.])
		
		axs1[count].set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', fontsize = 28)
		
		if (count == 0) or (count == 6) or (count == 12) or (count == 18):
			axs1[count].set_ylabel(r'Flux (Jy)', fontsize = 28)
		
		axs1[count].text(10., min(flux)/4., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = cmap.colors[int(obj['Aw']*100.)])
		if obj['AGNon'] == 1:
			axs1[count].text(5./(1.+z), max(flux)*2.5, obj['tplName_gal']+'+'+obj['tplName_AGN'], fontsize = 25)
		else:
			axs1[count].text(5./(1.+z), max(flux)*2.5, obj['tplName_gal'], fontsize = 25)
		axs1[count].tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
		axs1[count].tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

		axs1[count].fill_between(wavTempl, FnuTot - eFnuTot_down, FnuTot + eFnuTot_up, color = '#bab8b1', alpha = 0.6)

		count += 1

		# Plots with the best model only.
		if obj['Aw'] > 0.05:
			if obj['AGNon'] == 1:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName_gal']+' + '+ obj['tplName_AGN'] + ' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw']/1.5)
			else:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName_gal']+' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw'])

			try:
				FnuTot_Aw += FnuTot * obj['Aw']
				eFnuTot_Aw += (eFnuGal*obj['Aw'])**2.
				FnuGal_Aw += FnuGal * obj['Aw']
				if obj['AGNon'] == 1:
					FnuAGN_Aw += FnuAGN * obj['Aw']
			except:
				FnuTot_Aw = FnuTot * obj['Aw']
				eFnuTot_Aw = (eFnuGal * obj['Aw'])**2.
				FnuGal_Aw = FnuGal * obj['Aw']
				if obj['AGNon'] == 1:
					FnuAGN_Aw = FnuAGN * obj['Aw']
				else:
					FnuAGN_Aw = FnuGal_Aw * 0.
			

	axs2.errorbar(wavTempl, FnuTot_Aw, yerr = np.sqrt(eFnuTot_Aw), fmt = '-', color = 'k', elinewidth = 0.5, linewidth = 2, label = 'Best weighted fit [Total]',\
				 ecolor = 'k', alpha = 1., errorevery = 3)
	axs2.plot(wavTempl, FnuGal_Aw, '--', color = '#E94B3C', \
						 linewidth = 2, label = 'Best weighted fit [Galaxy]', alpha = 0.8)
	axs2.plot(wavTempl, FnuAGN_Aw, '-.', color = '#6395F2', \
						 linewidth = 2, label = 'Best weighted fit [AGN]', alpha = 0.8)

	o = np.where(UL < 1.)[0]
	axs2.errorbar(wav[o]/(1.+z), flux[o], yerr = eflux[o], fmt = 'o', color = '#292F33', alpha = 0.9, label = 'Observed SED', mfc = 'none', mew = 1, ms = 10)

	o = np.where(UL > 0.)[0]
	axs2.errorbar(wav[o]/(1.+z), flux[o], yerr = flux[o]/5., fmt = 'o', color = '#292F33', alpha = 0.9, label = '_no_label_', uplims = True, mfc = 'none', mew = 1, ms = 10)

	axs2.set_xscale('log')
	axs2.set_yscale('log')
	axs2.set_xlim([3./(1.+z), 800./(1.+z)])
	if NOAGN != True:
		axs2.set_ylim([min(flux)/5., max(flux)*10.])
	else:
		axs2.set_ylim([min(flux)/5., max(FnuGal_Aw)*10.])
	axs2.set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', FontProperties = font0)
	axs2.set_ylabel(r'Flux (Jy)', FontProperties = font0)
	axs2.legend(frameon = False, fontsize = 16, ncol = 2)

	# if saveRes is True, save the figures at the locations pathFig.
	if saveRes == True:
		fig1.savefig(pathFig+sourceName+'_fitResAll_photo.pdf')
		fig2.savefig(pathFig+sourceName+'_fitResBM_photo.pdf')
	else:
		plt.show()
	plt.close('all')