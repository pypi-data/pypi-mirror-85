# from __future__ import print_function, absolute_import, division
import multiprocessing
import re
import shutil
import types
from pathlib import Path

import allesfitter
import numpy as np
import matplotlib
from argparse import ArgumentParser

matplotlib.use('Agg')
import pandas as pd
import os
from os.path import exists
import ast
import csv
from LATTE import LATTEutils, LATTEbrew, LATTE_DV
from os import path
'''WATSON: Verboseless Vetting and Adjustments of Transits for Sherlock Objects of iNterest
This class intends to provide a inspection and transit fitting tool for SHERLOCK Candidates.
'''
# get the system path
syspath = str(os.path.abspath(LATTEutils.__file__))[0:-14]
# ---------

# --- IMPORTANT TO SET THIS ----
out = 'pipeline'  # or TALK or 'pipeline'
ttran = 0.1
resources_dir = path.join(path.dirname(__file__))

class Watson:
    def __init__(self, cpus, object_dir):
        self.args = types.SimpleNamespace()
        self.args.noshow = True
        self.args.north = False
        self.args.o = True
        self.args.auto = True
        self.args.save = True
        self.args.nickname = ""  # TODO do we set the sherlock id?
        self.args.FFI = False  # TODO get this from input
        self.args.targetlist = "best_signal_latte_input.csv"
        self.args.new_path = ""  # TODO check what to do with this
        self.object_dir = os.getcwd() if object_dir is None else object_dir
        self.latte_dir = str(Path.home()) + "/.sherlockpipe/latte/"
        if not os.path.exists(self.latte_dir):
            os.mkdir(self.latte_dir)
        self.cpus = cpus

    def __prepare(self):
        # check whether a path already exists
        indir = self.latte_dir
        # SAVE the new output path
        if not os.path.exists("{}/_config.txt".format(indir)):
            with open("{}/_config.txt".format(indir), 'w') as f:
                f.write(str(indir))
            # TODO force this every time so new data is downloaded?
            # this is also the first time that the program is being run, so download all the data that is required.
            print("\n Download the text files required ... ")
            print("\n Only the manifest text files (~325 M) will be downloaded and no TESS data.")
            print("\n This step may take a while but luckily it only has to run once... \n")
            if not os.path.exists("{}".format(indir)):
                os.makedirs(indir)
            if not os.path.exists("{}/data".format(indir)):
                os.makedirs("{}/data".format(indir))
            outF = open(indir + "/data/temp.txt", "w")
            outF.write("#all LC file links")
            outF.close()
            outF = open(indir + "/data/temp_tp.txt", "w+")
            outF.write("#all LC file links")
            outF.close()
            LATTEutils.data_files(indir)
            LATTEutils.tp_files(indir)
            LATTEutils.TOI_TCE_files(indir)
            LATTEutils.momentum_dumps_info(indir)
        df = pd.read_csv(self.data_dir + "/" + self.args.targetlist)
        df['TICID'] = df['TICID'].str.replace("TIC ", "")
        TIC_wanted = list(set(df['TICID']))
        nlc = len(TIC_wanted)
        print("nlc length: {}".format(nlc))
        print('{}/manifest.csv'.format(str(indir)))
        if exists('{}/manifest.csv'.format(str(indir))):
            print("Existing manifest file found, will skip previously processed LCs and append to end of manifest file")
        else:
            print("Creating new manifest file")
            metadata_header = ['TICID', 'Marked Transits', 'Sectors', 'RA', 'DEC', 'Solar Rad', 'TMag', 'Teff',
                               'thissector', 'TOI', 'TCE', 'TCE link', 'EB', 'Systematics', 'Background Flux',
                               'Centroids Positions', 'Momentum Dumps', 'Aperture Size', 'In/out Flux', 'Keep',
                               'Comment', 'starttime']
            with open('{}/manifest.csv'.format(str(indir)), 'w') as f:  # save in the photometry folder
                writer = csv.writer(f, delimiter=',')
                writer.writerow(metadata_header)
        return indir, df, TIC_wanted

    def __process(self, indir, tic, sectors_in, transit_list):
        sectors_all, ra, dec = LATTEutils.tess_point(indir, tic)
        try:
            sectors = list(set(sectors_in) & set(sectors_all))
            if len(sectors) == 0:
                print("The target was not observed in the sector(s) you stated ({}). \
                        Therefore take all sectors that it was observed in: {}".format(sectors, sectors_all))
                sectors = sectors_all
        except:
            sectors = sectors_all
        alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2, ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad = LATTEutils.download_data(
            indir, sectors, tic)

        # in my input file the the times start at 0 for each sector so I need the line below
        # transit_list = list(np.array(transit_list) + np.nanmin(alltime))
        # ------------
        simple = False
        BLS = False
        model = False
        save = True
        DV = True
        try:
            LATTEbrew.brew_LATTE(tic, indir, syspath, transit_list, simple, BLS, model, save, DV, sectors,
                                 sectors_all,
                                 alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2,
                                 ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad, ra,
                                 dec, self.args)
            # LATTE_DV.LATTE_DV(tic, indir, syspath, transit_list, sectors_all, simple, BLS, model, save, DV, sectors,
            #                      sectors_all,
            #                      alltime, allflux, allflux_err, all_md, alltimebinned, allfluxbinned, allx1, allx2,
            #                      ally1, ally2, alltime12, allfbkg, start_sec, end_sec, in_sec, tessmag, teff, srad, ra,
            #                      dec, self.args)
            tp_downloaded = True
        except:
            # see if it made any plots - often it just fails on the TPs as they are very large
            if exists("{}/{}/{}_fullLC_md.png".format(indir, tic, tic)):
                print("couldn't download TP but continue anyway")
                tp_downloaded = False
            else:
                mnd = {}
                mnd['TICID'] = -99
                return mnd
        # check again whether the TPs downloaded - depending on where the code failed it might still have worked.
        if exists("{}/{}/{}_aperture_size.png".format(indir, tic, tic)):
            tp_downloaded = True
        else:
            tp_downloaded = False
            print("code ran but no TP -- continue anyway")
        # -------------
        # check whether it's a TCE or a TOI

        # TCE -----
        lc_dv = np.genfromtxt('{}/data/tesscurl_sector_all_dv.sh'.format(indir), dtype=str)
        TCE_links = []
        for i in lc_dv:
            if str(tic) in str(i[6]):
                TCE_links.append(i[6])
        if len(TCE_links) == 0:
            TCE = " - "
            TCE = False
        else:
            TCE_links = np.sort(TCE_links)
            TCE_link = TCE_links[0]  # this link should allow you to acess the MAST DV report
            TCE = True
        # TOI -----
        TOI_planets = pd.read_csv('{}/data/TOI_list.txt'.format(indir), comment="#")
        TOIpl = TOI_planets.loc[TOI_planets['TIC'] == float(tic)]
        if len(TOIpl) == 0:
            TOI = False
        else:
            TOI = True
            TOI_name = (float(TOIpl["Full TOI ID"]))
        # -------------
        # return the tic so that it can be stored in the manifest to keep track of which files have already been produced
        # and to be able to skip the ones that have already been processed if the code has to be restarted.
        mnd = {}
        mnd['TICID'] = tic
        mnd['MarkedTransits'] = transit_list
        mnd['Sectors'] = sectors_all
        mnd['RA'] = ra
        mnd['DEC'] = dec
        mnd['SolarRad'] = srad
        mnd['TMag'] = tessmag
        mnd['Teff'] = teff
        mnd['thissector'] = sectors
        # make empty fields for the test to be checked
        if TOI == True:
            mnd['TOI'] = TOI_name
        else:
            mnd['TOI'] = " "
        if TCE == True:
            mnd['TCE'] = "Yes"
            mnd['TCE_link'] = TCE_link
        else:
            mnd['TCE'] = " "
            mnd['TCE_link'] = " "
        mnd['EB'] = " "
        mnd['Systematics'] = " "
        mnd['TransitShape'] = " "
        mnd['BackgroundFlux'] = " "
        mnd['CentroidsPositions'] = " "
        mnd['MomentumDumps'] = " "
        mnd['ApertureSize'] = " "
        mnd['InoutFlux'] = " "
        mnd['Keep'] = " "
        mnd['Comment'] = " "
        mnd['starttime'] = np.nanmin(alltime)
        return mnd

    def vetting(self):
        # TODO add TPFPlotter code here
        indir, df, TIC_wanted = self.__prepare()
        for tic in TIC_wanted:
            # check the existing manifest to see if I've processed this file!
            manifest_table = pd.read_csv('{}/manifest.csv'.format(str(indir)))
            # get a list of the current URLs that exist in the manifest
            urls_exist = manifest_table['TICID']
            if not np.isin(tic, urls_exist):
                # get the transit time list
                transit_list = ast.literal_eval(((df.loc[df['TICID'] == tic]['transits']).values)[0])
                try:
                    sectors_in = ast.literal_eval(str(((df.loc[df['TICID'] == tic]['sectors']).values)[0]))
                    if (type(sectors_in) == int) or (type(sectors_in) == float):
                        sectors = [sectors_in]
                    else:
                        sectors = list(sectors_in)
                except:
                    sectors = [0]
                res = self.__process(indir, tic, sectors, transit_list)
                if res['TICID'] == -99:
                    print('something went wrong')
                    continue
                # make sure the file is opened as append only
                with open('{}/manifest.csv'.format(str(indir)), 'a') as tic:  # save in the photometry folder
                    writer = csv.writer(tic, delimiter=',')
                    metadata_data = [res['TICID']]
                    metadata_data.append(res['MarkedTransits'])
                    metadata_data.append(res['Sectors'])
                    metadata_data.append(res['RA'])
                    metadata_data.append(res['DEC'])
                    metadata_data.append(res['SolarRad'])
                    metadata_data.append(res['TMag'])
                    metadata_data.append(res['Teff'])
                    metadata_data.append(res['thissector'])
                    metadata_data.append(res['TOI'])
                    metadata_data.append(res['TCE'])
                    metadata_data.append(res['TCE_link'])
                    metadata_data.append(res['EB'])
                    metadata_data.append(res['Systematics'])
                    metadata_data.append(res['BackgroundFlux'])
                    metadata_data.append(res['CentroidsPositions'])
                    metadata_data.append(res['MomentumDumps'])
                    metadata_data.append(res['ApertureSize'])
                    metadata_data.append(res['InoutFlux'])
                    metadata_data.append(res['Keep'])
                    metadata_data.append(res['Comment'])
                    metadata_data.append(res['starttime'])
                    writer.writerow(metadata_data)
            else:
                print('TIC {} already done - skipping'.format(tic))
        return TIC_wanted
    def show_candidates(self):
        self.candidates = pd.read_csv(self.object_dir + "/candidates.csv")
        self.candidates.index = np.arange(1, len(self.candidates) + 1)
        print("Suggested candidates are:")
        print(self.candidates.to_markdown(index=True))
        pass

    def demand_candidate_selection(self):
        user_input = input("Select candidate number to be examined and fit: ")
        if user_input.startswith("q"):
            raise SystemExit("User quitted")
        self.candidate_selection = int(user_input)
        if self.candidate_selection < 1 or self.candidate_selection > len(self.candidates.index):
            raise SystemExit("User selected a wrong candidate number.")
        self.data_dir = self.object_dir + "/" + str(self.candidate_selection)

    def fit(self):
        allesfit_dir = self.data_dir + "/fit/"
        if not os.path.exists(allesfit_dir):
            os.makedirs(allesfit_dir)
        star_file = allesfit_dir + "params_star.csv"
        params_file = allesfit_dir + "params.csv"
        settings_file = allesfit_dir + "settings.csv"
        shutil.copyfile(self.object_dir + "/lc.csv", allesfit_dir + "lc.csv")
        shutil.copyfile(self.object_dir + "/params_star.csv", star_file)
        shutil.copyfile(resources_dir + "/resources/allesfitter/params.csv", params_file)
        shutil.copyfile(resources_dir + "/resources/allesfitter/settings.csv", settings_file)
        star_df = pd.read_csv(star_file)
        # TODO replace sherlock properties from allesfitter files
        with open(settings_file, 'r+') as f:
            text = f.read()
            text = re.sub('\\${sherlock:cores}', str(self.cpus), text)
            f.seek(0)
            f.write(text)
            f.truncate()
        with open(params_file, 'r+') as f:
            candidate_row = self.candidates.iloc[self.candidate_selection - 1]
            text = f.read()
            text = re.sub('\\${sherlock:t0}', str(candidate_row["t0"]), text)
            text = re.sub('\\${sherlock:period}', str(candidate_row["period"]), text)
            rp_rs = candidate_row["rp_rs"] if candidate_row["rp_rs"] != "-" else 0.1
            text = re.sub('\\${sherlock:rp_rs}', str(rp_rs), text)
            sum_rp_rs_a = (candidate_row["rp_rs"] + star_df.iloc[0]['R_star']) / candidate_row["a"] * 0.00465047 \
                if candidate_row["rp_rs"] != "-" else 0.2
            text = re.sub('\\${sherlock:sum_rp_rs_a}', str(sum_rp_rs_a), text)
            f.seek(0)
            f.write(text)
            f.truncate()
        allesfitter.show_initial_guess(allesfit_dir)
        allesfitter.ns_fit(allesfit_dir)
        allesfitter.ns_output(allesfit_dir)

if __name__ == '__main__':
    ap = ArgumentParser(description='Visual Vetting and Adjustments of Transits for Sherlock Objects of iNterest')
    ap.add_argument('--no-vetting', dest='vetting', help="Disables vetting", action='store_false')
    ap.set_defaults(vetting=True)
    ap.add_argument('--no-fitting', dest='fitting', help="Disables fitting", action='store_false')
    ap.set_defaults(fitting=True)
    ap.add_argument('--object_dir', default=True, help="If the object directory is not your current one you need to provide the ABSOLUTE path", required=False)
    ap.add_argument('--cores', type=int, default=1, help="Number of CPU cores to be used.", required=False)
    ap.add_argument('--candidate', type=int, default=None, help="The candidate signal to be used.", required=False)
    args = ap.parse_args()
    watson = Watson(args.cores, args.object_dir)
    if args.candidate is None:
        watson.show_candidates()
        watson.demand_candidate_selection()
    print("Selected signal number " + str(watson.candidate_selection))
    if args.vetting:
        tics_processed = watson.vetting()
        dir = watson.data_dir + "/vetting"
        if os.path.exists(dir) and os.path.isdir(dir):
            shutil.rmtree(dir, ignore_errors=True)
        [shutil.move(watson.latte_dir + "/" + tic, watson.data_dir + "/vetting") for tic in tics_processed]
    if args.fitting:
        watson.fit()
