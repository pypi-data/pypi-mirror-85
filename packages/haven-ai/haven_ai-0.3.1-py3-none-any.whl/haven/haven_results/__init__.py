import copy
import glob
import os
import sys
import pprint
from itertools import groupby
from textwrap import wrap
import numpy as np
import pandas as pd
import pylab as plt
import tqdm

from .. import haven_jobs as hjb
from .. import haven_utils as hu
from .. import haven_share as hd
from .tables_scores import *
from .plots_line import *
from . import images_fig
# from . import tools


class ResultManager:
    def __init__(self, 
                 savedir_base,
                 exp_list=None,
                 filterby_list=None,
                 verbose=True,
                 has_score_list=False,
                 exp_groups=None,
                 mode_key=None,
                 exp_ids=None,
                 save_history=False,
                 score_list_name='score_list.pkl',
                 account_id=None):
        """[summary]
        
        Parameters
        ----------
        savedir_base : [type]
            A directory where experiments are saved
        exp_list : [type], optional
            [description], by default None
        filterby_list : [type], optional
            [description], by default None
        has_score_list : [type], optional
            [description], by default False
        
        Example
        -------
        >>> from haven import haven_results as hr
        >>> savedir_base='../results'
        >>> rm = hr.ResultManager(savedir_base=savedir_base,
                                filterby_list=[{'dataset':'mnist'}],
                                verbose=1)
        >>> for df in rm.get_score_df():
        >>>     display(df)
        >>> fig_list = rm.get_plot_all(y_metric_list=['train_loss', 'val_acc'], 
                                    order='groups_by_metrics',
                                    x_metric='epoch', 
                                    figsize=(15,6),
                                    title_list=['dataset'],
                                    legend_list=['model']) 
        """
        
        # sanity checks
        assert os.path.exists(savedir_base), '%s does not exist' % savedir_base

        self.exp_groups = {}
        if exp_groups is not None:
            if isinstance(exp_groups, dict):
                # load from a dict
                self.exp_groups = exp_groups
            elif os.path.exists(exp_groups):
                # load from a file
                self.exp_groups = hu.load_py(exp_groups).EXP_GROUPS
            else:
                raise ValueError('%s does not exist...' % exp_groups)
        
        # rest
        self.score_list_name = score_list_name
        self.mode_key = mode_key
        self.has_score_list = has_score_list
        self.save_history = save_history
        self.account_id = account_id
        # get exp _list
        
        if exp_ids is not None:
            assert exp_list is None, "settings exp_ids require exp_list=None"
            assert exp_groups is None, "settings exp_ids require exp_groups=None"
            exp_list = []
            for exp_id in exp_ids:
                exp_list += [hu.load_json(os.path.join(savedir_base, exp_id, 'exp_dict.json'))]
        else:
            if exp_list is None:
                exp_list = hu.get_exp_list(savedir_base=savedir_base, verbose=verbose)
            else:
                exp_list = exp_list
            
            if len(exp_list) == 0:
                raise ValueError('exp_list is empty...')

        exp_list_with_scores = [e for e in exp_list if 
                                    os.path.exists(os.path.join(savedir_base, 
                                                                hu.hash_dict(e),
                                                                score_list_name))]
        if has_score_list:
            exp_list = exp_list_with_scores

        self.exp_list_all = copy.deepcopy(exp_list)

        
        self.score_keys  = ['None']

        if len(exp_list_with_scores):
            score_fname = os.path.join(savedir_base, hu.hash_dict(exp_list_with_scores[0]), score_list_name)
            self.score_keys = ['None'] + list(hu.load_pkl(score_fname)[0].keys())
                    
                                                        
        self.savedir_base = savedir_base
        
        self.filterby_list = filterby_list
        self.verbose = verbose

        self.n_exp_all = len(exp_list)

        self.exp_list = hu.filter_exp_list(exp_list, 
                                        filterby_list=filterby_list, 
                                        savedir_base=savedir_base,
                                        verbose=verbose)

        if len(self.exp_list) != 0:
            self.exp_params = list(self.exp_list[0].keys())
        else:
            self.exp_params = []

        
        
        if mode_key:
            for exp_dict in exp_list:
                exp_dict[mode_key] = 1
            for exp_dict in self.exp_list_all:
                exp_dict[mode_key] = 1

        self.exp_groups['all'] = copy.deepcopy(self.exp_list_all)
    
    def get_state_dict(self):
        pass
    def load_state_dict(self, state_dict):
        pass

    def get_plot(self, groupby_list=None, savedir_plots=None, filterby_list=None, **kwargs):
        fig_list = []
        filterby_list = filterby_list or self.filterby_list
        exp_groups = hu.group_exp_list(self.exp_list, groupby_list)
        
        for i, exp_list in enumerate(exp_groups):
            fig, ax = get_plot(exp_list=exp_list, savedir_base=self.savedir_base, filterby_list=filterby_list, 
                        
                        verbose=self.verbose,
                        score_list_name=self.score_list_name,
                               **kwargs)
            fig_list += [fig]

            # save image if given
            if savedir_plots != '' and savedir_plots is not None:
                os.makedirs(savedir_plots, exist_ok=True)
                save_fname = os.path.join(savedir_plots, "%d.png" % i )
                fig.savefig(save_fname, bbox_inches='tight')

        return fig_list

    def get_plot_all(self, y_metric_list, order='groups_by_metrics', 
                     groupby_list=None, ylim_list=None, xlim_list=None,
                     savedir_plots=None, legend_last_row_only=False, show_legend_all=None,
                     **kwargs):
        """[summary]
        
        Parameters
        ----------
        y_metric_list : [type]
            [description]
        order : str, optional
            [description], by default 'groups_by_metrics'
        
        Returns
        -------
        [type]
            [description]
        
        """
        
        if order not in ['groups_by_metrics', 'metrics_by_groups']:
            raise ValueError('%s order is not defined, choose between %s' % (order, ['groups_by_metrics', 'metrics_by_groups']))
        exp_groups = hu.group_exp_list(self.exp_list, groupby_list)
        figsize = kwargs.get('figsize') or None
        
        fig_list = []

        if not isinstance(y_metric_list, list):
            y_metric_list = [y_metric_list]

        if ylim_list is not None:
            assert isinstance(ylim_list[0], list), "ylim_list has to be lists of lists"
        if xlim_list is not None:
            assert isinstance(xlim_list[0], list), "xlim_list has to be lists of lists"

        if order == 'groups_by_metrics':
            for j, exp_list in enumerate(exp_groups):   
                fig, ax_list = plt.subplots(nrows=1, ncols=len(y_metric_list), figsize=figsize)
                if not hasattr(ax_list, 'size'):
                    ax_list = [ax_list]
                for i, y_metric in enumerate(y_metric_list):
                    if i == (len(y_metric_list) - 1):
                        show_legend = True
                    else:
                        show_legend = False
                    
                    ylim = None
                    xlim = None
                    if ylim_list is not None:
                        assert len(ylim_list) == len(exp_groups), "ylim_list has to have %d rows" % len(exp_groups)
                        assert len(ylim_list[0]) == len(y_metric_list), "ylim_list has to have %d cols" % len(y_metric_list)
                        ylim = ylim_list[j][i]
                    if xlim_list is not None:
                        assert len(xlim_list) == len(exp_groups), "xlim_list has to have %d rows" % len(exp_groups)
                        assert len(xlim_list[0]) == len(y_metric_list), "xlim_list has to have %d cols" % len(y_metric_list)
                        xlim = xlim_list[j][i]
                    if show_legend_all is not None:
                        show_legend = show_legend_all
                    fig, _ = get_plot(exp_list=exp_list, savedir_base=self.savedir_base, y_metric=y_metric, 
                                    fig=fig, axis=ax_list[i], verbose=self.verbose, filterby_list=self.filterby_list,
                                    show_legend=show_legend,
                                    ylim=ylim, xlim=xlim,
                                    score_list_name=self.score_list_name,
                                    **kwargs)
                fig_list += [fig]

        elif order == 'metrics_by_groups':

            for j, y_metric in enumerate(y_metric_list):   
                fig, ax_list = plt.subplots(nrows=1, ncols=len(exp_groups) , figsize=figsize)
                if not hasattr(ax_list, 'size'):
                    ax_list = [ax_list]
                for i, exp_list in enumerate(exp_groups):
                    if i == 0:
                        show_ylabel = True
                    else:
                        show_ylabel = False

                    if i == (len(exp_groups) - 1):
                        show_legend = True
                    else:
                        show_legend = False

                    if legend_last_row_only and j < (len(y_metric_list) - 1):
                        show_legend = False

                    ylim = None
                    xlim = None
                    if ylim_list is not None:
                        assert len(ylim_list) == len(y_metric_list), "ylim_list has to have %d rows" % len(exp_groups)
                        assert len(ylim_list[0]) == len(exp_groups), "ylim_list has to have %d cols" % len(y_metric_list)
                        ylim = ylim_list[j][i]
                    if xlim_list is not None:
                        assert len(xlim_list) == len(y_metric_list), "xlim_list has to have %d rows" % len(exp_groups)
                        assert len(xlim_list[0]) == len(exp_groups), "xlim_list has to have %d cols" % len(y_metric_list)
                        xlim = xlim_list[j][i]

                    if show_legend_all is not None:
                        show_legend = show_legend_all
                        
                    fig, _ = get_plot(exp_list=exp_list, savedir_base=self.savedir_base, y_metric=y_metric, 
                                    fig=fig, axis=ax_list[i], verbose=self.verbose, filterby_list=self.filterby_list,
                                    ylim=ylim, xlim=xlim,
                                    show_legend=show_legend,
                                    show_ylabel=show_ylabel,
                                    score_list_name=self.score_list_name,
                                    **kwargs)
                fig_list += [fig]

        plt.tight_layout()
        if savedir_plots:
            for i in range(len(fig_list)):
                os.makedirs(savedir_plots, exist_ok=True)
                fname = os.path.join(savedir_plots + '_%d.pdf' % i)
                fig_list[i].savefig(fname,
                                     dpi=300, 
                                     bbox_inches='tight')
                print(fname, 'saved')
                
        return fig_list
    
    def get_score_df(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        df_list = get_score_df(exp_list=self.exp_list, 
                    savedir_base=self.savedir_base, verbose=self.verbose, 
                    score_list_name=self.score_list_name,
                    **kwargs)
        return df_list 

    def to_dropbox(self, outdir_base, access_token):
        """[summary]
        """ 
        hd.to_dropbox(self.exp_list, savedir_base=self.savedir_base, 
                          outdir_base=outdir_base,
                          access_token=access_token)

    def get_exp_list_df(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        df_list = get_exp_list_df(exp_list=self.exp_list,
                     verbose=self.verbose, **kwargs)
        
        return df_list 

    def get_exp_table(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        table = get_exp_list_df(exp_list=self.exp_list, verbose=self.verbose, **kwargs)
        return table 

     
    def get_score_table(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        table = get_score_df(exp_list=self.exp_list, 
                    savedir_base=self.savedir_base, 
                    score_list_name=self.score_list_name,
                    filterby_list=self.filterby_list,
                    verbose=self.verbose, **kwargs)
        return table 

    def get_score_lists(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        score_lists = get_score_lists(exp_list=self.exp_list, 
                                      savedir_base=self.savedir_base, 
                                      score_list_name=self.score_list_name,
                                      filterby_list=self.filterby_list,
                                      verbose=self.verbose, **kwargs)
        return score_lists

    def get_images(self, **kwargs):
        """[summary]
        
        Returns
        -------
        [type]
            [description]
        """
        return images_fig.get_images(exp_list=self.exp_list, savedir_base=self.savedir_base, verbose=self.verbose, **kwargs)

    def get_job_summary(self, columns=None, add_prefix=False, **kwargs):
        """[summary]
        """
        exp_list = hu.filter_exp_list(self.exp_list, self.filterby_list, savedir_base=self.savedir_base, verbose=self.verbose)
        jm = hjb.JobManager(exp_list=exp_list, savedir_base=self.savedir_base, account_id=self.account_id, **kwargs)
        summary_list = jm.get_summary_list(columns=columns, add_prefix=add_prefix)

        return summary_list
            
    def to_zip(self, savedir_base='', fname='tmp.zip', **kwargs):
        """[summary]
        
        Parameters
        ----------
        fname : [type]
            [description]
        """
        from haven.haven_share import haven_dropbox as hd
        if savedir_base == '':
            savedir_base = self.savedir_base
        exp_id_list = [hu.hash_dict(exp_dict) for exp_dict in self.exp_list]
        hd.zipdir(exp_id_list, savedir_base, fname, **kwargs)

    def to_dropbox(self, fname, dropbox_path=None, access_token=None):
        """[summary]
        
        Parameters
        ----------
        fname : [type]
            [description]
        dropbox_path : [type], optional
            [description], by default None
        access_token : [type], optional
            [description], by default None
        """
        from haven import haven_dropbox as hd

        out_fname = os.path.join(dropbox_path, fname)
        src_fname = os.path.join(self.savedir_base, fname)
        self.to_zip(src_fname)
        hd.upload_file_to_dropbox(src_fname, out_fname, access_token)
        print('saved: https://www.dropbox.com/home/%s' % out_fname)






