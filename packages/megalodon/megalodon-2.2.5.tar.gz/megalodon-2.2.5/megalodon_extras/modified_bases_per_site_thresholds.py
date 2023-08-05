import queue
import multiprocessing as mp
from collections import defaultdict

import numpy as np
from tqdm import tqdm

from megalodon import (
    logging, megalodon_multiprocessing as mega_mp, mods,
    megalodon_helper as mh)
from ._extras_parsers import get_parser_modified_bases_per_site_thresholds


BED_TMPLT = '{chrom}\t{pos}\t{end}\t.\t{score}\t{strand}\n'
COV_PCTLS = [1.0, 5.0, 10.0, 15.0, 20.0, 25.0]
MAX_MOD_SCORE = 100

MAX_BATCHES = 10

LOGGER = logging.get_logger()


def write_low_cov_worker(low_cov_q, low_cov_fn):
    with open(low_cov_fn, 'w') as low_cov_fp:
        while True:
            try:
                low_cov_batch = low_cov_q.get(block=True, timeout=0.1)
            except queue.Empty:
                continue
            if low_cov_batch is None:
                break
            low_cov_fp.write(low_cov_batch)


def write_thresh_worker(thresh_q, thresh_fn):
    bar = tqdm(desc='Completed Batches', smoothing=0)
    with open(thresh_fn, 'w') as thresh_fp:
        while True:
            try:
                thresh_batch = thresh_q.get(block=True, timeout=0.1)
            except queue.Empty:
                continue
            if thresh_batch is None:
                break
            bar.update()
            thresh_fp.write(thresh_batch)
    bar.close()


def extract_threshs_worker(
        site_batches_q, thresh_q, low_cov_q, mod_db_fn, gt_cov_min, np_cov_min,
        target_mod_base, strand_offset):
    def get_gt_cov(chrm, strand, pos):
        cov_pos = pos if strand_offset is None else (
            pos - strand_offset if strand == -1 else pos)
        cov_strand = strand if strand_offset is None else None
        pos_cov = 0
        try:
            pos_cov = cov[(cov_pos, cov_strand)]
            if pos_cov < gt_cov_min:
                return pos_cov, 0
            return pos_cov, mod_cov[(cov_pos, cov_strand)]
        except KeyError:
            return 0, 0

    def get_pos_thresh(pos_cov, pos_mod_cov, pos_mod_data):
        if pos_mod_cov == 0:
            return '{:.4f}'.format(-MAX_MOD_SCORE)
        elif pos_mod_cov == pos_cov:
            return '{:.4f}'.format(MAX_MOD_SCORE)

        # determine fractional threshold
        # collate stats per-read
        pos_stats = defaultdict(dict)
        for read_dbid, mod_dbid, lp in pos_mod_data:
            pos_stats[read_dbid][mod_dbid] = lp
        pos_llrs = []
        with np.errstate(divide='ignore'):
            for read_pos_lps in pos_stats.values():
                mt_lps = list(read_pos_lps.values())
                can_lp = np.log1p(-np.exp(mt_lps).sum())
                for mod_dbid, mod_lp in read_pos_lps.items():
                    if mod_dbid == target_mod_dbid:
                        pos_llrs.append(can_lp - mod_lp)
        gt_meth_pct = 100.0 * pos_mod_cov / pos_cov
        return '{:.4f}'.format(np.percentile(pos_llrs, gt_meth_pct))

    mods_db = mods.ModsDb(mod_db_fn)
    target_mod_dbid = mods_db.get_mod_base_dbid(target_mod_base)
    while True:
        try:
            batch = site_batches_q.get(block=True, timeout=0.1)
        except queue.Empty:
            continue
        if batch is None:
            break
        chrm, pos_range, cov, mod_cov = batch
        batch_low_cov = []
        batch_threshs = []
        for (chrm, strand, pos), pos_mod_data in mods_db.iter_pos_scores(
                convert_pos=True, pos_range=(chrm, *pos_range)):
            str_strand = mh.int_strand_to_str(strand)
            # extract ground truth coverage
            pos_cov, pos_mod_cov = get_gt_cov(chrm, strand, pos)
            if pos_cov < gt_cov_min:
                batch_low_cov.append(
                    BED_TMPLT.format(
                        chrom=chrm, pos=pos, end=pos + 1, strand=str_strand,
                        score='GT_COV:{}'.format(pos_cov)))
                continue

            # if nanopore coverage is not deep enough write to blacklist
            target_mod_cov = len(set(
                read_id for read_id, mod_dbid, _ in pos_mod_data
                if mod_dbid == target_mod_dbid))
            if target_mod_cov < np_cov_min:
                # don't blacklist sites covered by other called mods
                if target_mod_cov > 0:
                    batch_low_cov.append(
                        BED_TMPLT.format(
                            chrom=chrm, pos=pos, end=pos + 1,
                            strand=str_strand,
                            score='NP_COV:{}'.format(target_mod_cov)))
                continue

            pos_thresh = get_pos_thresh(pos_cov, pos_mod_cov, pos_mod_data)
            batch_threshs.append(BED_TMPLT.format(
                chrom=chrm, pos=pos, end=pos + 1, strand=str_strand,
                score=pos_thresh))

        thresh_q.put(''.join(batch_threshs))
        low_cov_q.put(''.join(batch_low_cov))


def parse_bedmethyl_worker(site_batches_q, batch_size, gt_bed, strand_offset):
    for batch in mh.iter_bed_methyl_batches(gt_bed, strand_offset, batch_size):
        site_batches_q.put(batch)


def process_all_batches(
        num_proc, batch_size, gt_bed, low_cov_fn, thresh_fn, mod_db_fn,
        strand_offset, gt_cov_min, np_cov_min, target_mod_base):
    site_batches_q = mega_mp.CountingMPQueue(maxsize=MAX_BATCHES)
    parse_bm_p = mp.Process(
        target=parse_bedmethyl_worker,
        args=(site_batches_q, batch_size, gt_bed, strand_offset),
        daemon=True, name='ParseBedMethyl')
    parse_bm_p.start()
    thresh_q = mega_mp.CountingMPQueue(maxsize=MAX_BATCHES)
    low_cov_q = mega_mp.CountingMPQueue(maxsize=MAX_BATCHES)
    extract_threshs_ps = []
    for et_i in range(num_proc):
        extract_threshs_ps.append(mp.Process(
            target=extract_threshs_worker,
            args=(site_batches_q, thresh_q, low_cov_q, mod_db_fn, gt_cov_min,
                  np_cov_min, target_mod_base, strand_offset),
            daemon=True, name='ExtractThresh{:03d}'.format(et_i)))
        extract_threshs_ps[-1].start()
    write_thresh_p = mp.Process(
        target=write_thresh_worker,
        args=(thresh_q, thresh_fn),
        daemon=True, name='WriteThresh')
    write_thresh_p.start()
    write_low_cov_p = mp.Process(
        target=write_low_cov_worker,
        args=(low_cov_q, low_cov_fn),
        daemon=True, name='WriteLowCov')
    write_low_cov_p.start()

    LOGGER.debug('Waiting for parser to join')
    parse_bm_p.join()
    for _ in range(num_proc):
        site_batches_q.put(None)
    LOGGER.debug('DB extractor processes to join')
    for et_p in extract_threshs_ps:
        et_p.join()
    thresh_q.put(None)
    low_cov_q.put(None)
    LOGGER.debug('Write thresholds process to join')
    write_thresh_p.join()
    LOGGER.debug('Write low ocverage process to join')
    write_low_cov_p.join()


def check_matching_attrs(
        ground_truth_bed, strand_offset, mod_db_fn, target_mod_base,
        limit=10000):
    mods_db = mods.ModsDb(mod_db_fn)
    db_strands = (1, -1) if strand_offset is None else (None, )
    db_chrms = set((chrm, strand)
                   for _, chrm, _ in mods_db.iter_chrms()
                   for strand in db_strands)
    cov, mod_cov = mh.parse_bed_methyls(
        [ground_truth_bed, ], strand_offset, show_prog_bar=False, limit=limit)
    if len(db_chrms.intersection(cov.keys())) == 0:
        LOGGER.error(
            ('Using first {} sites from {}, found zero overlapping ' +
             'contig/chromosome names with the mod database.').format(
                 limit, ground_truth_bed))
        LOGGER.info('Database contigs/chromosomes: {}'.format(', '.join(
            map(str, db_chrms))))
        LOGGER.info('BED methyl contigs/chromosomes: {}'.format(', '.join(
            map(str, list(cov.keys())))))
        raise mh.MegaError('No overlapping contigs found.')
    db_mods = set(mod_base for mod_base, _ in mods_db.get_mod_long_names())
    if target_mod_base not in db_mods:
        raise mh.MegaError('Target modified base not found in mods database.')
    mods_db.check_data_covering_index_exists()
    mods_db.close()


def _main(args):
    logging.init_logger(log_fn=args.log_filename)
    LOGGER.info('Parsing ground truth bed methyl files')
    mod_db_fn = mh.get_megalodon_fn(args.megalodon_results_dir, mh.PR_MOD_NAME)
    check_matching_attrs(
        args.ground_truth_bed, args.strand_offset, mod_db_fn, args.mod_base)

    process_all_batches(
        args.processes, args.batch_size, args.ground_truth_bed,
        args.out_low_coverage_sites, args.out_per_site_mod_thresholds,
        mod_db_fn, args.strand_offset, args.ground_truth_cov_min,
        args.nanopore_cov_min, args.mod_base)


if __name__ == '__main__':
    _main(get_parser_modified_bases_per_site_thresholds().parse_args())
